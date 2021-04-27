from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from . forms import UserRegisterForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'index.html'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'posts.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'edit_post.html'
    fields = ['title', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'account/createuser.html'
    success_url = reverse_lazy('index')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class LoginView(View):
    def log_in(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/user')

            else:
                return HttpResponse("Inactive User")

        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
