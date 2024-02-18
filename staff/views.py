from django.shortcuts import render, redirect
from .models import ReOffer, RePost, ReChat, ReUser, FoBusiness, FoStaff
from chat.models import Message
from app.views import strike as notify
from app.models import Profile
from django.utils import timezone

SOCIAL = 'staff:social'
FEED = 'staff:feed'

def home(request):
    """
    The "home" function checks if the user is a staff member and renders the staff home page if they
    are, otherwise it redirects to the regular home page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first parameter to a view function in
    Django
    :return: If the user is a staff member, the function calls the `unstrike()` function and returns the
    `staff/home.html` template using the `render()` function. If the user is not a staff member, the
    function redirects to the `home` URL.
    """
    if request.user.is_staff:
        unstrike()
        return render(request, 'staff/home.html')
    else:
        return redirect('home')

def feed(request):
    """
    This function checks if the user is a staff member and if so, retrieves all ReOffer objects and
    renders them in a template, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that represents an HTTP request made by a client
    to a server. It contains information about the request, such as the HTTP method used (e.g. GET,
    POST), the URL requested, any data submitted with the request, and more. In this code snippet, the
    :return: If the user is a staff member, the function returns a rendered HTML template
    'staff/feed.html' with a context dictionary containing all ReOffer objects ordered by timestamp. If
    the user is not a staff member, the function redirects to the 'home' page.
    """
    if request.user.is_staff:
        offers = ReOffer.objects.all().order_by('timestamp')
        context = {'offers':offers}
        return render(request, 'staff/feed.html', context)
    else:
        return redirect('home')

def offer(request, pk):
    """
    This function checks if the user is a staff member and returns a list of offers if they exist,
    otherwise it redirects to the feed page.
    
    :param request: The request parameter is an object that contains information about the current
    request made by the user, such as the HTTP method used, the user agent, the user's IP address, and
    any data submitted in the request. It is typically passed as the first argument to a view function
    in Django
    :param pk: pk is a parameter that represents the primary key of a ReOffer object. It is used to
    retrieve a specific ReOffer object from the database. The function checks if the user making the
    request is a staff member, and if so, it retrieves the ReOffer object with the specified primary key
    and renders
    :return: a rendered HTML template with the context variable 'offers' if the user is a staff member
    and there is at least one ReOffer object with the primary key (pk) specified in the URL. If there
    are no ReOffer objects with the specified pk, the function redirects to the FEED URL. If the user is
    not a staff member, the function redirects to the 'home'
    """
    if request.user.is_staff:
        offers = ReOffer.objects.filter(pk=pk)
        if offers:
            context = {'offers':offers}
            return render(request, 'staff/feed.html', context)
        else:
            return redirect(FEED)
    else:
        return redirect('home')

def osave(request, pk):
    """
    The "osave" function deletes a ReOffer object with a specific primary key if the user is a staff
    member, and redirects to a certain page, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current
    request made by the user, such as the HTTP method used, the user agent, the headers, the cookies,
    and the request body. It is typically passed as an argument to a view function in Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific ReOffer object that the function is trying to delete. The primary key is used to identify
    and access a specific record in a database table
    :return: If the user is a staff member, the function deletes a ReOffer object with the primary key
    (pk) specified in the URL and redirects to the FEED page. If the user is not a staff member, the
    function redirects to the 'home' page. So, either a redirect to the FEED page or the 'home' page is
    being returned depending on the user's status.
    """
    if request.user.is_staff:
        offer = ReOffer.objects.filter(pk=pk).first()
        if offer:
            offer.delete()
        return redirect(FEED)
    else:
        return redirect('home')

def odelete(request, pk):
    """
    This function deletes an offer and notifies the user if the current user is a staff member.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific ReOffer object that is being deleted. The primary key is typically an integer value
    assigned to each object in a database table
    :return: If the user is a staff member, the function will delete an offer and redirect to the FEED
    page. If the user is not a staff member, the function will redirect to the 'home' page.
    """
    if request.user.is_staff:
        offer = ReOffer.objects.filter(pk=pk).first()
        if offer:
            offer.offer.is_delete = True
            offer.offer.save()
            notify(offer.offer.user)
            offer.delete()
        return redirect(FEED)
    else:
        return redirect('home')

