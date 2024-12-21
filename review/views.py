from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.db.models import Avg


@csrf_exempt
def add_review(request, product_id):
    """
    Handles adding a review for a specific product.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
            comment = request.POST.get('comment')

            # Validation: Ensure rating is between 1 and 5, and comment is not empty
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
            elif not comment.strip():
                messages.error(request, "Comment cannot be empty.")
            else:
                # Create the review
                Review.objects.create(product=product, rating=rating, comment=comment)
                messages.success(request, "Your review has been submitted successfully.")
                return redirect(reverse('review:review_list', args=[product.id]))
        except ValueError:
            messages.error(request, "Invalid rating. Please enter a number between 1 and 5.")

    return render(request, 'add_review.html', {'product': product})


def review_list(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    total_reviews = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    star_summary = []
    for star in range(5, 0, -1):
        star_count = reviews.filter(rating=star).count()
        percentage = (star_count / total_reviews * 100) if total_reviews > 0 else 0
        star_summary.append({'star': star, 'count': star_count, 'percentage': percentage})

    # Add fractional part calculation
    fractional_part = average_rating - int(average_rating)

    context = {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
        'star_summary': star_summary,
        'rating_range': range(1, 6),  # Range untuk bintang 1-5
        'fractional_part': int(fractional_part * 100),  # Convert to percentage
    }
    return render(request, 'review_list.html', context)

