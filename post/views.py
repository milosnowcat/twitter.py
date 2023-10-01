from django.shortcuts import render, redirect
from .forms import PostForm, OfferForm, TopicForm
from .models import Post, Offer, Topic
from django.contrib.auth.decorators import login_required
from staff.models import RePost, ReOffer
from notifications.views import post as notify, offer as onotify, comment as cnotify
from chat.views import send

OFFER = 'post:offer'
POST = 'post:post'
SOCIAL = 'post:social'
FEED = 'post:feed'

def feed(request):
    """
    This function displays a feed of offers and allows users to create new offers with associated
    topics.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the HTTP method used (GET, POST,
    etc.), any data submitted in the request, and the user's session information
    :return: an HTTP response that renders the 'post/feed.html' template with the context dictionary
    containing the 'offers', 'form', and 'form_t' variables.
    """
    offers = Offer.objects.filter(is_delete=False)
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        form_t = TopicForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.user = request.user
            if request.user.profile.strikes == 0:
                offer.save()
                create_topics(form_t, offer)
                for follower in request.user.profile.followers():
                    onotify(request, follower, offer.pk)
            return redirect(FEED)
    else:
        form = OfferForm()
        form_t = TopicForm()
    context = {'offers':offers, 'form':form, 'form_t':form_t}
    return render(request, 'post/feed.html', context)

def social(request):
    """
    This function displays posts and allows users to create new posts with topics and notifications.
    
    :param request: The request object represents the current HTTP request that the user has made to
    access the web application. It contains information about the user's request, such as the HTTP
    method used (GET, POST, etc.), the requested URL, any submitted data, and more
    :return: an HTTP response that renders the 'post/social.html' template with the context dictionary
    containing the 'posts', 'form', and 'form_t' variables.
    """
    posts = Post.objects.filter(is_delete=False)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        form_t = TopicForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if request.user.profile.strikes == 0:
                post.save()
                create_topics(form_t, post)
                for follower in request.user.profile.followers():
                    notify(request, follower, post.pk)
            return redirect(SOCIAL)
    else:
        form = PostForm()
        form_t = TopicForm()
    context = {'posts':posts, 'form':form, 'form_t':form_t}
    return render(request, 'post/social.html', context)

@login_required
def delete(request, post_id):
    """
    This function deletes a post if the user who made the request is the same as the user who created
    the post.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. In this specific function, the request
    parameter is used to
    :param post_id: The post_id parameter is the unique identifier of the post that the user wants to
    delete. It is used to retrieve the Post object from the database using the get() method of the Post
    model
    :return: a redirect to the `POST` view with the primary key (`pk`) of the deleted post as a
    parameter.
    """
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.is_delete = True
        post.save()
    return redirect(POST, post.pk)

@login_required
def odelete(request, offer_id):
    """
    This function deletes an offer if the user who created it is the one making the request.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. In this function, the request parameter
    is used to determine
    :param offer_id: offer_id is a parameter that represents the unique identifier of an Offer object.
    It is used to retrieve the specific Offer object from the database using the get() method of the
    Offer model
    :return: a redirect to the `OFFER` page with the primary key (`pk`) of the deleted offer as a
    parameter.
    """
    offer = Offer.objects.get(id=offer_id)
    if offer.user == request.user:
        offer.is_delete = True
        offer.save()
    return redirect(OFFER, offer.pk)

@login_required
def like(request, pk):
    """
    This function allows a user to like or unlike a post, but only if they have less than or equal to 2
    strikes on their profile.
    
    :param request: The request parameter is an object that contains information about the current
    request, including the user making the request, the HTTP method used, and any data submitted with
    the request. It is typically passed to a view function in Django
    :param pk: pk is a parameter that stands for "primary key". In Django, primary keys are unique
    identifiers assigned to each instance of a model. In this case, pk is used to identify a specific
    Post object in the database
    :return: a redirect to the `POST` view with the primary key `pk` as a parameter.
    """
    post = Post.objects.get(pk=pk)
    is_like = False
    for like in post.likes.all():
        if like == request.user:
            is_like = True
            break
    if request.user.profile.strikes <= 2:
        if not is_like:
            post.likes.add(request.user)
        if is_like:
            post.likes.remove(request.user)
    return redirect(POST, pk)

