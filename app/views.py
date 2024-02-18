from django.shortcuts import render, redirect
from .models import Relationship
from .forms import UserRegisterForm, ProfileUpdateForm, BusRegisterForm, BusProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from staff.models import ReUser, FoBusiness, FoStaff
from notifications.views import mail_verification, follower
from notifications.views import strike as snotify
from django.utils import timezone
from datetime import timedelta
from post.models import Post, Offer
from chat.views import send

def home(request):
    """
    This function returns a rendered HTML template for the home page of a web application.
    
    :param request: The request parameter is an HttpRequest object that represents the current request
    made by the user. It contains information about the request, such as the HTTP method used (GET,
    POST, etc.), the URL requested, any data submitted in the request, and more. The request object is
    typically passed as the first
    :return: The `home` function is returning an HTTP response generated by the `render` function. The
    response will render the `home.html` template using the `request` object as context.
    """
    return render(request, 'app/home.html')

def registerb(request):
    """
    This function registers a business using a form and redirects to the start page if the form is valid.
    
    :param request: The `request` parameter is an HttpRequest object that represents the current request
    made by the user. It contains information about the request, such as the HTTP method used (GET,
    POST, etc.), the user's IP address, and any data submitted in the request. It is passed as the first
    parameter
    :return: a rendered HTML template 'app/registerB.html' with a context dictionary containing a form
    object. If the request method is POST and the form is valid, the function will also redirect the
    user to the 'startb' URL.
    """
    if request.method == 'POST':
        form = BusRegisterForm(request.POST)
        if form.is_valid():
            mail_verification(request, form)
            return redirect('startb')
    else:
        form = BusRegisterForm()
    context = {'form':form}
    return render(request, 'app/registerB.html', context)

def register(request):
    """
    This function handles user registration and redirects to a mail verification page if the
    registration form is valid.
    
    :param request: The request object represents the HTTP request that the user has made to the server.
    It contains information about the request, such as the HTTP method used (GET, POST, etc.), the URL
    requested, any data submitted in the request, and more. The view function uses this object to
    process the request
    :return: a rendered HTML template 'app/register.html' with a context dictionary containing a
    UserRegisterForm object. If the request method is POST and the form is valid, the function will call
    the mail_verification function and redirect to the 'notifications:mailverify' URL.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            mail_verification(request, form)
            return redirect('notifications:mailverify')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'app/register.html', context)

@login_required
def startb(request):
    """
    This function saves the user's business profile form and creates a new FoBusiness object if one does
    not already exist.
    
    :param request: The request parameter is an object that represents an HTTP request made by a client
    to a server. It contains information about the request, such as the HTTP method used (e.g. GET,
    POST), the URL being requested, any data submitted in the request, and more. In this specific code
    snippet
    :return: This function returns an HTTP response rendered by the `render` function. The rendered
    template is `app/startB.html` and the context contains a `BusProfileForm` instance.
    """
    if request.method == 'POST':
        form = BusProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            bus = FoBusiness.objects.filter(business=request.user).first()
            if not bus and not request.user.profile.business:
                FoBusiness.objects.create(business=request.user)
            return redirect('home')
    else:
        form = BusProfileForm()
    context = {'form':form}
    return render(request, 'app/startB.html', context)

def bus(request, username):
    """
    This function displays a business profile page with offers if the user is a business and not blocked
    by the viewer.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and other metadata. It is passed to the view function by Django's
    URL routing
    :param username: The username parameter is a string that represents the username of a user in the
    system. It is used to retrieve the User object associated with that username from the database
    :return: a rendered HTML template with context data, which displays information about a user's
    business and their offers. If the requesting user is blocked by the business owner, they are
    redirected to their own business page. If the requesting user has blocked the business owner, only
    limited information is displayed. If the user does not have a business, they are redirected to their
    profile page.
    """
    user = User.objects.get(username=username)
    if user.profile.business:
        if request.user in user.profile.blocking():
            return redirect('bus', request.user)
        elif request.user not in user.profile.blocked():
            offers = user.offers.filter(is_delete=False)
            context = {'user':user, 'offers':offers}
        else:
            context = {'user':user}
        return render(request, 'app/bus.html', context)
    else:
        return redirect('profile', user)

def profile(request, username):
    """
    This function retrieves a user's profile and their posts, and checks if the requesting user is
    blocked by the profile owner.
    
    :param request: The request parameter is an HttpRequest object that represents the current request
    made by the user. It contains information about the request, such as the HTTP method used, the
    headers, the user agent, and the request body. It is passed to the view function by Django's URL
    resolver
    :param username: The username parameter is a string that represents the username of the user whose
    profile is being requested
    :return: a rendered HTML template of the user's profile page with their posts (if they have any) and
    some context information. If the requesting user is blocked by the profile owner, they will be
    redirected to the bus page. If the requesting user is blocked by the profile owner, they will only
    see the profile information without any posts.
    """
    user = User.objects.get(username=username)
    if request.user in user.profile.blocking():
        return redirect('bus', request.user)
    elif request.user not in user.profile.blocked():
        posts = user.posts.filter(is_delete=False)
        context = {'user':user, 'posts':posts}
    else:
        context = {'user':user}
    return render(request, 'app/profile.html', context)

@login_required
def edit(request):
    """
    This function updates a user's profile information and redirects them to a specific page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, including the user making the request, the HTTP method used (e.g. GET, POST), and any data
    submitted with the request. It is passed to the view function as an argument
    :return: a rendered HTML template 'edit.html' with a context dictionary containing a form object. If
    the request method is POST and the form is valid, the function redirects the user to the 'bus' page
    with the user's profile instance.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('bus', request.user)
    else:
        form = ProfileUpdateForm()
    context = {'form':form}
    return render(request, 'app/edit.html', context)