def social(request):
    """
    This function checks if the user is a staff member and if so, retrieves all RePost objects and
    renders them in a staff-specific template, otherwise redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current
    request made by the user, such as the HTTP method used, the URL requested, any data submitted in the
    request, and the user making the request (if authenticated). It is typically passed as the first
    argument to a view function in Django
    :return: If the user is a staff member, the function returns a rendered HTML template
    'staff/social.html' with all RePost objects ordered by timestamp. If the user is not a staff member,
    the function redirects to the 'home' page.
    """
    if request.user.is_staff:
        posts = RePost.objects.all().order_by('timestamp')
        context = {'posts':posts}
        return render(request, 'staff/social.html', context)
    else:
        return redirect('home')

def post(request, pk):
    """
    This function checks if the user is a staff member and returns a page with a specific post if it
    exists, otherwise redirects to a different page.
    
    :param request: The request parameter is an object that represents an HTTP request made by a client
    to a server. It contains information about the request, such as the HTTP method used (GET, POST,
    etc.), the URL requested, any data submitted with the request, and more. In this code snippet, the
    request
    :param pk: The "pk" parameter in this code refers to the primary key of a RePost object that is
    being requested. The view is checking if the user is a staff member, and if so, it retrieves the
    RePost object with the specified primary key and renders it in the 'staff/social.html'
    :return: If the user is a staff member and there is a RePost object with the primary key (pk)
    specified in the URL, a rendered template with the posts context variable is returned. If there is
    no RePost object with that primary key, the user is redirected to the SOCIAL page. If the user is
    not a staff member, they are redirected to the home page.
    """
    if request.user.is_staff:
        posts = RePost.objects.filter(pk=pk)
        if posts:
            context = {'posts':posts}
            return render(request, 'staff/social.html', context)
        else:
            return redirect(SOCIAL)
    else:
        return redirect('home')

def psave(request, pk):
    """
    The function deletes a post if the user is a staff member, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current
    request made by the user, such as the HTTP method used, the user agent, the user's IP address, and
    any data submitted in the request. It is typically passed as an argument to view functions in Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific RePost object that the function is trying to delete. The primary key is used to identify
    and access a specific record in a database table
    :return: If the user is a staff member, the function will delete a RePost object with the primary
    key (pk) specified in the URL and redirect to the SOCIAL page. If the user is not a staff member,
    the function will redirect to the 'home' page.
    """
    if request.user.is_staff:
        post = RePost.objects.filter(pk=pk).first()
        if post:
            post.delete()
        return redirect(SOCIAL)
    else:
        return redirect('home')

def pdelete(request, pk):
    """
    This function deletes a post and notifies the user if the requesting user is a staff member.
    
    :param request: The request parameter is an HttpRequest object that contains information about the
    current request, including metadata such as headers and user information, as well as any data
    submitted in the request. It is typically passed as the first argument to a view function in Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    RePost object that is being deleted. The primary key is a field in the database table that ensures
    each record has a unique identifier. In Django, primary keys are automatically generated for each
    model unless specified otherwise
    :return: If the user is a staff member, the function will delete a post and redirect to the SOCIAL
    page. If the user is not a staff member, the function will redirect to the 'home' page.
    """
    if request.user.is_staff:
        post = RePost.objects.filter(pk=pk).first()
        if post:
            post.post.is_delete = True
            post.post.save()
            notify(post.post.user)
            post.delete()
        return redirect(SOCIAL)
    else:
        return redirect('home')

def chat(request):
    """
    The function checks if the user is staff and returns a rendered chat page with all ReChat objects
    ordered by timestamp, or redirects to the home page if the user is not staff.
    
    :param request: The request parameter is an object that represents the current HTTP request. It
    contains information about the request, such as the HTTP method used (GET, POST, etc.), the URL
    being requested, any data submitted with the request, and more. It is typically passed as the first
    parameter to a view function
    :return: If the user is a staff member, the function returns a rendered HTML template
    'staff/chat.html' with a context containing all ReChat objects ordered by timestamp. If the user is
    not a staff member, the function redirects to the 'home' page.
    """
    if request.user.is_staff:
        chats = ReChat.objects.all().order_by('timestamp')
        context = {'chats':chats}
        return render(request, 'staff/chat.html', context)
    else:
        return redirect('home')

def inbox(request, pk):
    """
    This function displays the messages in an inbox for staff users, given a specific chat ID.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user, the requested URL, any submitted data, and other
    metadata related to the request
    :param pk: The "pk" parameter is a primary key used to identify a specific object in the database.
    In this case, it is used to retrieve a specific ReChat object from the database
    :return: If the user is a staff member, the function returns a rendered HTML template with the chat
    messages and related information. If the user is not a staff member, the function redirects to the
    home page.
    """
    if request.user.is_staff:
        chats = ReChat.objects.filter(pk=pk).first()
        if chats:
            messages = Message.get_all_messages(chats.chat, chats.creport)
            context = {'report':chats, 'messages':messages,'other_person':chats.chat,'you':chats.creport}
            return render(request, 'staff/inbox.html', context)
        else:
            return redirect('staff:chat')
    else:
        return redirect('home')

