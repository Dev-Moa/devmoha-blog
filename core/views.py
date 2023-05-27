from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post,Author,Tag
from .forms import CommentForm
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
class IndexView(View):  
    def get(self,request):      
        post =  Post.objects.all()
        latest_post = post.order_by("-date")[:3]
        context = {
            "posts":latest_post,
            "date ":datetime.date
        }
        return render(request,"core/index.html",context)

class SignUpView(View):
    def get(self,request):
        form = UserCreationForm
        return render(request,"registration/signup.html",{"form":form})
    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        form = UserCreationForm
        return render(request,"registration/signup.html",{"form":form})
    

class AllPostsView(View):
    def get(self,request):
        posts = Post.objects.all()
        tag = Tag.objects.all()
        context = {
            "posts":posts,
            "tags":tag
        }
        return render(request,"core/all_posts.html",context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        post_id = post.id
        stored_posts = request.session.get('stored_posts')
        is_stored = False
        if stored_posts is not None:
            is_stored = post_id in stored_posts 
        tags = post.tags.all()
        form = CommentForm
        context = {
            "post":post,
            "tags":tags,
            "form":form, 
            "comments":post.comments.all().order_by("-id"),
            "is_stored":is_stored
        }
        return render(request,"core/post_detail.html",context)
    
    def post(self,request,slug):
        post = Post.objects.get(slug=slug)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        
        tags = post.tags.all()
        form = CommentForm
        context = {
            "post":post,
            "tags":tags,
            "form":form,
            "comments":post.comments.all().order_by("-id")
        }
        return render(request,"core/post_detail.html",context)


class AddFavoriteView(LoginRequiredMixin,View):
    def get(self,request):
        stored_posts = request.session.get('stored_posts')

        context = {}

        if stored_posts is None:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request,"core/fav_list.html",context)

    def post(self,request):
        stored_posts = request.session.get('stored_posts')
       
        if stored_posts is None:
            stored_posts = []

        post_id = request.POST["post_id"]

        if post_id not in stored_posts :
            stored_posts.append(int(post_id))
            request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse('favorites'))

class RemoveFavoriteView(LoginRequiredMixin,View):
    def get(self,request,id):
        post = Post.objects.get(id=id)
        return render(request,"core/remove-fav.html",{"post":post})

    def post(self,request,id):
        post = Post.objects.get(id=id)
        favorites = request.session.get("stored_posts")
        favorites.remove(post.id)
        request.session["stored_posts"] = favorites
        return HttpResponseRedirect(reverse("posts"))

class AuthorDetailView(View):
    def get(self,request,name):
        author = Author.objects.get(first_name=name)
        author_posts = author.posts.all()
        context = {
            "author":author,
            "posts":author_posts
        }
        return render(request,"core/author_detail.html",context)

class TagDetailView(View):
    def get(self,request,captions):
        tag = Tag.objects.get(captions=captions)
        tag_related_posts = tag.posts.all()
        context ={
            "tag":tag,
            "posts":tag_related_posts
        }
        return render(request,"core/tag_detail.html",context)



