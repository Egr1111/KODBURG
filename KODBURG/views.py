from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import *
from .forms import *
from django.views.generic import (
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    ListView,
    CreateView,
)

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.db.models import Count


# Create your views here


class Welcome(CreateView):
    form_class = UserCreateForm
    template_name = "KODBURG/welcome.html"
    success_url = reverse_lazy("enter")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = Post.objects.all()
        return context

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect("main_blog")

    # def form_invalid(self, form):
    #     error = "Форма заполнена неправильно!"
    #     return render(self.request, "KODBURG/welcome.html", {"object_list": Post.objects.all(), "error": error})


# def welcome(request):
#     model = Post.objects.all()
#     form_class = UserCreateForm


class Enter(LoginView):
    template_name = "KODBURG/enter.html"
    form_class = UserLoginForm
    success_url = "/kodburg/main_blog"


def main_blog(request):
    form_blog = Comments_to_blog()
    
    if request.method == "POST":
        form_blog = Comments_to_blog(request.POST, request.FILES)

        if form_blog.is_valid():
            form_blog = form_blog.save(commit=False)
            form_blog.author = request.user
            form_blog.save()
            return redirect("main_blog")
    return render(
        request,
        "KODBURG/main_blog.html",
        {
            "blog": Blog_list.objects.order_by("-date"),
            "comments_blog": Comment_blog.objects.order_by("-date"),
            "form_blog": form_blog,
        },
    )


