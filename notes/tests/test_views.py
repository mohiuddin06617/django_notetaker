from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note


class CoreFeatureTestCase(TestCase):
    def setUp(self):
        # Create a test user
        user_email = 'admin@admin.com'
        user_password = 'password'
        self.user = get_user_model().objects.create_user(
            email=user_email,
            password=user_password
        )

        # Log in the test user
        self.client.login(email=user_email, password=user_password)

    def test_note_creation_success(self):
        # Positive scenario: Test creating a new note
        response = self.client.post(reverse('notes:note_create'), {
            'title': 'New Note',
            'content_raw': 'New content',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Note.objects.count(), 1)

    def test_note_creation_validation_failed(self):
        response = self.client.post(reverse('notes:note_create'), {
            'title': '',  # An empty title should result in form validation error
            'content_raw': 'New content',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title',
                             'This field is required.')

    def test_note_editing_success(self):
        # Create a sample note
        note = Note.objects.create(
            title='Sample Note',
            content_raw='Sample content',
            author=self.user
        )
        response = self.client.post(reverse('notes:note_update', args=[note.id]), {
            'title': 'Updated Note',
            'content_raw': 'Updated content',
        })
        self.assertEqual(response.status_code, 302)
        note.refresh_from_db()
        self.assertEqual(note.title, 'Updated Note')
        self.assertEqual(note.content_raw, 'Updated content')