@login_required
def follow(request, username):
    """
    This function allows a user to follow or unfollow another user and updates the relationship status
    accordingly.
    
    :param request: The request object represents the HTTP request that the user has made to the server.
    It contains information about the request, such as the HTTP method used (GET, POST, etc.), the
    headers, and any data that was sent with the request
    :param username: The username parameter is a string that represents the username of the user that
    the current user wants to follow or unfollow
    :return: a redirect to the 'bus' page for the user with the given username.
    """
    current_user = request.user
    to_user = User.objects.get(username=username)
    rel = Relationship.objects.filter(from_user=current_user, to_user=to_user).first()
    if rel:
        if rel.is_follow:
            rel.is_follow = False
            rel.save()
        else:
            rel.is_follow = True
            rel.save()
            follower(request, to_user)
    else:
        rel = Relationship(from_user=current_user, to_user=to_user, is_follow=True)
        rel.save()
        follower(request, to_user)
    return redirect('bus', username)

@login_required
def report(request, username):
    """
    This function reports a user and saves the report in the database.
    
    :param request: The request parameter is an object that contains information about the current
    request, including the user making the request, the HTTP method used, and any data submitted with
    the request. It is typically passed to a view function in Django
    :param username: The username parameter is a string that represents the username of a user in the
    system. It is used to filter the User model to retrieve the user object with the matching username
    :return: a redirect to the 'bus' view with the username parameter.
    """
    user = User.objects.filter(username=username).first()
    report = ReUser.objects.filter(user=user).first()
    if report:
        report.reported_by.add(request.user.pk)
        report.save()
    else:
        if user:
            new_report = ReUser.objects.create(user=user)
            new_report.reported_by.add(request.user.pk)
            new_report.save()
    return redirect('bus', username)

@login_required
def staff(request):
    """
    This function creates a new FoStaff object for the current user if one does not already exist and
    redirects to the home page.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by a
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. In this specific code snippet, the
    `request
    :return: The code is returning a redirect to the 'home' URL after creating a new FoStaff object with
    the current user as the staff member if one does not already exist.
    """
    form = FoStaff.objects.filter(staff=request.user)
    if not form:
        FoStaff.objects.create(staff=request.user)
    return redirect('home')

