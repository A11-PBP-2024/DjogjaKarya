from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Review
from product.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.db.models import Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def delete_review(request, product_id, review_id):
    """
    Web endpoint for deleting a review (admin only)
    """
    if request.method == 'POST':
        try:
            review = get_object_or_404(Review, id=review_id)
            review.delete()
            messages.success(request, "Review has been deleted successfully.")
            return redirect('review:review_list', product_id=product_id)
        except Review.DoesNotExist:
            messages.error(request, "Review not found.")
        return redirect('review:review_list', product_id=product_id)
    return HttpResponseForbidden()

@api_view(['GET'])
def get_reviews(request):
    """
    API endpoint to get reviews, can filter by product_id
    """
    product_id = request.query_params.get('product_id')
    if product_id:
        reviews = Review.objects.filter(product_id=product_id)
    else:
        reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_review_api(request):
    """
    API endpoint to add a review
    """
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@csrf_exempt
@login_required
def add_review(request, product_id):
    """
    Web endpoint for adding a review for a specific product
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
                Review.objects.create(
                    product=product, 
                    rating=rating, 
                    comment=comment,
                )
                messages.success(request, "Your review has been submitted successfully.")
                return redirect(reverse('review:review_list', args=[product.id]))
        except ValueError:
            messages.error(request, "Invalid rating. Please enter a number between 1 and 5.")

    return render(request, 'add_review.html', {'product': product})

@login_required
def review_list(request, product_id):
    """
    Web endpoint to display list of reviews for a specific product
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    total_reviews = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    star_summary = []
    for star in range(5, 0, -1):
        star_count = reviews.filter(rating=star).count()
        percentage = (star_count / total_reviews * 100) if total_reviews > 0 else 0
        star_summary.append({
            'star': star, 
            'count': star_count, 
            'percentage': percentage
        })

    # Add fractional part calculation
    fractional_part = average_rating - int(average_rating)

    context = {
        'product': product,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
        'star_summary': star_summary,
        'rating_range': range(1, 6),  # Range for stars 1-5
        'fractional_part': int(fractional_part * 100),  # Convert to percentage
    }
    return render(request, 'review_list.html', context)

# API Endpoint untuk delete review
@csrf_exempt
@api_view(['DELETE'])
@user_passes_test(is_admin)
def delete_review_api(request, review_id):
    """
    API endpoint untuk menghapus review (admin only)
    """
    try:
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=200)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)