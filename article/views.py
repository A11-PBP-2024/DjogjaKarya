from django.shortcuts import render
from .models import Article

# Create your views here.
def show_article(request):
    # Fetch all articles from the database
    all_articles = Article.objects.all()

    # Example of filtering articles based on tags or content categories
    technology_articles = Article.objects.filter(tags__icontains="technology")
    science_articles = Article.objects.filter(tags__icontains="science")
    politics_articles = Article.objects.filter(tags__icontains="politics")
    health_articles = Article.objects.filter(tags__icontains="health")
    sports_articles = Article.objects.filter(tags__icontains="sports")

    # Preparing context data to be sent to the template
    context = {
        'name': request.user.username,  # User's username for personalization
        'articles': all_articles,  # All articles
        'technologyArticles': technology_articles,
        'scienceArticles': science_articles,
        'politicsArticles': politics_articles,
        'healthArticles': health_articles,
        'sportsArticles': sports_articles,
    }

    # Rendering the template with the context
    return render(request, "blog.html", context)
