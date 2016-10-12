from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

def HomeView(request):
    return render(request, "birdie/home.html", {})

@login_required
def AdminView(request):
    return render(request, "birdie/admin.html", {})