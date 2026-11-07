from django.test import TestCase
from django.urls import reverse


class CatalogRouteTests(TestCase):
    def test_home(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Active Courses Offered')

    def test_course_list_and_search(self):
        self.assertContains(self.client.get('/courses/'), 'DTI201')
        r = self.client.get('/courses/', {'q': 'react'})
        self.assertContains(r, 'DTI305')
        self.assertNotContains(r, 'DTI201')
        self.assertContains(self.client.get('/courses/', {'q': 'zzz'}), 'No courses match')

    def test_detail_and_404(self):
        self.assertContains(self.client.get('/courses/101/'), 'DTI412')
        self.assertEqual(self.client.get('/courses/999/').status_code, 404)

    def test_inquiry_validation_and_success(self):
        url = reverse('catalog:inquiry')
        r = self.client.post(url, {'student_name': '', 'email': 'bad', 'message': ''})
        self.assertContains(r, 'Student Name is required.')
        self.assertContains(r, 'A valid Email address is required.')
        r = self.client.post(url, {'student_name': 'Jane', 'email': 'j@x.com',
                                   'course_code': 'DTI412', 'message': 'Hi'})
        self.assertContains(r, 'Inquiry Processed Successfully!')

    def test_csrf_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        self.assertEqual(c.post('/inquiry/', {'student_name': 'a'}).status_code, 403)
