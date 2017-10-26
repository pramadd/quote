from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request,'quotes/index.html')

def quotes(request):
    context = {}
    context['quotes'] = User.objects.all()
    return render(request,'quotes/quotes.html',context)

def register(request):
    Name = request.POST['Name']
    Alias = request.POST['Alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    context = {'Name': Name,'Alias': Alias, 'email': email, 'password': password, 'confirm_password': confirm_password}
    errors = User.objects.validate(context)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(Name = Name, Alias = Alias, email = email, password = hashed_password )
        return redirect('/quotes')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    print "inside login"
    
    errors = User.objects.validateLogin(request.POST)
    print errors
    if errors:
        print "heres"
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print "redirecting to root"
        return redirect('/')
    else:
        user = User.objects.filter(email = email)[0]
        request.session['id'] = user.id
        return redirect('/quotes')




def add(request):
    author = request.POST['author']
    info = request.POST['info']
    currentUser = User.objects.get(id = request.session['id'])
    context = {
        'author': author,
        'info': info,
    }
    errors = Quote.objects.validate(context)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else:
        Quote.objects.create(author = author, info = info, uploader = currentUser)
    return redirect('/quotes')  


def logout(request):
    request.session['id'] = ""
    return redirect('/')  


def quotes(request):
    try:
        print 'try'
        request.session['id']
    except KeyError:
        print'nah'
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    # read
    context = {
        'user': user,
        'quotes': Quote.objects.all(),
        'liked': Quote.objects.filter(authors = request.session['id'])
    }
    print context['liked']
    return render(request, "quotes/quotes.html", context)

def users(request, number):
    
    context = {}
    theUser = User.objects.get(id = number)
    context['quotes'] = theUser
    context['tot'] = len(Quote.objects.filter(uploader = theUser))
    context['quotes'] = Quote.objects.filter(uploader = theUser)
    return render(request, 'quotes/user.html', context)

def favourite(request, number):
    print "Pranu"
    user = User.objects.get(id = request.session['id'])
    print user
    quote = Quote.objects.get(id = number)
    print quote
    quote.authors.add(user)
    quote.save()
    print quote
    
    return redirect('/quotes')

def remove(request, number):
    user = User.objects.get(id = request.session['id'])
    quote = Quote.objects.get(id = number)
    quote.authors.remove(user)
    quote.save()
    
    return redirect('/quotes')