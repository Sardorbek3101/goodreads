from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from friends.models import Friendship, FriendshipRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser


class FriendshipRequestView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'friends/friendship_requests.html', {"user":request.user})

class CreateFriendshipRequestView(View):
    def get(self, request, id):
        to_user = CustomUser.objects.get(id=id)
        if request.user.is_authenticated:
            if request.user == to_user:
                messages.warning(request, "Вы не можете предложить дружбу сам себе!")
                return redirect(reverse("users:profile", kwargs={"id":to_user.id}))
            
            for n in request.user.friends_to.all():
                if n.from_user == to_user:
                    messages.warning(request, "Вы уже друзья !")
                    return redirect(reverse("users:profile", kwargs={"id":to_user.id}))
                
            for n in request.user.friends_from.all():
                if n.to_user == to_user:
                    messages.warning(request, "Вы уже друзья !")
                    return redirect(reverse("users:profile", kwargs={"id":to_user.id}))

            for to in request.user.friendship_requests_from.all():
                if to.to_user == to_user:
                    messages.warning(request, "Предложение на дружбу уже отправлена ! Вы не можете предложить дружбу два раза !")
                    return redirect(reverse("users:profile", kwargs={"id":to_user.id}))
            else:
                FriendshipRequest.objects.create(
                    from_user = request.user,
                    to_user = to_user
                )

        return redirect(reverse("users:profile", kwargs={"id":to_user.id}))
    
class DontFriendshipView(LoginRequiredMixin ,View):
    def get(self, request, id):
        from_user = CustomUser.objects.get(id=id)
        for n in request.user.friendship_requests_to.all():
            if n.from_user == from_user:
                n.delete()
                return redirect("home_page")
            else:
                messages.warning(request, f"Пользователь {from_user.username} не отправлял вам запрос на дружбу !")
                return redirect(reverse("users:profile", kwargs={"id":from_user.id}))

class ConfirmFriendshipView(View):
    def get(self, request, id):
        from_user = CustomUser.objects.get(id=id)
        if request.user.is_authenticated:
            for n in request.user.friends_to.all():
                if n.from_user == from_user:
                    messages.warning(request, "Вы уже друзья !")
                    return redirect(reverse("users:profile", kwargs={"id":from_user.id}))
                    
            for n in request.user.friends_from.all():
                if n.to_user == from_user:
                    messages.warning(request, "Вы уже друзья !")
                    return redirect(reverse("users:profile", kwargs={"id":from_user.id}))
                
            for to in request.user.friendship_requests_to.all():
                if to.from_user == from_user:
                    for t in request.user.friendship_requests_to.all():
                        if t.from_user == from_user:
                            t.delete()
                    for t in request.user.friendship_requests_from.all():
                        if t.to_user == from_user:
                            t.delete()
                    Friendship.objects.create(from_user=from_user, to_user=request.user)
                    messages.success(request, f"Пользователь {from_user.username} теперь ваш друг !")
                    return redirect(reverse("users:profile", kwargs={"id":from_user.id}))
        messages.warning(request, f"Пользователь {from_user.username} не отправлял вам запрос на дружбу !")
        return redirect(reverse("users:profile", kwargs={"id":from_user.id}))


class FriendsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "friends/friends.html", {"user":request.user})
    
class ConfirmDeleteFriendshipView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)

        return render(request, "friends/confirm_delete_friend.html", {"user":user})

class DeleteFriendshipView(View):
    def get(self, request, id):
        user = CustomUser.objects.get(id=id)
        for t in request.user.friends_to.all():
            if t.from_user == user:
                t.delete()
        for t in request.user.friends_from.all():
            if t.to_user == user:
                t.delete()

        messages.success(request, "Удаление завершено успешно !")
        return redirect("home_page")