@login_required
def block(request, username):
    """
    This function allows a user to block or unblock another user and sends a notification message
    accordingly.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), any data submitted with the request, and the user's session information
    :param username: The username parameter is a string that represents the username of the user that
    the current user wants to block or unblock
    :return: a redirect to the 'bus' view with the username parameter.
    """
    current_user = request.user
    to_user = User.objects.get(username=username)
    rel = Relationship.objects.filter(from_user=current_user, to_user=to_user).first()
    if current_user != to_user:
        if rel:
            if rel.is_block:
                rel.is_block = False
                rel.save()
                message = current_user.username + " has unblocked " + to_user.username
                send(request, current_user, to_user, message, None, True)
            else:
                rel.is_block = True
                rel.save()
                message = current_user.username + " has blocked " + to_user.username
                send(request, current_user, to_user, message, None, True)
        else:
            rel = Relationship(from_user=current_user, to_user=to_user, is_block=True)
            rel.save()
    return redirect('bus', username)

def strike(user):
    """
    The function adds a strike to a user's profile and takes appropriate actions based on the number of
    strikes.
    
    :param user: The "user" parameter is an instance of the User model in Django, which represents a
    user account in the application. The function "strike" is designed to add a strike to the user's
    profile and take appropriate actions based on the number of strikes the user has accumulated
    """
    user.profile.strikes += 1
    if user.profile.strikes == 1:
        user.profile.strike_date = timezone.now() + timedelta(days=7)
        if user.is_staff and not user.is_superuser:
            user.is_staff = False
            user.save()
    elif user.profile.strikes == 2:
        user.profile.strike_date = timezone.now() + timedelta(days=28)
    elif user.profile.strikes >= 3:
        user.profile.strike_date = timezone.now() + timedelta(days=365)
        rem(user)
    user.profile.save()
    snotify(user)

def rem(user):
    """
    The function "rem" removes a user's posts, offers, and followers.
    
    :param user: The "user" parameter is likely a variable that represents a user in a system or
    application. The "rem" function appears to be removing various aspects of the user's data or
    settings, such as their position, offline status, and followers. However, without more context it is
    difficult to determine the
    """
    rempos(user)
    remoff(user)
    remfol(user)

def rempos(user):
    """
    The function `rempos` sets the `is_delete` attribute of all posts belonging to a given user to
    `True`.
    
    :param user: The "user" parameter is an object that represents a user in the system. It is used to
    filter all the posts that belong to that user and mark them as deleted by setting the "is_delete"
    attribute to True
    """
    posts = Post.objects.filter(user=user)
    for post in posts:
        post.is_delete = True
        post.save()

def remoff(user):
    """
    The function sets the "is_delete" attribute to True for all offers associated with a given user.
    
    :param user: The "user" parameter is an object that represents a user in the system. It is used to
    filter all the offers that belong to that user and mark them as deleted by setting the "is_delete"
    attribute to True
    """
    offers = Offer.objects.filter(user=user)
    for offer in offers:
        offer.is_delete = True
        offer.save()

def remfol(user):
    """
    The function "remfol" removes all follow relationships for a given user.
    
    :param user: The "user" parameter is an instance of a user model in Django. It is used to filter the
    Relationship objects based on the "from_user" and "to_user" fields. The function "remfol" removes
    all the follow relationships for the given user by setting the "is_follow" field
    """
    ers = Relationship.objects.filter(from_user=user,is_follow=True)
    for er in ers:
        er.is_follow = False
        er.save()
    ings = Relationship.objects.filter(to_user=user,is_follow=True)
    for ing in ings:
        ing.is_follow = False
        ing.save()

def about(request):
    """
    This function returns a rendered HTML template for the "about" page of a web application.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information about the request, such as the URL, headers, and any
    data sent in the request body. In this code snippet, the request object is passed to the render
    function, which uses it
    :return: The `about` view function is returning an HTTP response that renders the `about.html`
    template.
    """
    return render(request, 'app/about.html')
