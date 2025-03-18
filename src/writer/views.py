from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import aget_user
from common.auth import awriter_required, ensure_for_current_user
from common.django_utils import arender
from django.shortcuts import redirect
from .forms import ArticleForm, UpdateUserForm
from .models import Article
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

@awriter_required
async def dashboard(request: HttpRequest) -> HttpResponse:
        return await arender(request, 'writer/dashboard.html')

@awriter_required
async def create_article(request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if await form.ais_valid():
                article = await form.asave(commit = False)
                article.user = await aget_user(request)
                await article.asave()
                return redirect('my-articles')
        else:
                form = ArticleForm()
                
        context = {'create_article_form': form}
        return await arender(request, 'writer/create-article.html', context)

@awriter_required
async def my_articles(request: HttpRequest) -> HttpResponse:
        current_user = await aget_user(request)
        articles = Article.objects.filter(user=current_user) 
        context = {'articles': articles}
        return await arender(request, 'writer/my-article.html', context)

@awriter_required
@ensure_for_current_user(Article, redirect_if_missing = 'my-articles')
async def  update_articles(request: HttpRequest, article: Article) -> HttpResponse:
        if request.method == 'POST':
                form = ArticleForm(request.POST, instance=article) 
                if await form.ais_valid():
                        await form.asave()
                        return redirect('my-articles')
        else:
                        form = ArticleForm(instance=article)
        context = {'update_article_form': form}
        return await arender(request, 'writer/update-article.html', context)

@awriter_required
@ensure_for_current_user(Article, redirect_if_missing = 'my-articles')
async def  delete_article(request: HttpRequest, article: Article) -> HttpResponse:
        if request.method == 'POST':
                await article.adelete()
                return redirect('my-articles')
        
        context = {'article': article}
        return await arender(request, 'writer/delete-article.html', context)

@awriter_required
async def  update_user(request: HttpRequest) -> HttpResponse:
        user = await aget_user(request)
        if request.method == 'POST':
                form = UpdateUserForm(request.POST, instance=user)
                if await form.ais_valid():
                        await form.asave()
                        return redirect('writer-dashboard')
        else:
                form = UpdateUserForm(instance=user)
        context = {'update_user_form': form}
        return await arender(request, 'writer/update-user.html', context)

@awriter_required
async def  delete_user(request: HttpRequest) -> HttpResponse:
        user = await aget_user(request)
        if request.method == 'POST':
                await user.adelete()
                return redirect('home')
        context = {'user': user}
        return await arender(request, 'writer/delete-user.html', context)



