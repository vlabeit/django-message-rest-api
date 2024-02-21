from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

# from django.apps import apps
# def get_user_model():
#     return apps.get_model('auth', 'User')

class Message(models.Model):
    """Model for messages"""
    message_from = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='message_from')
    message_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='message_to')
    message_title = models.CharField(max_length=255)
    message_content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(blank=True, null=True)

    REQUIRED_FIELDS = ['message_from', 'message_to', 'message_content', 'message_title']

    class Meta:
        ordering = ['-id']

    def message_viewed(self):
        """Change message to viewed and add time viewed"""
        self.is_viewed = True
        self.viewed_at = timezone.now()

    def __str__(self):
        return self.message_title
