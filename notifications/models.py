from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# The Notification class is a model that represents a notification with a user, title, content,
# optional URL, and timestamp.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    more = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    # This class sets the default ordering for a model to be based on the timestamp field in
    # descending order.
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        This function returns the title of an object as a string.
        :return: The `__str__` method is returning the `title` attribute of the object.
        """
        return self.title