def cstrike(request, pk):
    """
    This function checks if the user is a staff member, deletes a chat object if it exists, and
    redirects to the staff inbox page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: The "pk" parameter in this code refers to the primary key of a ReChat object that is
    being passed in as an argument to the view function. It is used to retrieve a specific ReChat object
    from the database and perform some actions on it
    :return: If the user is a staff member, the function will delete a ReChat object with the primary
    key (pk) specified in the URL parameter, notify the chat associated with the ReChat object, and
    redirect to the staff inbox page. If the user is not a staff member, the function will redirect to
    the home page. Therefore, the function returns a redirect response.
    """
    if request.user.is_staff:
        chats = ReChat.objects.filter(pk=pk).first()
        if chats:
            notify(chats.chat)
            chats.delete()
        return redirect('staff:inbox', pk)
    else:
        return redirect('home')

def cdismiss(request, pk):
    """
    This function deletes a chat if the user is a staff member and redirects them to the inbox page,
    otherwise it redirects them to the home page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, including the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: "pk" stands for "primary key" and is a unique identifier for a specific object in a
    database table. In this case, it is being used to identify a specific ReChat object that the
    function will delete
    :return: If the user is a staff member, the function will delete a ReChat object with the primary
    key (pk) specified in the URL and redirect to the staff inbox page. If the user is not a staff
    member, the function will redirect to the home page.
    """
    if request.user.is_staff:
        chats = ReChat.objects.filter(pk=pk).first()
        if chats:
            chats.delete()
        return redirect('staff:inbox', pk)
    else:
        return redirect('home')

def user(request):
    """
    This function checks if the user is a staff member and if so, retrieves all ReUser objects and
    orders them by timestamp, then renders the 'staff/user.html' template with the users as context. If
    the user is not a staff member, it redirects to the 'home' page.
    
    :param request: The request parameter is an object that represents an HTTP request made by a client
    to a server. It contains information about the request, such as the HTTP method used (e.g. GET,
    POST), the URL requested, any data submitted with the request, and more. In this code snippet, the
    :return: If the user making the request is a staff member, the function returns a rendered HTML
    template 'staff/user.html' that displays a list of all ReUser objects ordered by their timestamp
    attribute. If the user is not a staff member, the function redirects them to the 'home' page.
    """
    if request.user.is_staff:
        users = ReUser.objects.all().order_by('timestamp')
        context = {'users':users}
        return render(request, 'staff/user.html', context)
    else:
        return redirect('home')

def bus(request, pk):
    """
    This function displays a user's business offers if the user is a staff member and the user has a
    business profile.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the body of the request, and other metadata. It is passed to the view function as an
    argument
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    ReUser object that is being requested. The function retrieves the ReUser object with the given
    primary key and uses it to display information about the user's business and any offers they have
    made
    :return: a rendered HTML template with context data if the user is a staff member and the report
    exists and belongs to a user with a business profile. If the report does not exist or the user does
    not have a business profile, it redirects to another page. If the user is not a staff member, it
    redirects to the home page.
    """
    if request.user.is_staff:
        report = ReUser.objects.filter(pk=pk).first()
        if report:
            if report.user.profile.business:
                offers = report.user.offers.filter(is_delete=False)
                context = {'user':report.user, 'offers':offers, 'report':report}
                return render(request, 'staff/bus.html', context)
            else:
                return redirect('staff:profile', pk)
        else:
            return redirect('staff:user')
    else:
        return redirect('home')

def profile(request, pk):
    """
    This function displays the profile of a user with their posts and report information if the
    requesting user is a staff member.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user, the requested URL, any submitted data, and other
    metadata related to the request
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    ReUser object that is being requested in the view. The view retrieves the ReUser object with the
    given primary key and uses it to display information about the user and their posts
    :return: If the user making the request is a staff member, the function returns a rendered HTML
    template with the user's profile information and posts. If the requested user does not exist, the
    function redirects to the staff user page. If the user making the request is not a staff member, the
    function redirects to the home page.
    """
    if request.user.is_staff:
        report = ReUser.objects.filter(pk=pk).first()
        if report:
            posts = report.user.posts.filter(is_delete=False)
            context = {'user':report.user, 'posts':posts, 'report':report}
            return render(request, 'staff/profile.html', context)
        else:
            return redirect('staff:user')
    else:
        return redirect('home')

