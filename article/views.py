from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from article.forms import CommentForm
from .models import Article

# View for showing a single article by id

def show_article(request):
    return render(request, 'blog.html')
# Function to check if user is admin


def blog_detail(request):
    return render(request, 'detail_blog.html')


def is_admin(user):
    # Only allow superuser (admin) to access certain views
    return user.is_superuser

# View for creating a new article (admin only)

def submit_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()  # Save the comment to the database
        # Redirect to the article detail page (use the correct view name)
        return redirect('article_detail')
    # Redirect back in case of form errors (adjust as needed)
    return redirect('article_detail')

@login_required
@user_passes_test(is_admin)
def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        content = request.POST.get('content')
        publication_date = request.POST.get('publication_date')
        image = request.POST.get('image')
        tags = request.POST.get('tags')

        Article.objects.create(
            title=title,
            author=author,
            description=description,
            content=content,
            publication_date=publication_date,
            image=image,
            tags=tags
        )
        return redirect('article_list')

    return render(request, 'articles/article_form.html')

# View for updating an existing article (admin only)


@login_required
@user_passes_test(is_admin)
def article_update(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.author = request.POST.get('author')
        article.description = request.POST.get('description')
        article.content = request.POST.get('content')
        article.publication_date = request.POST.get('publication_date')
        article.image = request.POST.get('image')
        article.tags = request.POST.get('tags')
        article.save()

        return redirect('article_detail', article_id=article.id)

    return render(request, 'articles/article_form.html', {'article': article})

# View for deleting an article (admin only)


@login_required
@user_passes_test(is_admin)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'articles/article_confirm_delete.html', {'article': article})