@login_required
def olike(request, pk):
    """
    This function allows a user to like or unlike an offer, but only if they have less than or equal to
    2 strikes on their profile.
    
    :param request: The request parameter is an object that contains information about the current
    request, including the user making the request, the HTTP method used, and any data submitted with
    the request. It is typically passed to a view function in Django
    :param pk: pk is a parameter that represents the primary key of an Offer object. It is used to
    retrieve the specific Offer object from the database
    :return: a redirect to the OFFER page with the primary key (pk) of the offer that was just liked or
    unliked.
    """
    offer = Offer.objects.get(pk=pk)
    is_like = False
    for like in offer.likes.all():
        if like == request.user:
            is_like = True
            break
    if request.user.profile.strikes <= 2:
        if not is_like:
            offer.likes.add(request.user)
        if is_like:
            offer.likes.remove(request.user)
    return redirect(OFFER, pk)

def offer(request, pk):
    """
    The function checks if a user is blocked and redirects them if they are, otherwise it renders an
    offer page.
    
    :param request: The request parameter is an object that represents the HTTP request made by the
    client to the server. It contains information such as the HTTP method used (GET, POST, etc.), the
    URL requested, any data submitted in the request, and more. The view function uses this object to
    determine how to respond
    :param pk: pk stands for "primary key". In this context, it refers to the unique identifier of a
    specific Offer object in the database. The function retrieves the Offer object with the given
    primary key using the `Offer.objects.get(pk=pk)` method
    :return: If the user who created the offer is in the current user's blocking list or blocked list,
    the function will redirect to the FEED page. Otherwise, it will render the 'offer.html' template
    with the offer object passed in the context dictionary.
    """
    offer = Offer.objects.get(pk=pk)
    if offer.user in request.user.profile.blocking() or offer.user in request.user.profile.blocked():
        return redirect(FEED)
    else:
        context = {'offer':offer}
        return render(request, 'post/offer.html', context)

def post(request, pk):
    """
    This function handles the creation and display of comments on a post, with additional checks for
    blocked users.
    
    :param request: The HTTP request object that contains metadata about the request being made, such as
    the user agent, headers, and data
    :param pk: pk is a parameter that represents the primary key of a Post object. It is used to
    retrieve a specific Post object from the database
    :return: a HTTP response, either a redirect to the SOCIAL page if the post user is in the requesting
    user's blocking or blocked list, or a rendered HTML template with the post, comments, and forms for
    creating a new comment and topic.
    """
    post = Post.objects.get(pk=pk)
    if post.user in request.user.profile.blocking() or post.user in request.user.profile.blocked():
        return redirect(SOCIAL)
    else:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            form_t = TopicForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.comment = post
                if request.user.profile.strikes == 0:
                    new_comment.save()
                    create_topics(form_t, new_comment)
                    cnotify(request, post.user, new_comment.pk)
                return redirect(POST, post.pk)
        else:
            form = PostForm()
            form_t = TopicForm()
        comments = Post.objects.filter(comment=post, is_delete=False).order_by('-timestamp')
        context = {'post':post, 'form':form, 'comments':comments, 'form_t':form_t}
        return render(request, 'post/post.html', context)

def topics(request, name):
    """
    This function retrieves all posts associated with a given topic and renders them on a topic-specific
    page.
    
    :param request: The HTTP request object that contains information about the current request, such as
    the user agent, headers, and data
    :param name: The name parameter is a string that represents the name of a topic. It is used to
    filter the Topic objects to find the specific topic that the user is interested in
    :return: This function returns a rendered HTML template with a context dictionary containing posts
    and the topic object filtered by the name parameter passed in the URL. If the tag object is not
    found, it redirects to the SOCIAL page.
    """
    tag = Topic.objects.filter(name=name).first()
    if tag:
        posts = Post.objects.filter(is_delete=False, topics__in=[tag])
    else:
        return redirect(SOCIAL)
    context = {'posts':posts,'topic':tag}
    return render(request, 'post/topic.html', context)

