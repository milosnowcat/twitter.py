from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

def rename(instance):
    """
    The function renames a model instance with a unique identifier based on the model name and relevant
    user information.
    
    :param instance: The instance parameter is an instance of a Django model. It represents a single
    record in the database table associated with that model. The function takes this instance as input
    and returns a new name for it
    :return: a string that consists of the model name of the instance, the username(s) of the sender and
    recipient (if the instance is a message), and a randomly generated UUID.
    """
    if instance._meta.model_name == 'message':
        user = instance.sender.username + "_" + instance.recipient.username
    else:
        user = instance.user.username
    new_name = instance._meta.model_name + "_" + user + "_" + str(uuid.uuid4())
    return new_name

def rename_image(instance, filename):
    """
    This function renames an image file with a new name and returns the new name with a ".jpg"
    extension.
    
    :param instance: It is an instance of a model that has a field for an image file. This function is
    likely used as a helper function for renaming the image file before it is saved to the server
    :param filename: The filename parameter is a string that represents the original name of the image
    file that is being uploaded
    :return: a string value, which is the new name of the image file with the extension ".jpg".
    """
    new_name = rename(instance) + ".jpg"
    return new_name

def rename_document(instance, filename):
    """
    This function renames a document file to a new name with a ".pdf" extension.
    
    :param instance: It is an instance of a document object that needs to be renamed
    :param filename: The filename parameter is a string that represents the original name of the file
    that is being renamed
    :return: a string value, which is the new name of the document with the ".pdf" extension.
    """
    new_name = rename(instance) + ".pdf"
    return new_name

# The Profile class defines a model with various fields and methods for managing user profiles,
# including following, followers, blocking, and blocked users.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to=rename_image)
    business = models.BooleanField(default=False)
    domain = models.URLField(default='https://example.com')
    strikes = models.IntegerField(default=0)
    strike_date = models.DateTimeField(default=timezone.now)
    cv = models.FileField(default='default.pdf', upload_to=rename_document)
    mails = models.IntegerField(default=0)

    def __str__(self):
        """
        This function returns a string representation of a user's profile.
        :return: A string representation of the user's profile, specifically the username of the user
        followed by the phrase "'s profile".
        """
        return f"{self.user.username}'s profile"

    def following(self):
        """
        This function returns a queryset of users that the current user is following.
        :return: The `following` method returns a queryset of `User` objects that are being followed by
        the user associated with the current instance of the `self` object. The queryset is filtered
        based on the `to_user_id` values in the `Relationship` model where `is_follow` is True and the
        `from_user` is the user associated with the current instance of the `self` object.
        """
        user_ids = Relationship.objects.filter(from_user=self.user, is_follow=True)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        """
        This function returns a queryset of users who follow the current user.
        :return: The `followers` method is returning a queryset of `User` objects who are following the
        `self.user` object. It does this by first filtering the `Relationship` objects where `to_user`
        is `self.user` and `is_follow` is `True`, and then getting the `from_user_id` values of those
        objects. Finally, it returns a queryset of `User` objects whose
        """
        user_ids = Relationship.objects.filter(to_user=self.user, is_follow=True)\
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def blocking(self):
        """
        This function returns a queryset of users who have been blocked by the current user.
        :return: The `blocking` method is returning a queryset of `User` objects who have been blocked
        by the user associated with the current instance of the class. The queryset is filtered based on
        the `to_user_id` values of the `Relationship` objects where `is_block` is True and the
        `from_user` is the current user.
        """
        user_ids = Relationship.objects.filter(from_user=self.user, is_block=True)\
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def blocked(self):
        """
        This function returns a queryset of users who have blocked the current user.
        :return: The `blocked` method returns a queryset of `User` objects who have blocked the
        user associated with the current instance of the class. This is determined by querying the
        `Relationship` model for all relationships where the `to_user` is the current user and
        `is_block` is True, and then returning a queryset of `User` objects corresponding to the
        `from_user_id` values of
        """
        user_ids = Relationship.objects.filter(to_user=self.user, is_block=True)\
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

# The `Relationship` class defines a model with fields for a relationship between two `User`
# instances, including whether they are following each other or if one has been blocked by the other.
class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)
    is_follow = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)

    def __str__(self):
        """
        This function returns a string representation of an object with the format "from_user to
        to_user".
        :return: A string representation of the object, which includes the names of the "from_user" and
        "to_user" attributes separated by "to".
        """
        return f'{self.from_user} to {self.to_user}'

# The Ban class defines a model with name and mail attributes and a string representation method.
class Ban(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

    def __str__(self):
        """
        This function returns the name of an object as a string.
        :return: A string representation of the object's name attribute.
        """
        return f'{self.name}'

# The `Client` class is a Django model that represents a client with a name, domain, and a
# many-to-many relationship with `Ban` objects.
# * Default:
# ? UDG
# ? udg.mx
class Client(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    banned = models.ManyToManyField(Ban, blank=True)

    def __str__(self):
        """
        This function returns the name of an object as a string.
        :return: A string representation of the object's name attribute.
        """
        return f'{self.name}'
