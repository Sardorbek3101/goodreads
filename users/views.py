from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from users.forms import UserCreateForm, UserUpdateForm
from users.models import CustomUser


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()  
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, "users/login.html", {"login_form": login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("books:list")
        else:
            return render(request, "users/login.html", {"login_form": login_form})


class ProfileView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        response = ''
        friends = None
        subscriptions_req = request.GET.get("user", "")
        subscribers = user.friendship_requests_to.all().count()
        subscriptions = user.friendship_requests_from.all().count()
        sub = {'subscribers': subscribers, 'subscriptions':subscriptions}
        if request.user.is_authenticated:
            for to in request.user.friendship_requests_from.all():
                if to.to_user == user:
                    response = 'request'
            for frm in request.user.friendship_requests_to.all():
                if frm.from_user == user:
                    response = 'to_request'
            for n in request.user.friends_to.all():
                if n.from_user == user:
                    response = 'friends'
                    friends = n
            for n in request.user.friends_from.all():
                if n.to_user == user:
                    response = 'friends'
                    friends = n

        return render(request, "users/profile.html", {"user": user, "response":response, "friends":friends, "sub":sub, "user_sub_req":subscriptions_req})


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("landing_page")


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        user_update_form = UserUpdateForm(instance=user)
        if request.user == user:
            return render(request, "users/profile_edit.html", {'form':user_update_form})
        return redirect(reverse("users:profile", kwargs={"id":id}))
        
    
    def post(self, request, id):
        user = CustomUser.objects.get(id=id)
        user_update_form = UserUpdateForm(
            instance=user,
            data=request.POST,
            files=request.FILES
        )
        if request.user == user:
            if user_update_form.is_valid():
                user_update_form.save()
                messages.success(request, "You have successfully updated your profile.")
                return redirect(reverse("users:profile", kwargs={"id":user.id}))
            
            return render(request, "users/profile_edit.html", {"form":user_update_form})
        
        return redirect(reverse("users:profile", kwargs={"id":id}))