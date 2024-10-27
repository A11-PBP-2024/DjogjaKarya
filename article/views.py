from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article
from .forms import ArticleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Article
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Helper function to check if the user is a superuser
def superuser_required(user):
    return user.is_superuser


def article_list(request):
    articles = Article.objects.all()  # Fetch all articles
    return render(request, 'blog.html', {'articles': articles})

def show_article(request):
    all_articles = Article.objects.all()

    # Filter articles based on Djogjakarya-specific categories
    art_articles = Article.objects.filter(tags__icontains="art")
    heritage_articles = Article.objects.filter(tags__icontains="heritage")
    culture_articles = Article.objects.filter(tags__icontains="culture")
    craft_articles = Article.objects.filter(tags__icontains="craft")
    travel_articles = Article.objects.filter(tags__icontains="travel")

    context = {
        'name': request.user.username,
        'articles': all_articles,
        # Djogjakarya-specific categories
        'artArticles': art_articles,
        'heritageArticles': heritage_articles,
        'cultureArticles': culture_articles,
        'craftArticles': craft_articles,
        'travelArticles': travel_articles,
    }

    return render(request, "blog.html", context)


def detail_blog(request, id):
    article = get_object_or_404(Article, id=id)
    related_articles = Article.objects.exclude(id=id)[:5]  # Adjust the number as needed
    # Adjusting for a CharField of comma-separated tags
    tags = article.tags.split(',')

    return render(request, 'detail_blog.html', {
        'article': article,
        'related_articles': related_articles,
        'tags': tags,
    })




#@user_passes_test(superuser_required)

@csrf_exempt
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # This will now automatically set the publication_date to today's date in UTC+7
            # Redirect to a success page or wherever you need
            return redirect('success_url')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            # Redirect to the article detail page
            return redirect('article:detail_blog', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})


def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('article:show_article')  # Redirect to the article list
    return render(request, 'confirm_delete.html', {'article': article})
