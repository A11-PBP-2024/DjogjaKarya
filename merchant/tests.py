from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Store

class StoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.normal_user = User.objects.create_user(username='user', password='password')
        self.store = Store.objects.create(
            name='Test Store',
            description='A store for testing',
            address='123 Test St',
            opening_days='Mon-Fri',
            opening_hours='9am-5pm',
            phone='123456789',
            image1='http://image1.jpg',
            image2='http://image2.jpg',
            image3='http://image3.jpg',
            location_link='http://example.com'
        )

    def test_store_list_view_admin(self):
        self.client.login(username='admin', password='password') 
        response = self.client.get(reverse('merchant:store_list'))
        self.assertEqual(response.status_code, 200)

    def test_get_stores_view_admin(self):
        self.client.login(username='admin', password='password') 
        response = self.client.get(reverse('merchant:get_stores'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Store')

    def test_add_store_view_as_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('merchant:add_store'), {
            'name': 'New Store',
            'description': 'A new store',
            'address': '456 New St',
            'opening_days': 'Sat-Sun',
            'opening_hours': '10am-6pm',
            'phone': '987654321',
            'image1': 'http://image1.jpg',
            'image2': 'http://image2.jpg',
            'image3': 'http://image3.jpg',
            'location_link': 'http://newstore.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Store.objects.filter(name='New Store').exists())

    def test_edit_store_view_as_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('merchant:edit_store', args=[self.store.id]), {
            'name': 'Updated Store',
            'description': 'Updated description',
            'address': '123 Updated St',
            'opening_days': 'Mon-Sun',
            'opening_hours': '10am-8pm',
            'phone': '111222333',
            'image1': 'http://image1.jpg',
            'image2': 'http://image2.jpg',
            'image3': 'http://image3.jpg',
            'location_link': 'http://updatedstore.com'
        })
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, 'Updated Store')

    def test_delete_store_view_as_admin(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('merchant:delete_store', args=[self.store.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Store.objects.filter(id=self.store.id).exists())

    def test_store_products_view(self):
        response = self.client.get(reverse('merchant:store_products'), {'toko': self.store.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.store.name)