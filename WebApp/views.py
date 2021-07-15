from collections import Counter
from datetime import datetime, timedelta
from math import floor
from urllib.parse import unquote

import pandas as pd
import pytz
from constance import config
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django_filters.views import FilterView
from rest_framework.authtoken.models import Token

from . import models, forms
from .models import Contribution, Votes


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def login_request(request):
    # from https://pythonprogramming.net/user-login-logout-django-tutorial/
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={"form": form})


def LeaderBoard(request):
    def ProcessQuery(hours=0):
        qur = Contribution.objects.filter(created__gte=pytz.utc.localize(
            datetime.now() - timedelta(hours=hours))).values_list("User__username").annotate(
            dcount=Count('User__username')).order_by()

        if (len(qur)):
            qur = pd.DataFrame(qur, columns=['Username', 'Count'])
        else:
            return [None, None, None, None]

        qur.sort_values('Count', inplace=True, ascending=False)
        qur.reset_index(drop=True, inplace=True)
        qur['Rank'] = list(qur.index + 1)

        if request.user.is_authenticated:
            myCurrent = (qur[qur['Username'] == request.user.username])

            after = qur[qur.Rank < int(myCurrent.Rank)].sort_values('Rank', ascending=True).tail(5)
            before = qur[qur.Rank > int(myCurrent.Rank)].sort_values('Rank', ascending=True).head(5)

            return [qur.head(11), before, after, myCurrent.values]
        return [qur, None, None, None]

    daily = ProcessQuery(hours=24)
    weekly = ProcessQuery(hours=24 * 7)
    monthly = ProcessQuery(hours=24 * 30)
    overall = ProcessQuery(hours=24 * 9999)
    context = {
        "daily": {
            "total": daily[0],
            "before": daily[1],
            "after": daily[2],
            "MyState": daily[3],
        }, "weekly": {
            "total": weekly[0],
            "before": weekly[1],
            "after": weekly[2],
            "MyState": weekly[3],
        }, "monthly": {
            "total": monthly[0],
            "before": monthly[1],
            "after": monthly[2],
            "MyState": monthly[3],
        }, "total": {
            "total": overall[0],
            "before": overall[1],
            "after": overall[2],
            "MyState": overall[3],
        },
    }

    return render(request, 'LeaderBoard.html', context)


def Profile(request):
    usr = (request.GET.get('usr', None))
    isMe = None
    if not usr or usr == 'None':
        if request.user.is_authenticated:
            user = request.user
            isMe = True
        else:
            messages.info(request, "You need to login to see your profile.")
            return redirect('login')
    else:
        user = get_object_or_404(User, username=usr)
        if user == request.user:
            isMe = True
    quest = {
        "daily": {
            "Votes_Get": config.Daily_Votes_Get,
            "Votes_Given": config.Daily_Votes_Given,
            "Contributions": config.Daily_Contributions,
        },
        "weekly": {
            "Votes_Get": config.Weekly_Votes_Get,
            "Votes_Given": config.Weekly_Votes_Given,
            "Contributions": config.Weekly_Contributions,
        },
        "monthly": {
            "Votes_Get": config.Monthly_Votes_Get,
            "Votes_Given": config.Monthly_Votes_Given,
            "Contributions": config.Monthly_Contributions,
        },
        "my":
            {"daily": {
                "Votes_Get": Votes.objects.filter(
                    last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(hours=24)),
                    contribution__User=user).count(),
                "Votes_Given": Votes.objects.filter(
                    last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(hours=24)),
                    voter=user).count(),
                "Contributions": Contribution.objects.filter(User=user, created__gte=pytz.utc.localize(
                    datetime.now() - timedelta(hours=24))).count(),
            },
                "weekly": {
                    "Votes_Get": Votes.objects.filter(
                        last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(days=7)),
                        contribution__User=user).count(),
                    "Votes_Given": Votes.objects.filter(
                        last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(days=7)),
                        voter=user).count(),
                    "Contributions": Contribution.objects.filter(User=user, created__gte=pytz.utc.localize(
                        datetime.now() - timedelta(days=7))).count(),
                },
                "monthly": {
                    "Votes_Get": Votes.objects.filter(
                        last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(days=30)),
                        contribution__User=user).count(),
                    "Votes_Given": Votes.objects.filter(
                        last_updated__gte=pytz.utc.localize(datetime.now() - timedelta(days=30)),
                        voter=user).count(),
                    "Contributions": Contribution.objects.filter(User=user, created__gte=pytz.utc.localize(
                        datetime.now() - timedelta(days=30))).count(),
                },
                "total": {
                    "Votes_Get": Votes.objects.filter(
                        contribution__User=user).count(),
                    "Votes_Given": Votes.objects.filter(
                        voter=user).count(),
                    "Contributions": Contribution.objects.filter(User=user, ).count(),
                },
            }
    }

    level = quest['my']['total']['Contributions'] + quest['my']['total']['Votes_Given'] + quest['my']['total'][
        'Votes_Get']
    return render(request, 'profile.html',
                  {'data': getUserContributions(user), "usr": user, 'isMe': isMe, "quest": quest,
                   "level": CalLevel(level)})


