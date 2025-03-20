from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import LoginForm, SignupForm
from users.models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("posts:feeds")
            else:
                form.add_error(None, "Invalid username or password")

        context = {
            "form": form
        }
        return render(request, 'users/login.html', context)
    else:
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return redirect("users:login")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("users:login")

    else:
        form = SignupForm()

    context = {"form": form}
    return render(request, 'users/signup.html', context)


def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {"user": user}
    return render(request, 'users/profile.html', context)


def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.follower_relationships.all()
    context = {
        "user": user,
        "relationships": relationships
    }
    return render(request, 'users/followers.html', context)


def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    relationships = user.following_relationships.all()
    context = {
        "user": user,
        "relationships": relationships
    }
    return render(request, 'users/following.html', context)


def follow(request, user_id):
    user = request.user
    target = get_object_or_404(User, id=user_id)

    if user.id == user_id and target in user.following.all():
        user.following.remove(target)

    if target in user.following.all():
        user.following.remove(target)
    else:
        user.following.add(target)

    url_next = request.GET.get('next') or reverse("users:profile", args=[user.id])
    return HttpResponseRedirect(url_next)
