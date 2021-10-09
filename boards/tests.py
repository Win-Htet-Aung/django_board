from django.test import TestCase
from django.urls import reverse, resolve
from .views import home

# Create your tests here.
class HomeTests(TestCase):
    def test_home_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_view(self):
        url = reverse('home')
        view = resolve(url)
        self.assertEquals(view.func, home)

