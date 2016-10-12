import stripe
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

def HomeView(request):
    return render(request, "birdie/home.html", {})

@login_required
def AdminView(request):
    return render(request, "birdie/admin.html", {})

def PostCreateView(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, "birdie/home.html", context)

def PostUpdateView(request, pk):
    instance = get_object_or_404(Post, pk=pk)
    if request.user.first_name == 'Martin':
        raise Http404()
    form = PostForm(request.POST or None, instance=instance )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return redirect('/')
    context = {
        'form': form,
    }
    return render(request, "birdie/home.html", context)


def PaymentView(request):
    charge = stripe.Charge.create(
        amount=100,
        currency='sgd',
        description='',
        token=request.POST.get('token'),
    )
    send_mail(
        'Payment received',
        'Charge {} succeeded!'.format(charge['id']),
        'server@example.com',
        ['admin@example.com', ],
    )
    return redirect('/')