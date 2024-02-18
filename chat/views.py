from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from staff.models import ReChat
from notifications.views import message as notify
from django.contrib.auth.decorators import login_required

INBOX = 'chat:inbox'

# This is a class that displays a list of messages and other users in a chat application.
class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat/messages_list.html'

    def get_context_data(self, **kwargs):
        """
        This function retrieves message data and other user data to be displayed in a context
        dictionary.
        :return: This code is a method that returns a dictionary of context data to be used in a Django
        template. The context data includes a list of messages, a list of other users involved in those
        messages, and the current user.
        """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        messages = Message.get_message_list(user)
        other_users = []
        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)
        context['messages_list'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context

# This is a Django class-based view for displaying and handling messages in a user's inbox.
class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'chat/inbox.html'
    queryset = User.objects.all()

    def dispatch(self, request, *args, **kwargs):
        """
        This function overrides the dispatch method of a class and returns the result of calling the
        parent dispatch method with the request and arguments.
        
        :param request: The HTTP request object that contains information about the incoming request,
        such as the HTTP method, headers, and body
        :return: The `dispatch` method of a class is being called with the `request` object, `args`, and
        `kwargs` as arguments. The `super()` function is used to call the `dispatch` method of the
        parent class, and the `self.request` attribute is passed as the first argument to the parent
        method. The return value of the parent `dispatch` method is being returned.
        """
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self):
        """
        This function retrieves a User object based on the provided username or returns a 404 error if
        the object does not exist.
        :return: The `get_object()` method is returning a `User` object with the `username` specified in
        the URL path. If the user with that `username` does not exist, a 404 error page will be
        returned.
        """
        username= self.kwargs.get("username")
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        """
        This function gets context data for a view, including messages between two users and information
        about those users.
        :return: The `context` dictionary with added keys `'messages'`, `'other_person'`, and `'you'` is
        being returned.
        """
        context = super().get_context_data(**kwargs)
        user = User.objects.get(pk=self.request.user.pk)
        other_user = User.objects.get(username=self.kwargs.get("username"))
        context['messages'] = Message.get_all_messages(other_user, user)
        context['other_person'] = other_user
        context['you'] = user
        return context

    def post(self, request, *args, **kwargs):
        """
        This function handles a POST request to create a new message post with a sender, recipient,
        message, and optional image attachment.
        
        :param request: The HTTP request object that contains information about the current request,
        such as the user making the request, the HTTP method used, and any data submitted with the
        request
        :return: The view is returning a redirect to the `INBOX` view with the `username` parameter set
        to the `username` of the `recipient` user object. If the user is not authenticated, the view is
        rendering the `login.html` template.
        """
        sender = User.objects.get(pk=request.POST.get('you'))
        recipient = User.objects.get(pk=request.POST.get('recipient'))
        message = request.POST.get('message')
        image = request.FILES.get('img')
        if request.user.is_authenticated:
            if request.method == 'POST':
                mkpost(request, sender, recipient, message, image)
            return redirect(INBOX, username=recipient.username)
        else:
            return render(request, 'auth/login.html')

def mkpost(request, sender, recipient, message, image):
    """
    The function sends a message and/or image from a sender to a recipient, but redirects if the
    recipient is blocked by the sender.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, and any data submitted in the request
    :param sender: The user who is sending the message or post. It is likely an instance of a User model
    in Django or a similar framework
    :param recipient: The username of the user who will receive the message
    :param message: The message parameter is a string that represents the text message that the sender
    wants to send to the recipient
    :param image: The "image" parameter is a variable that holds the image file that the user wants to
    send along with their message. It could be an image file in any format such as JPEG, PNG, or GIF. If
    the user does not want to send an image, this parameter will be set to None
    :return: If the recipient is in the sender's blocking list or blocked list, the function redirects
    to the inbox page of the recipient's username. Otherwise, the function sends a message with the
    given parameters (sender, recipient, message, image) and returns nothing.
    """
    if recipient in sender.profile.blocking() or recipient in sender.profile.blocked():
        return redirect(INBOX, username=recipient.username)
    else:
        if image:
            message = 'Image'
        if message:
            send(request ,sender, recipient, message, image, False)

def send(request, sender, recipient, message, image, system):
    """
    This function sends a message to a recipient and creates a system message if it's the first message
    in the conversation.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the URL, headers, and any data
    that was sent with the request
    :param sender: The user who is sending the message. It is likely an instance of the User model in
    Django
    :param recipient: The user who will receive the message
    :param message: The actual text message that the sender wants to send to the recipient
    :param image: The "image" parameter is likely a variable that holds an image file or URL that the
    sender wants to include in their message. It could be an image of anything, such as a meme, a
    screenshot, or a photo. The function appears to allow for the inclusion of both a text message and
    :param system: The "system" parameter is a boolean value that indicates whether the message being
    sent is a system message or not. If it is a system message, it means that it is not a message sent
    by a user, but rather a message generated by the system itself. This can be useful for notifications
    or
    """
    if not Message.get_all_messages(sender, recipient):
        Message.objects.create(sender=sender, recipient=recipient,
        message=sender.username+
        " has started a conversation with "+
        recipient.username,
        is_system=True)
    Message.objects.create(sender=sender, recipient=recipient, message=message, image=image, is_system=system)
    notify(request, recipient)

# This is a Django class-based view that displays a list of all users in the database on a template
# called 'users_list.html'.
class UserListsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'chat/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        """
        This function adds all users to the context data of a view.
        :return: The `get_context_data` method is returning a dictionary object `context` which contains
        a key-value pair where the key is `'users'` and the value is a queryset of all `User` objects in
        the database. This queryset is obtained using the `all` method on the `User` model.
        """
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all
        return context

@login_required
def report(request, username):
    """
    This function creates a report for a chat if it doesn't already exist and redirects the user to the
    inbox page.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and any query parameters. It is typically passed as the first
    parameter to view functions
    :param username: The username parameter is a string that represents the username of a user in the
    system. It is used to filter the User model to find a specific user and then create a ReChat object
    for that user if it does not already exist. The function then redirects the user to the INBOX view
    for that
    :return: a redirect to the INBOX view with the username parameter.
    """
    chat = User.objects.filter(username=username).first()
    if chat:
        report = ReChat.objects.filter(chat=chat, creport=request.user).first()
        if not report:
            ReChat.objects.create(chat=chat, creport=request.user)
    return redirect(INBOX, username)
