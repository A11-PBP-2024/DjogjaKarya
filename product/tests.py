from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product, Category
from merchant.models import Store
from unittest.mock import patch
import json

class ProductViewsTest(TestCase):
    """Test suite for Product views"""

    def setUp(self):
        """Set up test data before each test method"""
        self.client = Client()
        
        #user
        self.admin_user = User.objects.create_superuser(
            username='admin', password='adminpassword', email='admin@test.com'
        )
        self.normal_user = User.objects.create_user(
            username='user', password='userpassword', email='user@test.com'
        )
        
        #dummy
        self.store = Store.objects.create(name='Test Store')
        self.product = Product.objects.create(
            name='Test Product',
            kategori='Batik',
            harga=100000,
            toko='Test Store',
            image='image.jpg'
        )
        self.category = Category.objects.create(
            name='Test Category',
            products=self.product,
            is_wishlist=False
        )

        #dummy
        self.product_data = {
            'name': 'New Product',
            'kategori': 'Batik',
            'harga': 200000,
            'toko': 'Test Store',
            'image': 'new_image.jpg'
        }

    def test_authentication_required_views(self):
        """Test views that require authentication"""
        protected_urls = [
            ('product:add_product', []),
            ('product:edit_product', [self.product.id]),
            ('product:delete_product', [self.product.id]),
            ('product:show_category', []),
            ('product:show_detail', [self.product.id])
        ]

        for url_name, args in protected_urls:
           
            response = self.client.get(reverse(url_name, args=args))
            self.assertEqual(response.status_code, 302)  

    def test_admin_only_views(self):
        """Test views that require admin privileges"""
        admin_urls = [
            ('product:add_product', 'post', self.product_data),
            ('product:edit_product', 'post', self.product_data),
            ('product:delete_product', 'post', {}),
            ('product:get_form_data', 'get', {})
        ]

        for url_name, method, data in admin_urls:
           
            self.client.login(username='user', password='userpassword')
            url = reverse(url_name) if not method == 'post' else reverse(url_name, args=[self.product.id] if 'edit' in url_name or 'delete' in url_name else [])
            
            if method == 'get':
                response = self.client.get(url)
            else:
                response = self.client.post(url, data)
            
           
            self.assertEqual(response.status_code, 302)
            
          
            self.client.logout()
            self.client.login(username='admin', password='adminpassword')
            
            if method == 'get':
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
            else:
                response = self.client.post(url, data)
                self.assertIn(response.status_code, [200, 201])

    def test_product_crud_operations(self):
        """Test Create, Read, Update, Delete operations for products"""
        self.client.login(username='admin', password='adminpassword')

        
        response = self.client.post(reverse('product:add_product'), self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

        
        response = self.client.get(reverse('product:get_product_id', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['name'], 'Test Product')

       
        update_data = self.product_data.copy()
        update_data['name'] = 'Updated Product'
        response = self.client.post(
            reverse('product:edit_product', args=[self.product.id]),
            update_data
        )
        self.assertEqual(response.status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

       
        response = self.client.post(reverse('product:delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_edge_cases_and_validation(self):
        """Test edge cases and validation scenarios"""
        self.client.login(username='admin', password='adminpassword')

        
        invalid_data = self.product_data.copy()
        del invalid_data['name']
        response = self.client.post(reverse('product:add_product'), invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Field name is required', response.json()['error'])

        non_existent_id = 999

        response = self.client.get(reverse('product:get_product_id', args=[non_existent_id]))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Produk tidak ditemukan!')

        response = self.client.post(
            reverse('product:edit_product', args=[non_existent_id]),
            self.product_data
        )
        self.assertEqual(response.status_code, 500)

        response = self.client.post(reverse('product:delete_product', args=[non_existent_id]))
        self.assertEqual(response.status_code, 500)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)

    def test_category_filtering(self):
        response = self.client.get(reverse('product:filter-category-ajax'), {'kategori': 'all'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('kainBatik', data)

        response = self.client.get(reverse('product:filter-category-ajax'), {'kategori': 'Batik'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('products', data)
        self.assertTrue(isinstance(data['products'], list))

    def test_error_handling(self):
        self.client.login(username='admin', password='adminpassword')

        with patch('product.views.Store.objects.values_list', side_effect=Exception('Database error')):
            response = self.client.get(reverse('product:get_form_data'))
            self.assertEqual(response.status_code, 500)
            self.assertIn('error', response.json())

        response = self.client.get(reverse('product:add_product'))
        self.assertEqual(response.status_code, 405)

    def test_show_category_view_all_categories(self):
        self.client.login(username='user', password='userpassword')
        response = self.client.get(reverse('product:show_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')

        expected_categories = [
            'kainBatik', 'kerajinanKulit', 'kerajinanPerak', 'kerajinanWayang',
            'kerajinanKayu', 'kerajinanAnyaman', 'kerajinanGerabah',
            'kerajinanBambu', 'kerajinanTenun'
        ]
        for category in expected_categories:
            self.assertIn(category, response.context)
        self.assertEqual(response.context['selected_kategori'], 'all')