def otopics(request, name):
    """
    This function retrieves offers related to a specific topic and renders them on a topic page.
    
    :param request: The request parameter is an HttpRequest object that represents the current request
    made by the user to the server. It contains information about the request, such as the HTTP method
    used, the headers, the user agent, and the request body. It is passed to the view function by
    Django's URL routing system
    :param name: The "name" parameter is a string that represents the name of a topic. It is used to
    filter the Topic objects and find the specific topic that matches the given name. Once the topic is
    found, the function filters the Offer objects that have this topic and returns them in the context
    dictionary to be
    :return: This function returns a rendered HTML template with a context dictionary containing the
    offers related to a specific topic. If the topic does not exist, the user is redirected to the FEED
    page.
    """
    tag = Topic.objects.filter(name=name).first()
    if tag:
        offers = Offer.objects.filter(is_delete=False, topics__in=[tag])
    else:
        return redirect(FEED)
    context = {'offers':offers}
    return render(request, 'post/topic.html', context)

@login_required
def report(request, pk):
    """
    This function reports a post and adds the user who reported it to the list of those who reported it.
    
    :param request: The request object represents the current HTTP request that the user has made to the
    server. It contains information about the user's request, such as the URL, headers, and any data
    that was submitted with the request
    :param pk: pk is a parameter that represents the primary key of a Post object. It is used to
    retrieve a specific Post object from the database and perform operations on it, such as creating a
    RePost object or adding a user to the list of users who have reported the post
    :return: a redirect to the POST view with the primary key (pk) of the post that was reported.
    """
    post = Post.objects.filter(pk=pk, is_delete=False).first()
    report = RePost.objects.filter(post=post).first()
    if report:
        report.reported_by.add(request.user.pk)
        report.save()
    else:
        if post:
            new_report = RePost.objects.create(post=post)
            new_report.reported_by.add(request.user.pk)
            new_report.save()
    return redirect(POST, pk)

@login_required
def oreport(request, pk):
    """
    This function allows a user to report an offer and adds the user to the list of those who have
    reported it.
    
    :param request: The request object represents the HTTP request that the user has made to the server.
    It contains information such as the user's browser information, the requested URL, and any data that
    was submitted with the request
    :param pk: "pk" is an abbreviation for "primary key". In Django, it is a unique identifier for each
    record in a database table. In this specific code snippet, "pk" is used as a parameter to identify a
    specific offer object in the Offer model
    :return: a redirect to the OFFER view with the primary key (pk) of the offer as a parameter.
    """
    offer = Offer.objects.filter(pk=pk, is_delete=False).first()
    report = ReOffer.objects.filter(offer=offer).first()
    if report:
        report.reported_by.add(request.user.pk)
        report.save()
    else:
        if offer:
            new_report = ReOffer.objects.create(offer=offer)
            new_report.reported_by.add(request.user.pk)
            new_report.save()
    return redirect(OFFER, pk)

@login_required
def apply(request, pk):
    """
    This function sends a message to the user who created an offer and redirects the current user to
    their inbox.
    
    :param request: The request object represents the current HTTP request that the user has made. It
    contains information about the user's request, such as the HTTP method used, the URL requested, any
    data submitted in the request, and more
    :param pk: `pk` is a variable that stands for "primary key". In this context, it refers to the
    primary key of an `Offer` object that is being filtered for in the database. The `first()` method is
    used to retrieve the first `Offer` object that matches the filter criteria
    :return: a redirect to the 'chat:inbox' URL with the offer user as a parameter.
    """
    offer = Offer.objects.filter(pk=pk, is_delete=False).first()
    message = request.scheme + "://" + request.META['HTTP_HOST'] + redirect(OFFER, offer.pk).url
    send(request, request.user, offer.user, message, None, False)
    return redirect('chat:inbox', offer.user)

def create_topics(form, post):
    """
    This function creates topics for a post by splitting the post's name into words, filtering out
    non-alphanumeric characters, and checking if a topic with that name already exists. If it does, the
    post is associated with that topic, otherwise a new topic is created and associated with the post.
    
    :param form: The form parameter is an instance of a Django form that is used to create or update a
    Topic object
    :param post: The "post" parameter is likely an instance of a model representing a post or message in
    a forum or discussion board. The code is adding topics to this post based on the words in the topic
    name entered in a form
    """
    if form.is_valid:
        t = form.save(commit=False)
        for word in t.name.split():
            new_word = ''.join(filter(str.isalnum, word))
            topic = Topic.objects.filter(name=new_word).first()
            if topic:
                post.topics.add(topic.pk)
            else:
                topic = Topic(name=new_word)
                topic.save()
                post.topics.add(topic.pk)