def IncreaseCounterBlog(request, pk):
    if request.user in Blog_list.objects.get(id=pk).dislike.all():
        Blog_list.objects.get(id=pk).like.add(request.user)
        Blog_list.objects.get(id=pk).dislike.remove(request.user)
    else:
        Blog_list.objects.get(id=pk).like.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def DownCounterBlog(request, pk):
    Blog_list.objects.get(id=pk).like.remove(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def IncreaseCounterDisBlog(request, pk):
    if request.user in Blog_list.objects.get(id=pk).like.all():
        Blog_list.objects.get(id=pk).dislike.add(request.user)
        Blog_list.objects.get(id=pk).like.remove(request.user)
    else:
        Blog_list.objects.get(id=pk).dislike.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def DownCounterDisBlog(request, pk):
    Blog_list.objects.get(id=pk).dislike.remove(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def IncreaseCounterProject(request, pk):
    if request.user in Project_list.objects.get(id=pk).dislike.all():
        Project_list.objects.get(id=pk).like.add(request.user)
        Project_list.objects.get(id=pk).dislike.remove(request.user)
    else:
        Project_list.objects.get(id=pk).like.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def DownCounterProject(request, pk):
    Project_list.objects.get(id=pk).like.remove(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def IncreaseCounterDisProject(request, pk):
    if request.user in Project_list.objects.get(id=pk).like.all():
        Project_list.objects.get(id=pk).dislike.add(request.user)
        Project_list.objects.get(id=pk).like.remove(request.user)
    else:
        Project_list.objects.get(id=pk).dislike.add(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def DownCounterDisProject(request, pk):
    Project_list.objects.get(id=pk).dislike.remove(request.user)
    return redirect(request.META.get("HTTP_REFERER"))


def main_project(request):
    form_project = Comments_to_projects()

    if request.method == "POST":
        form_project = Comments_to_projects(request.POST, request.FILES)
        if form_project.is_valid():
            form_project = form_project.save(commit=False)
            form_project.author = request.user
            form_project.save()
            return redirect("main_project")

    return render(
        request,
        "KODBURG/main_project.html",
        {
            "projects": Project_list.objects.order_by("-date"),
            "comments_project": Comment_project.objects.order_by("-date"),
            "form_project": form_project,
        },
    )


class My_friends(TemplateView):
    template_name = "KODBURG/my_friends.html"

    def get(self, request, *args, **kwargs):
        return render(request, "KODBURG/my_friends.html", {})


class My_notice(TemplateView):
    template_name = "KODBURG/my_notice.html"


@login_required
def update_profile(request):
    error = ""

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect("main_blog")
        else:
            error = "Ошибка в заполнении формы"
    else:
        user_form = UserForm(instance=request.user)

    return render(
        request,
        "KODBURG/edit_profile.html",
        {
            "user_form": user_form,
            "error": error,
        },
    )


def my_blog(request):
    form = Comments_to_blog()
    if request.method == "POST":
        form = Comments_to_blog(request.POST, request.FILES)
        if form.is_valid:
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("my_blog")

    return render(
        request,
        "KODBURG/my_blog.html",
        {
            "object_list": Blog_list.objects.filter(username=request.user).order_by(
                "-date"
            ),
            "form": form,
            "comments": Comment_blog.objects.order_by("-date"),
        },
    )


def add_blog(request):
    error = ""
    form = Blog_form()
    if request.method == "POST":
        form = Blog_form(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = request.user
            form.save()
            return redirect("my_blog")
        else:
            error = "Форма заполнена неверно!"

    return render(
        request,
        "KODBURG/create_blog.html",
        {
            "form": form,
            "error": error,
        },
    )


class Update_blog(UpdateView):
    model = Blog_list
    form_class = Blog_form
    template_name = "KODBURG/change_blog.html"
    success_url = reverse_lazy("my_blog")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notice"] = Notice.objects.filter(
            usernameTo=self.request.user
        ).order_by("-date")[:3]
        context["Users"] = User.objects.all()
        context["new_notice"] = Notice.objects.filter(
            usernameTo=self.request.user, read=False
        ).order_by("-date")
        return context


class Delete_blog(DeleteView):
    model = Blog_list
    context_object_name = "Blog_list"
    template_name = "KODBURG/delete_blog.html"
    success_url = reverse_lazy("my_blog")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notice"] = Notice.objects.filter(
            usernameTo=self.request.user
        ).order_by("-date")[:3]
        context["Users"] = User.objects.all()
        context["new_notice"] = Notice.objects.filter(
            usernameTo=self.request.user, read=False
        ).order_by("-date")
        return context


def my_project(request):
    form = Comments_to_projects()
    if request.method == "POST":
        form = Comments_to_projects(request.POST, request.FILES)
        if form.is_valid:
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect("my_projects")

    return render(
        request,
        "KODBURG/my_project.html",
        {
            "object_list": Project_list.objects.filter(username=request.user).order_by(
                "-date"
            ),
            "form": form,
            "comments": Comment_project.objects.order_by("-date"),
        },
    )


def add_project(request):
    error = ""
    form = Project_form()
    if request.method == "POST":
        form = Project_form(request.POST, request.FILES)
        if form.is_valid:
            form = form.save(commit=False)
            form.username = request.user
            form.save()
            return redirect("my_projects")
        else:
            error = "Форма заполнена неверно!"

    return render(
        request,
        "KODBURG/create_project.html",
        {
            "form": form,
            "error": error,
        },
    )


class Update_project(UpdateView):
    model = Project_list
    form_class = Project_form
    template_name = "KODBURG/change_project.html"
    success_url = reverse_lazy("my_projects")

    def get_context_data(self, **kwargs):
        error = ""
        context = super().get_context_data(**kwargs)
        context["notice"] = Notice.objects.filter(
            usernameTo=self.request.user
        ).order_by("-date")[:3]
        context["Users"] = User.objects.all()
        context["error"] = error
        context["new_notice"] = Notice.objects.filter(
            usernameTo=self.request.user, read=False
        ).order_by("-date")
        return context


class Delete_project(DeleteView):
    model = Project_list
    context_object_name = "Project_list"
    template_name = "KODBURG/delete_project.html"
    success_url = "/kodburg/main/my_projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notice"] = Notice.objects.filter(
            usernameTo=self.request.user
        ).order_by("date")[:3]
        context["Users"] = User.objects.all()
        context["new_notice"] = Notice.objects.filter(
            usernameTo=self.request.user, read=False
        ).order_by("-date")
        return context


class Reach(ListView):
    model = User
    template_name = "KODBURG/reach.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notice"] = Notice.objects.filter(
            usernameTo=self.request.user
        ).order_by("-date")[:3]
        context["Users"] = User.objects.all()
        context["friends"] = self.request.user.friends
        context["new_notice"] = Notice.objects.filter(
            usernameTo=self.request.user, read=False
        ).order_by("-date")
        return context


@login_required
def other_user(request, username, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    object = Notice.objects.filter(usernameFrom=to_user, usernameTo=from_user)
    connection_from = Requests.objects.filter(user_from=from_user, user_to=to_user)
    connections_to = Requests.objects.filter(user_from=to_user, user_to=from_user)

    if object:
        if len(object) > 1:
            for i in range(len(object)):
                object_get = Notice.objects.filter(
                    usernameFrom=to_user, usernameTo=from_user
                )[i]
                object_get.read = True
                object_get.save()

        else:
            object_get = Notice.objects.get(usernameFrom=to_user, usernameTo=from_user)
            object_get.read = True
            object_get.save()

    if connection_from:
        connection = {"user_from": from_user.id, "user_to": userID}
    elif connections_to:
        connection = {"user_from": userID, "user_to": from_user.id}
    else:
        Requests.objects.create(user_from=from_user, user_to=to_user)
        new_connect = Requests.objects.get(user_from=from_user, user_to=to_user)
        from_user.connections.add(new_connect)
        to_user.connections.add(new_connect)
        connection = {"user_from": from_user.id, "user_to": userID}

    return render(
        request,
        "KODBURG/other_user.html",
        {
            "notices": Notice.objects.filter(usernameTo=request.user).order_by("-date")[
                :3
            ],
            "projects": Project_list.objects.filter(username=to_user).order_by("-date"),
            "blog": Blog_list.objects.filter(username=to_user).order_by("-date"),
            "fri_reqFrom": Friends_request.objects.filter(
                from_user=from_user, to_user=to_user
            ),
            "fri_reqTo": Friends_request.objects.filter(
                from_user=to_user, to_user=from_user
            ),
            "friends": request.user.friends,
            "room_to": Room.objects.filter(
                title=f"{from_user.username}.{to_user.username}"
            ),
            "room_from": Room.objects.filter(
                title=f"{to_user.username}.{from_user.username}"
            ),
            "other_user": to_user,
            "connection": connection,
        },
    )


def chat(request, user_from, user_to):
    

    my_id = request.user.pk
    print(user_from, user_to)
    user1 = User.objects.get(pk=user_from)
    user2 = User.objects.get(pk=user_to)
    print(f"{user1.username}.{user2.username}")

    if Messages.objects.filter(
        room=Room.objects.get(title=f"{user1.username}.{user2.username}"), viewed=False
    ).first:
        non_viewed = Messages.objects.filter(
            room=Room.objects.get(title=f"{user1.username}.{user2.username}"),
            viewed=False,
        ).first
        print(non_viewed, "Все работает!")
    else:
        non_viewed = ""
        print(user1.pk)
    if Messages.objects.filter(
        room=Room.objects.get(title=f"{user1.username}.{user2.username}")
    ):
        list = {}
        item = ""
        for i in Messages.objects.filter(
            room=Room.objects.get(title=f"{user1.username}.{user2.username}")
        ).order_by("time_send"):
            if item != i.time_send.date():
                item = i.time_send.date()
                print(item)
                list[item] = Messages.objects.filter(
                    room=Room.objects.get(title=f"{user1.username}.{user2.username}"),
                    time_send=i.time_send,
                ).first
        print(list)
    else:
        list = {}

    return render(
        request,
        "KODBURG/chat.html",
        {
            "room_name": f"{user1.username}.{user2.username}",
            "room_id": Room.objects.get(title=f"{user1.username}.{user2.username}").pk,
            "messages": Messages.objects.filter(
                room=Room.objects.get(title=f"{user1.username}.{user2.username}")
            ),
            "User": user1,
            "friends": request.user.friends,
            "non_viewed": non_viewed,
            "User1": user1,
            "User2": user2,
            "date": list,
        },
    )


def create_chat(request, user_from, user_to):
    user1 = User.objects.get(pk=user_from)
    user2 = User.objects.get(pk=user_to)
    if Room.objects.filter(title=f"{user1.username}.{user2.username}"):
        return redirect(f"/kodburg/main/chat/{user_from}{user_to}/")
    elif Room.objects.filter(title=f"{user2.username}.{user1.username}"):
        return redirect(f"/kodburg/main/chat/{user_to}{user_from}/")
    else:
        Room.objects.create(title=f"{user1.username}.{user2.username}")
        new_room = Room.objects.get(title=f"{user1.username}.{user2.username}")

        user1.chats.add(new_room)
        user2.chats.add(new_room)

        return redirect(f"/kodburg/main/chat/{user_from}{user_to}/")


def messager(request):
    Users = User.objects.all()
    rooms = Room.objects.all().order_by("time_create")
    notice = Notice.objects.filter(usernameTo=request.user).order_by("-date")[:3]
    
    list = {}
    for i in rooms:
        if request.user.username in i.title:
            print(i.title)
            if len(Messages.objects.filter(room=i)) > 0:
                print(">0")
                for item in User.objects.all():
                    if (
                        item != request.user
                        and item.username in i.title
                        and len(Messages.objects.filter(room=i)) > 1
                    ):
                        print(i.title, ">1")
                        if request.user.username + "." + item.username == i.title:
                            print(">1.1")
                            list[i.title] = {
                                "user_from": request.user,
                                "user_to": item,
                                "last_message": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ],
                                "viewed": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ].viewed,
                                "time_send": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ].time_send,
                            }
                        elif item.username + "." + request.user.username == i.title:
                            print(">1.2")
                            list[i.title] = {
                                "user_from": item,
                                "user_to": request.user,
                                "last_message": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ],
                                "viewed": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ].viewed,
                                "time_send": Messages.objects.filter(room=i)[
                                    len(Messages.objects.filter(room=i)) - 1
                                ].time_send,
                            }
                    elif (
                        item != request.user
                        and item.username in i.title
                        and len(Messages.objects.filter(room=i)) == 1
                    ):
                        print(i.title, "=1")
                        if request.user.username + "." + item.username == i.title:
                            print("=1.1")
                            list[i.title] = {
                                "user_from": request.user,
                                "user_to": item,
                                "last_message": Messages.objects.get(room=i),
                                "viewed": Messages.objects.get(room=i).viewed,
                                "time_send": Messages.objects.get(room=i).time_send,
                            }
                        elif item.username + "." + request.user.username == i.title:
                            print("=1.2")
                            list[i.title] = {
                                "user_from": item,
                                "user_to": request.user,
                                "last_message": Messages.objects.get(room=i),
                                "viewed": Messages.objects.get(room=i).viewed,
                                "time_send": Messages.objects.get(room=i).time_send,
                            }
            else:
                print("=0")
                for item in User.objects.all():
                    if item != request.user and item.username in i.title:
                        if request.user.username + "." + item.username == i.title:
                            print("=0.1")
                            list[i.title] = {
                                "user_from": request.user,
                                "user_to": item,
                                "last_message": "Напишите свое первое сообщение!",
                                "viewed": True,
                                "time_send": Room.objects.get(title=i).time_create,
                            }
                        elif item.username + "." + request.user.username == i.title:
                            print("=0.2")
                            list[i.title] = {
                                "user_from": item,
                                "user_to": request.user,
                                "last_message": "Напишите свое первое сообщение!",
                                "viewed": True,
                                "time_send": Room.objects.get(title=i).time_create,
                            }

    return render(
        request,
        "KODBURG/messager.html",
        {
            "chats": list,
            "Users": Users,
            "notice": notice,
        },
    )