from django.shortcuts import render


def forum(request):
    return render(request, "forum/index.html", {})

