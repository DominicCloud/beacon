from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from primary.models import Profile, Post
from datetime import datetime, timedelta
from django.core.mail import send_mail

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect('/log-in')
    
    start_date = (datetime.now() + timedelta(days=8)).date()

    new_file = []

    list_of_posts = Post.objects.all()
    for p in list_of_posts:
 
        if p.sdate.date() == start_date:
            new_file.append(p.title)
    
    return render(request, 'index.html', {'start':start_date, 'list_of_posts':new_file})

def loginUser(request):
    if request.method == 'POST':
        print("Function started")
        name = request.POST.get('name')
        password = request.POST.get('password')
        #print(name, password)
        user = authenticate(username=name, password=password)
        
        print('user authenticated! user is', user)

        if user is not None:
            login(request, user)
            return redirect('/')
    # A backend authenticated the credentials
        else:
            return render(request, 'loginpage.html')
    # No backend authenticated the credentials
    return render(request, 'loginpage.html')

def logoutUser(request):
    logout(request)
    return redirect('/log-in')

def registerUser(request):
    if not request.user.is_anonymous:
        logout(request)
        
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        college = request.POST.get('college')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        isAdminString = request.POST.get('isAdmin')
        isAdmin = bool(isAdminString)

        print(username, email, college, phone, password1, password2)


        if password1!=password2 or User.objects.filter(username=username).exists():
            messages.info(request, 'Hey there, fill out the info properly!')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()
            Profile.objects.create(user=user, college=college, phone=phone, isAdmin = isAdmin)

            user = authenticate(username=username, password=password1)
            login(request, user)

            return redirect('/')
    return render(request, 'register.html')

def trending_events(request):
    list_of_posts = Post.objects.all()
    return render(request, 'trending_events.html', {'list_of_posts':list_of_posts})

def design(request):
    for x in Profile.objects.filter(user = request.user):
        if not x.isAdmin:
            messages.warning(request, f'Sorry {x.user.username}, you do not seem to have the rights to do that :( ... Here, check out our trending events instead :D')
            return redirect ('trending_events')


    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        post_images = request.FILES.get('post_images')
        caption = request.POST.get('event_caption')
        college = request.POST.get('college')
        description = request.POST.get('decription')
        sdate_str = request.POST.get('sdate')
        sdate = datetime.strptime(sdate_str, '%Y-%m-%dT%H:%M')
        edate_str = request.POST.get('edate')
        edate = datetime.strptime(edate_str, '%Y-%m-%dT%H:%M')

        print(event_title, college, caption, sdate, edate)

        if post_images:
            Post.objects.create(title=event_title, caption=caption, description=description, college=college, sdate=sdate, edate=edate, post_images=post_images)
        else:
            Post.objects.create(title=event_title, caption=caption, description=description, college=college, sdate=sdate, edate=edate)

        # Send a notification to all users about this event

        messages.success(request, 'POST CREATED!')

        p_list = Profile.objects.all()
        list_of_emails = []
        for p in p_list:
            list_of_emails.append(p.user.email)

        print(list_of_emails)
        email_body = f"Hello There!\nJust wanted to let you know that \n{event_title} : {caption} \norganized by {college} is coming up. Come check it out on our website!"

        send_mail(
            "MESSAGE FROM BEACON", # subject
            email_body, # body
            'beaconcen@gmail.com', # from_mail
            list_of_emails, # list of to_mails
        )

        return redirect('/')
    return render(request, 'design.html')

def interestedevents(request):
    posts = Post.objects.all()
    return render(request, 'interested.html', {'list_of_posts':posts})