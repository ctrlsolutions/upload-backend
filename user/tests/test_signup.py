from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from university.models import College, Department

CustomUser = get_user_model()

class SignUpTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.college = College.objects.create(code="ENG", name="College of Engineering")
        cls.department = Department.objects.create(code="CS", name="Computer Science", college=cls.college)

    def setUp(self):
        self.url = "/api/user/"
        self.valid_payload = {
            "email": "juan.delacruz@up.edu.ph",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Juan",
            "middle_name": "Reyes",
            "last_name": "Dela Cruz",
            "sex": "M",
            "birth_date": "2000-01-01",
            "college": self.college.pk,
            "department": self.department.pk
        }


    def test_valid_signup(self):
        print(College.objects.all())
        print(Department.objects.all())
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email=self.valid_payload['email']).exists())

    def test_invalid_email_domain(self):
        payload = self.valid_payload.copy()
        payload['email'] = "juan@gmail.com"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['error'])

    def test_mismatched_passwords(self):
        payload = self.valid_payload.copy()
        payload['password2'] = "Different123!"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data['error'])

    def test_weak_password(self):
        payload = self.valid_payload.copy()
        payload['password'] = payload['password2'] = "weakpass"
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data['error'])

    def test_missing_required_field(self):
        payload = self.valid_payload.copy()
        del payload['first_name']
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data['error'])