def ustrike(request, pk):
    """
    This function deletes a report and notifies the user if the requesting user is a staff member.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    ReUser object that is being passed as an argument to the ustrike function. The function uses this
    primary key to retrieve the corresponding ReUser object from the database and perform certain
    actions on it, such as
    :return: If the user making the request is a staff member, the function will delete a ReUser object
    with the primary key (pk) specified in the request and notify the user associated with that object.
    Then, it will redirect to the 'staff:bus' page with the same primary key. If the user making the
    request is not a staff member, it will redirect to the 'home' page.
    """
    if request.user.is_staff:
        report = ReUser.objects.filter(pk=pk).first()
        if report:
            notify(report.user)
            report.delete()
        return redirect('staff:bus', pk)
    else:
        return redirect('home')

def udismiss(request, pk):
    """
    This function deletes a ReUser object with a given primary key if the user is a staff member, and
    redirects to a specific page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: `pk` stands for "primary key" and is a unique identifier for a specific object in a
    database table. In this case, it is used to identify a specific `ReUser` object that needs to be
    deleted
    :return: If the user making the request is a staff member, the function will delete a ReUser object
    with the primary key (pk) specified in the URL and redirect to the 'staff:bus' URL with the same
    primary key. If the user is not a staff member, the function will redirect to the 'home' URL.
    Therefore, the function returns a redirect response.
    """
    if request.user.is_staff:
        report = ReUser.objects.filter(pk=pk).first()
        if report:
            report.delete()
        
        return redirect('staff:bus', pk)
    else:
        return redirect('home')

def blist(request):
    """
    This function returns a list of FoBusiness objects ordered by timestamp if the user is a staff
    member, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, including the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first parameter to a view function in
    Django
    :return: If the user is a staff member, the function returns a rendered HTML template
    'staff/blist.html' with a context dictionary containing all FoBusiness objects ordered by their
    timestamp. If the user is not a staff member, the function redirects them to the 'home' page.
    """
    if request.user.is_staff:
        users = FoBusiness.objects.all().order_by('timestamp')
        context = {'users':users}
        return render(request, 'staff/blist.html', context)
    else:
        return redirect('home')

def bprofile(request, pk):
    """
    This function displays the profile of a business and its posts if the user is a staff member.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. The view function uses this object to
    determine how to respond
    :param pk: pk stands for "primary key". In this context, it is used to retrieve a specific instance
    of the FoBusiness model based on its primary key value. The primary key is a unique identifier for
    each instance of a model in a database
    :return: a rendered HTML template 'staff/bprofile.html' with a context dictionary containing a
    report object, a user object, and a queryset of posts. If the user is not a staff member, the
    function redirects to the 'home' page. If the form object is not found, the function redirects to
    the 'blist' page.
    """
    if request.user.is_staff:
        form = FoBusiness.objects.filter(pk=pk).first()
        if form:
            posts = form.business.posts.filter(is_delete=False)
            context = {'report':form, 'user':form.business, 'posts':posts}
            return render(request, 'staff/bprofile.html', context)
        else:
            return redirect('staff:blist')
    else:
        return redirect('home')

def baccept(request, pk):
    """
    This function accepts a business request and updates the business profile if the user is a staff
    member.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the user agent, and the request body. It is typically passed as the first argument to a
    view function in
    :param pk: The "pk" parameter in this function refers to the primary key of a specific FoBusiness
    object that is being accepted. The function retrieves the FoBusiness object with the given primary
    key and sets the "business" attribute of its associated profile to True, indicating that the
    business has been accepted. Then,
    :return: If the user is a staff member, the function will update the business profile to set the
    "business" attribute to True, delete the form, and redirect to the staff business profile page. If
    the user is not a staff member, the function will redirect to the home page.
    """
    if request.user.is_staff:
        form = FoBusiness.objects.filter(pk=pk).first()
        if form:
            form.business.profile.business = True
            form.business.profile.save()
            form.delete()
        return redirect('staff:bprofile', pk)
    else:
        return redirect('home')

