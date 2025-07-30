from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(email='sender@example.com', password='test123', first_name='Sender', last_name='One')
        self.receiver = User.objects.create_user(email='receiver@example.com', password='test123', first_name='Receiver', last_name='Two')

    def test_notification_created_on_message_send(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")
        notif = Notification.objects.get(message=msg)
        self.assertEqual(notif.user, self.receiver)
