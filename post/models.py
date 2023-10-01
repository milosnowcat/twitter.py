from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from app.models import rename_image

# The Offer class defines a model for offers with various fields such as timestamp, head, content,
# user, likes, image, and topics.
class Offer(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    head = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    likes = models.ManyToManyField(User, blank=True, related_name='olikes')
    is_delete = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to=rename_image)
    topics = models.ManyToManyField('Topic', blank=True)

    # This class sets the default ordering for a model to be based on the timestamp field in
    # descending order.
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        This function returns the string representation of the "head" attribute of an object.
        :return: The `__str__` method is returning the value of the `head` attribute of the object. It
        is assumed that `head` is a string attribute.
        """
        return self.head

# This is a Django model class for a post that includes fields for timestamp, content, user, likes,
# comments, deletion status, image, and topics.
class Post(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to=rename_image)
    topics = models.ManyToManyField('Topic', blank=True)

    # This class sets the default ordering for a model to be based on the timestamp field in
    # descending order.
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        """
        This function returns the content of an object as a string.
        :return: The `__str__` method is returning the `content` attribute of the object.
        """
        return self.content

# The Topic class defines a model with a name attribute that can be represented as a string.
class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        This function returns the name attribute of an object as a string.
        :return: The `__str__` method is returning the `name` attribute of the object.
        """
        return self.name
