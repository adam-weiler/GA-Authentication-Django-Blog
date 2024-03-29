# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse


from blog.models import Article, Topic, Comment
from blog.forms import ArticleForm, CommentForm


def index(request): # Redirects to http://localhost:8000/articles
    return redirect(reverse("show_all"))


def show_all(request):  # Renders a list of all articles.
    context = { 'blog_articles': Article.objects.all().order_by('-published_date'), 'blog_topics': Topic.objects.all() } #The - in published_date means order from newest to oldest.
    return render(request, "articles.html", context)


def show_article(request, article_id):  # Renders a single article.
    article = Article.objects.get(pk=article_id)
    form = CommentForm()

    return render(request, 'article.html', {
        'article': article, 
        'form': form
    })


@login_required
def new_article(request):  # Renders a form to create a new article.
    form = ArticleForm()

    return render(request, 'article_form.html', {
        'form': form
    })


@login_required
def create_article(request):  # User creating a new article.
    form = ArticleForm(request.POST)

    if form.is_valid():
        # form.save()
        new_article = form.save(commit=False)
        new_article.user = request.user
        new_article.save()

        return redirect(reverse('show_all'))
    else:  # Else sends user back to article_form page.
        return render(request, 'article_form.html', {
            'form': form
        })
        # return redirect(reverse('new_article')) #How do you reverse and attach a form..?


def create_comment(request, article_id):  # Renders a form to create a new comment.
    article = Article.objects.get(pk=article_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return redirect(reverse('show_article', args=[article_id]))
    else:  # Else sends user back to article page.
        return render(request, 'article.html', {
            'article': article, 
            'form': form
        })


def signup(request):  # Renders a form for a new user to signup.
    form = UserCreationForm()
    # context = { 'form': form }
    return render(request, 'registration/signup.html', {
        'form': form
    })


def signup_create(request):  # Creates a new user if request is valid.
    form = UserCreationForm(request.POST)

    if form.is_valid():
        new_user = form.save()
        login(request, new_user)
        return redirect(reverse("show_all"))
    else:  # Else sends user back to signup page.
        return render(request, 'registration/signup.html', {
            'form': form
        })


def login_view(request):  # Logins in user if request is valid.
    if request.user.is_autheticated:
        return redirect(reverse('user_profile'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    form.add_error('username', 'This account has been disabled.')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    })
    

        



def logout_view(request):
    logout(request)
    return redirect(reverse("show_all"))
    