def bdeny(request, pk):
    """
    The function deletes a business form if the user is a staff member and redirects to the staff
    profile page, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current
    request, such as the user making the request, the HTTP method used, and any data submitted with the
    request. It is typically passed to a view function in Django
    :param pk: `pk` stands for "primary key" and is a unique identifier for a specific instance of a
    model in a database. In this case, it is used to identify a specific instance of the `FoBusiness`
    model that the user wants to delete
    :return: If the user is a staff member, the function deletes a FoBusiness object with the primary
    key (pk) specified in the URL and redirects to the staff:bprofile page with the same primary key. If
    the user is not a staff member, the function redirects to the home page.
    """
    if request.user.is_staff:
        form = FoBusiness.objects.filter(pk=pk).first()
        if form:
            form.delete()
        return redirect('staff:bprofile', pk)
    else:
        return redirect('home')

def slist(request):
    """
    This function returns a list of staff users if the requesting user is a staff member, otherwise it
    redirects to the home page.
    
    :param request: The request parameter is an object that represents an HTTP request made by a client
    to a server. It contains information about the request, such as the HTTP method used (e.g. GET,
    POST), the URL requested, any data submitted with the request, and more. In this code snippet, the
    :return: If the user is a staff member, a list of all FoStaff objects ordered by timestamp is
    returned in the context of the 'staff/slist.html' template. If the user is not a staff member, they
    are redirected to the 'home' page.
    """
    if request.user.is_staff:
        users = FoStaff.objects.all().order_by('timestamp')
        context = {'users':users}
        return render(request, 'staff/slist.html', context)
    else:
        return redirect('home')

def sprofile(request, pk):
    """
    This function displays the profile of a staff member and their posts if the user is a staff member
    and the staff member exists, otherwise it redirects to the staff list or home page.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. The view function uses this object to
    determine how to respond
    :param pk: pk is a parameter that stands for "primary key". In this context, it is used to retrieve
    a specific instance of the FoStaff model from the database based on its primary key value. The
    primary key is a unique identifier for each instance of a model in the database
    :return: a rendered HTML template with the context variables 'report', 'user', and 'posts' if the
    user making the request is a staff member and the FoStaff object with the primary key 'pk' exists.
    If the user is not a staff member, they are redirected to the home page. If the FoStaff object does
    not exist, the user is redirected to the staff list page
    """
    if request.user.is_staff:
        form = FoStaff.objects.filter(pk=pk).first()
        if form:
            posts = form.staff.posts.filter(is_delete=False)
            context = {'report':form, 'user':form.staff, 'posts':posts}
            return render(request, 'staff/sprofile.html', context)
        else:
            return redirect('staff:slist')
    else:
        return redirect('home')

def saccept(request, pk):
    """
    This function checks if the user is a staff member, and if so, sets a staff flag to true and deletes
    a form object.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    headers, the user agent, and the request body (if any). It is typically passed as the first argument
    to a
    :param pk: The "pk" parameter in this code refers to the primary key of a specific object in the
    database. It is used to retrieve and manipulate a specific instance of the "FoStaff" model
    :return: If the user is a staff member, the function will update the staff member's status to
    "is_staff = True" and delete the corresponding form object. Then, it will redirect the user to the
    staff profile page with the primary key (pk) of the staff member. If the user is not a staff member,
    the function will redirect them to the home page. Therefore, the function returns a
    """
    if request.user.is_staff:
        form = FoStaff.objects.filter(pk=pk).first()
        if form:
            form.staff.is_staff = True
            form.staff.save()
            form.delete()
        return redirect('staff:sprofile', pk)
    else:
        return redirect('home')

def sdeny(request, pk):
    """
    The function deletes a form object if the user is a staff member and redirects to the staff profile
    page, otherwise it redirects to the home page.
    
    :param request: The request parameter is an object that contains information about the current HTTP
    request, such as the user making the request, the HTTP method used (GET, POST, etc.), and any data
    submitted with the request. It is typically passed as the first argument to a view function in
    Django
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific instance of the FoStaff model. The function is using the pk parameter to retrieve and
    delete a specific instance of the FoStaff model
    :return: If the user is a staff member, the function deletes a form object with the primary key (pk)
    specified in the URL and redirects to the staff profile page with the same primary key. If the user
    is not a staff member, the function redirects to the home page. So, either a redirect to the staff
    profile page or the home page is being returned depending on the user's role.
    """
    if request.user.is_staff:
        form = FoStaff.objects.filter(pk=pk).first()
        if form:
            form.delete()
        return redirect('staff:sprofile', pk)
    else:
        return redirect('home')

def unstrike():
    """
    The function unstrike resets the strikes of users who have strike dates in the past and have at
    least one strike.
    """
    users = Profile.objects.filter(strike_date__lt=timezone.now()).exclude(strikes=0)
    for u in users:
        u.strikes = 0
        u.save()
