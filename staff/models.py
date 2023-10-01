from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from post.models import Offer, Post

# The ReOffer class represents a reported offer and includes a timestamp, a foreign key to the
# original offer, and a many-to-many relationship with users who reported the offer.
class ReOffer(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    reported_by = models.ManyToManyField(User)

# This is a Django model class for a repost, which includes a timestamp, a foreign key to a Post
# model, and a many-to-many relationship with User model for reporting.
class RePost(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reported_by = models.ManyToManyField(User)

# The ReChat class defines a model with timestamp, chat, and creport fields, where chat and creport
# are foreign keys to the User model.
class ReChat(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    chat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat')
    creport = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creport')

# This is a Django model class that represents a user who has been reported by other users.
class ReUser(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    reported_by = models.ManyToManyField(User)

# This is a Django model class called FoBusiness that has two fields: a timestamp field and a foreign
# key field linking to the User model.
class FoBusiness(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    business = models.ForeignKey(User, on_delete=models.CASCADE)

# This is a Django model class called FoStaff that has two fields: a timestamp field and a foreign key
# field linking to the User model.
class FoStaff(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
