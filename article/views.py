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

def is_admin(user):
    return user.is_superuser


def article_list(request):
    articles = Article.objects.all()  # Fetch all articles
    return render(request, 'blog.html', {'articles': articles})


def show_article(request):
    # Get the tag parameter from the URL
    tag = request.GET.get('tag', None)

    # Fetch all articles
    all_articles = Article.objects.all()

    # Filter articles based on the provided tag if it exists
    if tag:
        articles = Article.objects.filter(tags__icontains=tag)
    else:
        articles = all_articles

    # Optional: Fetch articles for specific tags if needed (this can be omitted if not used)
    art_articles = Article.objects.filter(tags__icontains="art")
    heritage_articles = Article.objects.filter(tags__icontains="heritage")
    culture_articles = Article.objects.filter(tags__icontains="culture")
    craft_articles = Article.objects.filter(tags__icontains="craft")
    travel_articles = Article.objects.filter(tags__icontains="travel")

    context = {
        'name': request.user.username,
        'articles': articles,  # Use the filtered articles here
        # Djogjakarya-specific categories (optional)
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
@login_required
@user_passes_test(is_admin)
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()  # Save the article instance
            # Prepare response data
            response_data = {
                'id': article.id,
                'title': article.title,
                'description': article.description,
                'image': article.image if article.image else None,  # Handle if there's no image
                # Handle category
                'tags': article.tags if article.tags else 'Uncategorized',
                'author': article.author if article.author else 'Unknown',  # Handle author
                # Format date as needed
                'publication_date': article.publication_date.strftime('%Y-%m-%d'),
            }
            # Return JSON response with article data
            return JsonResponse(response_data)
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})


@csrf_exempt
@login_required
@user_passes_test(is_admin)
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.description = request.POST.get('description')
        article.content = request.POST.get('content')
        article.save()

        response_data = {
            'title': article.title,
            'description': article.description,
            'content': article.content,
        }
        return JsonResponse(response_data)


@csrf_exempt
@login_required
@user_passes_test(is_admin)
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('article:show_article')  # Redirect to the article list
    return render(request, 'confirm_delete.html', {'article': article})