def CalLevel(TotalContribution):
    if (0 <= TotalContribution <= 10):
        return ['secondary', 'Novice', floor(TotalContribution / 1)]
    elif (11 <= TotalContribution <= 100):
        return ['warning', 'Beginner', floor(TotalContribution / 10)]
    elif (101 <= TotalContribution <= 1000):
        return ['primary', 'Competent', floor(TotalContribution / 100)]
    elif (1001 <= TotalContribution <= 10000):
        return ['success', 'Proficient', floor(TotalContribution / 1000)]
    elif (10001 <= TotalContribution):
        return ['danger', 'Expert', floor(TotalContribution / 10000)]


class ContributionListView(FilterView):
    model = models.Contribution
    form_class = forms.ContributionForm
    paginate_by = 5  # and that's it !!
    template_name = "WebApp/contribution_list.html"

    def get_queryset(self):
        path = (self.request.GET.get('path', None))
        elementID = (self.request.GET.get('elementID', None))
        searchSubmission = (self.request.GET.get('searchSubmission', None))
        user = (self.request.GET.get('user', None))

        new_context = Contribution.objects.all()
        if (path and path != 'None'):
            new_context = new_context.filter(EditURL=unquote(path))
        if (elementID and elementID != 'None'):
            new_context = new_context.filter(EditxPath=unquote(elementID))
        if (searchSubmission and searchSubmission != 'None'):
            new_context = new_context.filter(Submission__contains=searchSubmission)
        if (user and user != 'None'):
            new_context = new_context.filter(User__username=user)

        return new_context

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['path'] = (self.request.GET.get('path', None))
        context['elementID'] = (self.request.GET.get('elementID', None))
        context['searchSubmission'] = (self.request.GET.get('searchSubmission', None))
        context['usr'] = (self.request.GET.get('usr', None))
        if (context['path'] == 'None'):
            context['path'] = None
        if (context['elementID'] == 'None'):
            context['elementID'] = None
        if (context['searchSubmission'] == 'None'):
            context['searchSubmission'] = None
        if (context['usr'] == 'None' or context['usr'] == None):
            context['usr'] = None
        else:
            context['usr'] = get_object_or_404(User, username=context['usr'])
        context['paginationTrail'] = ""
        if context['path']: context['paginationTrail'] += "&path=" + context['path']
        if context['elementID']: context['paginationTrail'] += "&elementID=" + context['elementID']
        if context['searchSubmission']: context['paginationTrail'] += "&searchSubmission=" + context['searchSubmission']
        if context['usr']: context['paginationTrail'] += "&usr=" + context['usr'].username
        return context


