from django.db import models
from django.contrib.auth.models import User
from app.models import rename_image

# The Message class defines a model for storing messages between users and includes methods for
# retrieving and displaying messages.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_system = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True, upload_to=rename_image)

    def __str__(self):
        """
        This function returns the message attribute of an object as a string.
        :return: The `__str__` method is returning the `message` attribute of the object.
        """
        return self.message

    # The class defines metadata for a database table called "chat_messages" including verbose names
    # and ordering.
    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    def get_all_messages(id_1, id_2):
        """
        This function retrieves all messages between two users and marks them as read for the first
        user.
        
        :param id_1: The ID of the first user in the conversation
        :param id_2: The parameter `id_2` is likely an identifier for the recipient of the messages. It
        is used in the function to filter messages where the sender is `id_1` and the recipient is
        `id_2`, and also to filter messages where the sender is `id_2` and
        :return: The function `get_all_messages` returns a list of messages between two users with the
        given `id_1` and `id_2`. The messages are sorted by date in ascending order. If `id_1` is not
        equal to `id_2`, the function also includes messages sent from `id_2` to `id_1`. The function
        also marks all messages sent from
        """
        messages = []
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date')
        for x in range(len(message1)):
            message1[x].is_read = True
            message1[x].save()
            messages.append(message1[x])
        if id_1 != id_2:
            message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
            for x in range(len(message2)):
                messages.append(message2[x])
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

    def get_message_list(u):
        """
        This function retrieves a list of messages for a given user, sorted by sender and date, and
        removes duplicates.
        
        :param u: The parameter "u" is likely a user object representing the user for whom we want to
        retrieve a list of messages
        :return: The function `get_message_list(u)` returns a list of messages that involve the user
        `u`. The messages are sorted by sender's username and then by date in descending order. The
        function also removes duplicate messages and returns only one message per conversation between
        two users.
        """
        m = []
        j = []
        k = []
        for message in Message.objects.all():
            for_you = message.recipient == u
            from_you = message.sender == u
            if (for_you != from_you) and (for_you or from_you):
                m.append(message)
                m.sort(key=lambda x: x.sender.username)
                m.sort(key=lambda x: x.date, reverse=True)
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)
        return k
