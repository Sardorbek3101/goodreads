from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from posts.models import Posts, PostComments
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostCommentsForm

class PostsView(View):
    def get(self, request):
        comment = None
        post = None
        com_form = PostCommentsForm()
        posts = Posts.objects.all().order_by('-created_at')
        update_com_id = request.GET.get("update_comm", "")
        if update_com_id:
            try:
                comm = PostComments.objects.get(id=update_com_id)
                com_form = PostCommentsForm(instance=comm)
            except:
                messages.warning(request, "По вашему запросу не найдено комметарий !")
                return redirect('landing_page')
            if not comm.user == request.user:
                messages.warning(request, "Вам не разрешено изменять чужие сообщения !")
                return redirect('landing_page')
        del_com = request.GET.get("delete_comm", 0)
        if del_com:
            try:
                comm = PostComments.objects.get(id=del_com)
            except:
                messages.warning(request, "По вашему запросу не найдено комметарий !")
                return redirect('landing_page')
            if not comm.user == request.user:
                messages.warning(request, "Вам не разрешено удалять чужие сообщения !")
                return redirect('landing_page')
        post_id = request.GET.get("comments", "")
        if post_id:
            post = Posts.objects.get(id = post_id)
            comment = post.postcomments_set.all()
        return render(request, "landing.html", {"posts": posts, "comments":comment, "com_post":post, "form":com_form, "del_com":int(del_com)})
    
    def post(self, request):
        update_com_id = request.GET.get("update_comm", "")
        if request.user.is_authenticated:
            if update_com_id:
                try:
                    post_com = PostComments.objects.get(id=update_com_id)
                    com_form = PostCommentsForm(instance=post_com, data=request.POST)
                except:
                    messages.warning(request, "По вашему запросу не найдено комметарий !")
                    return redirect('landing_page')
                if post_com.user == request.user:
                    if com_form.is_valid():
                        com_form.save()
                        messages.success(request, "Изменения внесены успешно !")
                        return redirect("landing_page")
                    else:
                        messages.warning(request, "Произошла ошибка")
                        return redirect("landing_page")
                else:
                    messages.warning(request, "Вам не разрешено изменять чужие сооющения !")
                    return redirect('landing_page')
            form = PostCommentsForm(data=request.POST)
            post_id = request.GET.get("comments", "")
            if post_id:
                try:
                    post = Posts.objects.get(id=post_id)
                except:
                    messages.warning(request, "По вашему запросу не найдено постов !")
                    return redirect('landing_page')
            else:
                messages.warning(request, "По вашему запросу не найдено постов !")
                return redirect('landing_page')
            if form.is_valid():
                PostComments.objects.create(user=request.user, comment=form.cleaned_data['comment'], post=post)
                messages.success(request, "Комментарий успешно отправлен")
                return redirect('landing_page')
            else:
                messages.warning(request, "При отправки комментария произошла ошибка")
                return redirect('landing_page')
        else:
            return redirect('users:login')



class DeletePostCommentView(LoginRequiredMixin ,View):
    def post(self, request):
        try:
            comment = PostComments.objects.get(id=request.POST['com_id'])
        except:
            messages.warning(request, "По вашему запросу комментарий не найдено !")
            return redirect('landing_page')
        if request.user == comment.user:
            comment.delete()
            messages.success(request,"Комментарий удалён успешно !")
            return redirect('landing_page')
        messages.warning(request, "Вам не разрешено удалять чужие сообщения !")
        return redirect('landing_page')
    


class LikeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            post = Posts.objects.get(id = request.POST['post'])
        except:
            messages.warning(request, "По вашему запросу постов не найдено !")
            return redirect('landing_page')
        if not request.user in post.likes.all():
            post.likes.add(request.user)
            post.save()
            return redirect('landing_page')
        messages.warning(request, "Вы уже лайкали этот пост")
        return redirect('landing_page')


class DeleteLikeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            post = Posts.objects.get(id = request.POST['post'])
        except:
            messages.warning(request, "По вашему запросу постов не найдено !")
            return redirect('landing_page')
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            post.save()
            return redirect('landing_page')
        messages.warning(request, "Вы ещё не лайкали этот пост")
        return redirect('landing_page')


# class LikeView(LoginRequiredMixin, View):
#     def post(self, request):
#         post = Posts.objects.get(id = request.POST['post'])
#         Like.objects.create(user=request.user, post=post)
#         return redirect('landing_page')
    

# class DeleteLikeView(LoginRequiredMixin, View):
#     def post(self, request):
#         post = Posts.objects.get(id = request.POST['post'])
#         try:
#             like = Like.objects.get(user=request.user, post=post)
#         except:
#             messages.warning(request, "Вы ещё не лайкали этот пост")
#             return redirect('landing_page')
#         like.delete()
#         return redirect('landing_page')
    