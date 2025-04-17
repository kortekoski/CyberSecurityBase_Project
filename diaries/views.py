from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

from diaries.models import User, Entry
from django.db import connection

def index(request):
    if 'user_id' not in request.session:
        return HttpResponseRedirect(reverse("diaries:login"))
    else:
        user_id = request.session['user_id']
        return HttpResponseRedirect(reverse("diaries:profile", args=[user_id]))
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.get(username=username)

        # FLAW 2
        if user.password == password:
        # FLAW 2 FIX
        # if check_password(password, user.password):
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse("diaries:profile", args=[user.id]))
        else:
            error_message = 'incorrect username/password'
            return render(request, 'diaries/login.html', {'error_message': error_message})

    return render(request, 'diaries/login.html')

def logout(request):
    request.session.pop('user_id')

    return HttpResponseRedirect(reverse("diaries:index"))


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # FLAW 2 FIX
        # hashed_password = make_password(password)
        # new_user = User(username=username, password=hashed_password)

        # FLAW 2
        new_user = User(username=username, password=password)


        new_user.save()

        return HttpResponseRedirect(reverse("diaries:index"))

    return render(request, 'diaries/signup.html')

def write(request):
    text = request.POST.get('entry')
    user_id = request.session['user_id']
    entry_user = User.objects.get(id=user_id)
    new_entry = Entry(content=text, pub_date=timezone.now(), user=entry_user)
    new_entry.save()

    return HttpResponseRedirect(reverse("diaries:index"))

def edit(request, entry_id):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except Entry.DoesNotExist:
        raise Http404('Entry not found')
    
    if request.method == 'POST':
        new_content = request.POST.get('new_entry')

        # FLAW 3
        with connection.cursor() as cursor:
            cursor.execute("UPDATE diaries_entry SET content='" + new_content + "' WHERE id= " + str(entry_id) + ";")

        # FLAW 3 FIX
        #entry.content = new_content
        #entry.save()

        session_id = request.session['user_id']

        return HttpResponseRedirect(reverse('diaries:profile', args=[session_id]))

        
    return render(request, 'diaries/edit.html', {'entry': entry})


def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404('User not found')
    
    # FLAW 1 FIX
    # if 'user_id' not in request.session or not user_id == request.session['user_id']:
    #    return HttpResponseForbidden('You do not have the permission to view this page.')

    ## FLAW 1
    entries = Entry.objects.filter(user_id=user_id)
    
    return render(request, 'diaries/profile.html', {'entries': entries})