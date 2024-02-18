from django.shortcuts import render, redirect
from verify_email.email_handler import send_verification_email
from .models import Notification
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def mail_verification(request,form):
    """
    This function sends a verification email and returns the result.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the URL, headers, and any data
    that was submitted with the request
    :param form: The "form" parameter is likely a Django form object that contains data submitted by a
    user through a web form. This form object would typically include fields for the user's email
    address and other relevant information needed for email verification. The "mail_verification"
    function appears to be responsible for sending a verification email
    :return: the result of the `send_verification_email` function called with the `request` and `form`
    arguments.
    """
    verification = send_verification_email(request, form)
    return verification

def mailverify(request):
    """
    The function returns a rendered HTML template for email verification notifications.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. In this specific code snippet, the
    request parameter is used
    :return: The `mailverify` view function is returning an HTTP response that renders the
    `mailverify.html` template.
    """
    return render(request, 'notifications/mailverify.html')

@login_required
def notifications(request):
    """
    This function retrieves notifications for a specific user and renders them in a list on a web page.
    
    :param request: The request parameter is an object that represents the current HTTP request. It
    contains information about the user making the request, the requested URL, any submitted data, and
    other metadata related to the request. In this case, the function is using the request object to
    filter notifications for the current user and pass them
    :return: a rendered HTML template 'notifications/list.html' with a context dictionary containing the
    notifications for the current user.
    """
    notifications = Notification.objects.filter(user=request.user)
    context = {'notifications':notifications}
    return render(request, 'notifications/list.html', context)

def send_mail(head, body, to):
    """
    The function sends an email message with a given subject, body, and recipient.
    
    :param head: The subject of the email that will be sent
    :param body: The body of the email message that will be sent. It is a string containing the main
    content of the email
    :param to: The email address of the recipient(s) to whom the email will be sent
    """
    body += "\nHexagon - Notifications"
    email = EmailMessage(head, body, to=to)
    email.send()

def notify_mail(request, head, body, to):
    """
    The function sends an email notification and resets the mail count for a user's profile if it
    exceeds 10.
    
    :param request: The request object represents the current HTTP request that is being processed by
    the server. It contains information about the client making the request, the requested URL, and any
    data that was sent along with the request. In this case, the request object is being used to access
    the user object associated with the current
    :param head: The subject of the email that will be sent
    :param body: The body parameter in the notify_mail function is a string that represents the content
    of the email that will be sent. It typically includes the message that the sender wants to convey to
    the recipient(s)
    :param to: The "to" parameter is the email address of the recipient who will receive the email
    notification
    """
    user = request.user.profile
    if user.mails >= 10:
        send_mail(head, body, to)
        user.mails = 0
        user.save()
    else:
        user.mails += 1
        user.save()

def follower(request, user):
    """
    This function creates a notification and sends an email to a user when they receive a new follower.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted in the request, and more
    :param user: The user parameter is the user who is being followed and who will receive the
    notification
    """
    title = "New follower"
    content = request.user.username + " has followed you"
    url = redirect('bus', request.user).url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    notify_mail(request, title, content, [user.email])

def post(request, user, post):
    """
    This function creates a notification and sends an email to a user when a new post is made.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted in the request, and more
    :param user: The user parameter is the user who will receive the notification
    :param post: The "post" parameter is a variable that represents a specific post object. It is likely
    being used to retrieve information about the post or to perform some action related to the post,
    such as displaying it on a webpage or updating its content
    """
    title = "New post"
    content = request.user.username + " has made a new post"
    url = redirect('post:post', post).url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    notify_mail(request, title, content, [user.email])

def offer(request, user, offer):
    """
    This function creates a notification and sends an email to a user about a new offer made by another
    user.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used, the URL
    requested, and any data submitted in the request
    :param user: The user parameter is an instance of the User model representing the user who will
    receive the notification
    :param offer: The "offer" parameter is likely an object or identifier representing a specific offer
    being made by the user. It is used in the URL redirect to the offer page
    """
    title = "New offer"
    content = request.user.username + " has made a new offer"
    url = redirect('post:offer', offer).url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    notify_mail(request, title, content, [user.email])

def comment(request, user, comment):
    """
    This function creates a notification and sends an email to a user when they receive a new comment on
    their post.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the URL being accessed, any data
    submitted in a form, and the user's session information
    :param user: The user parameter is the user who will receive the notification for the new comment
    :param comment: The comment parameter is likely the ID or reference to a specific comment that the
    user has made on a post. It is used to generate a URL that redirects to the post where the comment
    was made
    """
    title = "New comment"
    content = request.user.username + " has commented your post"
    url = redirect('post:post', comment).url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    notify_mail(request, title, content, [user.email])

def message(request, user):
    """
    This function creates a notification and sends an email to a user with a message from another user.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the URL, headers, and any data
    that was submitted with the request
    :param user: The user parameter is the recipient of the message/notification. It is the user object
    that represents the user who will receive the notification
    """
    title = "New message"
    content = request.user.username + " has sended you a message"
    url = redirect('chat:inbox', request.user).url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    notify_mail(request, title, content, [user.email])

def strike(user):
    """
    This function sends a notification to a user and sends an email if the user has received a strike,
    with a different message if they have received three strikes.
    
    :param user: The user parameter is an instance of a user model, which represents a user in the
    system. It is used to identify the user who will receive the notification
    """
    title = "New strike"
    content = "You've received a strike"
    if user.profile.strikes == 3:
        title = "ALERT"
        content = "You have been permanently suspended"
    url = redirect('notifications:strikes').url
    notify = Notification(user=user, title=title, content=content, more=url)
    notify.save()
    send_mail(title, content, [user.email])

@login_required
def strikes(request):
    """
    This function retrieves the number of strikes for the current user and a list of all superusers to
    display in a template.
    
    :param request: The request parameter is an object that represents the current HTTP request. It
    contains information about the request, such as the HTTP method used (GET, POST, etc.), the URL
    being accessed, any data submitted with the request, and more. It is typically passed as the first
    parameter to view functions in
    :return: The function `strikes` is returning an HTTP response that renders the `strikes.html`
    template with the context dictionary containing the number of strikes for the current user and a
    queryset of all users who are superusers.
    """
    admins = User.objects.filter(is_superuser=True)
    context = {'strikes':request.user.profile.strikes, 'admins':admins}
    return render(request, 'notifications/strikes.html', context)
