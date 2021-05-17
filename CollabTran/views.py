from django.http import HttpResponse


def gitpull(request):
    import subprocess
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return HttpResponse(output)
