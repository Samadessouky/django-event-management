from django.test import TestCase
from .models import Event, EventCategory


class EventViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.category = EventCategory.objects.create(name='Test Category', code='TC123', status='active')

    def test_event_create_view(self):
        url = reverse('admin_events:event-create')
        data = {
            'category': self.category.id,
            'name': 'Test Event',
            'description': 'Test Event Description',
            'scheduled_status': 'scheduled',
            'venue': 'Test Venue',
            'start_date': '2024-12-25',
            'end_date': '2024-12-26',
            'location': 'Test Location',
            'maximum_attende': 100,
            'price': 50,
            'status': 'active'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(Event.objects.filter(name='Test Event').exists())

    def test_event_update_view(self):
        event = Event.objects.create(
            category=self.category,
            name='Old Event',
            description='Old Event Description',
            scheduled_status='scheduled',
            venue='Old Venue',
            start_date='2024-12-20',
            end_date='2024-12-21',
            location='Old Location',
            maximum_attende=50,
            price=100,
            status='active'
        )
        url = reverse('admin_events:event-edit', args=[event.id])
        data = {
            'category': self.category.id,
            'name': 'Updated Event',
            'description': 'Updated Event Description',
            'scheduled_status': 'scheduled',
            'venue': 'Updated Venue',
            'start_date': '2024-12-27',
            'end_date': '2024-12-28',
            'location': 'Updated Location',
            'maximum_attende': 200,
            'price': 150,
            'status': 'active'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        event.refresh_from_db()
        self.assertEqual(event.name, 'Updated Event')

    def test_event_delete_view(self):
        event = Event.objects.create(
            category=self.category,
            name='Delete Event',
            description='Delete Event Description',
            scheduled_status='scheduled',
            venue='Delete Venue',
            start_date='2024-12-29',
            end_date='2024-12-30',
            location='Delete Location',
            maximum_attende=10,
            price=20,
            status='active'
        )
        url = reverse('admin_events:event-delete', args=[event.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Event.objects.filter(name='Delete Event').exists())
# Create your tests here.
