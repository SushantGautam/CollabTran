from urllib.parse import unquote

import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.authtoken.models import Token

from .models import Contribution


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
    return render(request, 'LeaderBoard.html', {'data': None})


def MyProfile(request):
    return render(request, 'MyProfile.html', {'data': None})


from django.views import generic
from . import models
from . import forms

from django_filters.views import FilterView


class ContributionListView(FilterView):
    model = models.Contribution
    form_class = forms.ContributionForm
    paginate_by = 5  # and that's it !!
    template_name = "WebApp/contribution_list.html"

    def get_queryset(self):
        path = (self.request.GET.get('path', None))
        elementID = (self.request.GET.get('elementID', None))
        searchSubmission = (self.request.GET.get('searchSubmission', None))
        new_context = Contribution.objects.all()
        if (path and path != 'None'):
            new_context = new_context.filter(EditURL=unquote(path))
        if (elementID and elementID != 'None'):
            new_context = new_context.filter(EditxPath=unquote(elementID))
        if (searchSubmission and searchSubmission != 'None'):
            new_context = new_context.filter(Submission__contains=searchSubmission)

        return new_context

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['path'] = (self.request.GET.get('path', None))
        context['elementID'] = (self.request.GET.get('elementID', None))
        context['searchSubmission'] = (self.request.GET.get('searchSubmission', None))
        if (context['path'] == 'None'):
            context['path'] = None
        if (context['elementID'] == 'None'):
            context['elementID'] = None
        if (context['searchSubmission'] == 'None'):
            context['searchSubmission'] = None
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
    model = models.Urls
    form_class = forms.UrlsForm


def resolveURL(request):
    if request.user.is_anonymous:
        return HttpResponse('Unauthorized', status=401)
    EditURL = request.POST.get('EditURL')

    contributions_q = Contribution.objects.filter(EditURL=EditURL).values("id", 'Original', 'Submission', "EditxPath",
                                                                          'User__username',
                                                                          'created')
    df = pd.DataFrame(list(contributions_q))

    TotalElementsEditedOnThisPage = 0
    TotalEditsOnThisPage = 0
    if (len(df)):
        df['TotalEditsOnThisElement'] = df.groupby(['EditxPath'])['EditxPath'].transform('count')
        TotalElementsEditedOnThisPage = df[:].EditxPath.unique().__len__()
        TotalEditsOnThisPage = len(df)
        df = df[df.groupby(['EditxPath'])['id'].transform(max) == df['id']]
    # contributions = Contribution.objects.filter(EditURL=EditURL).annotate(
    #     latest_date=Max('created')).values('Submission', "EditxPath", 'User__username')

    # html = urlopen(url).read()
    # data = list(OrderedDict.fromkeys(text_from_html(html)))
    return JsonResponse(
        {"data": df.to_json(orient='index'), "TotalElementsEditedOnThisPage": TotalElementsEditedOnThisPage,
         "TotalEditsOnThisPage": TotalEditsOnThisPage},
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
    else:
        return render(request, 'home.html')