#
# class ContributionCreateView(generic.CreateView):
#     model = models.Contribution
#     form_class = forms.ContributionForm


class ContributionDetailView(generic.DetailView):
    model = models.Contribution
    form_class = forms.ContributionForm


#
# class ContributionUpdateView(generic.UpdateView):
#     model = models.Contribution
#     form_class = forms.ContributionForm
#     pk_url_kwarg = "pk"
#

class UrlsListView(generic.ListView):
    model = models.Votes
    form_class = forms.VotesForm


def resolveURL(request):
    # if request.user.is_anonymous:
    #     return HttpResponse('Unauthorized', status=401)
    EditURL = request.POST.get('EditURL')

    contributions_q = Contribution.objects.filter(EditURL=EditURL).values("id", 'Original', 'Submission', "EditxPath",
                                                                          'User__username',
                                                                          'created')
    df = pd.DataFrame(list(contributions_q))

    TotalElementsEditedOnThisPage = 0
    TotalEditsOnThisPage = 0
    LastContributedInThisPageBy = ""
    if (len(df)):
        df['TotalEditsOnThisElement'] = df.groupby(['EditxPath'])['EditxPath'].transform('count')
        TotalElementsEditedOnThisPage = df[:].EditxPath.unique().__len__()
        TotalEditsOnThisPage = len(df)
        df = df[df.groupby(['EditxPath'])['id'].transform(max) == df['id']]
        LastContributedInThisPageBy = "Top Contributors: " + "".join(
            ['''<a href="/Profile?usr=''' + i[0] + '''"> ''' + i[0] + '''</a>, ''' for i in
             Counter(df[:].User__username).most_common(3)])
    # contributions = Contribution.objects.filter(EditURL=EditURL).annotate(
    #     latest_date=Max('created')).values('Submission', "EditxPath", 'User__username')

    # html = urlopen(url).read()
    # data = list(OrderedDict.fromkeys(text_from_html(html)))
    return JsonResponse(
        {"data": df.to_json(orient='index'), "TotalElementsEditedOnThisPage": TotalElementsEditedOnThisPage,
         "TotalEditsOnThisPage": TotalEditsOnThisPage,
         "LastContributedInThisPageBy": LastContributedInThisPageBy,
         },
        safe=False)


def SubmitContributions(request):
    if request.user.is_anonymous:
        return HttpResponse('Unauthorized', status=401)

    User = request.user
    Submission = request.POST.get("Submission")
    EditURL = request.POST.get('EditURL')
    EditxPath = request.POST.get('EditxPath')
    Original = request.POST.get('Original')
    try:
        contribution = Contribution.objects.create(User=User, Submission=Submission, EditURL=EditURL,
                                                   EditxPath=EditxPath, Original=Original)
        if contribution.getDifference():
            contribution.save()

            return JsonResponse({"difference": contribution.getDifference()})
        else:
            return JsonResponse({"errorMessage": "No Change Detected"}, status=500)

    except Exception  as e:
        return JsonResponse({"errorMessage": str(e)}, status=500)


def home(request, token=None):
    if request.user.is_authenticated:
        token = Token.objects.get_or_create(user=request.user)[0].key
    navigateToPage = request.GET.get('navigateToPage', None)
    navigateToID = request.GET.get('navigateToID', None)
    return render(request, 'home.html', context={"token": token,
                                                 "navigateToPage": navigateToPage,
                                                 "navigateToID": navigateToID,
                                                 })


def getUserContributions(user):
    return {"daily": 10}


@login_required
def SubmitVote(request):
    contribution = Contribution.objects.get(pk=int(request.POST.get('submissionID')))
    type = request.POST.get('vote')
    obj, created = Votes.objects.get_or_create(voter=request.user, contribution=contribution)
    if (obj.type == type):
        obj.delete()
    else:
        obj.type = type
        obj.save()

    return JsonResponse({"countVote": contribution.countVote(), "My": contribution.countVote(request.user)})
