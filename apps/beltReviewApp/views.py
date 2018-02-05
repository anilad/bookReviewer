from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import datetime

def index(request):
    if not 'id' in request.session:
        request.session['id'] = None
    if not 'name' in request.session:
        request.session['name']=None
    if request.session['id'] != None:
        return redirect ('/books')
    else:
        return render(request, "beltReviewApp/index.html")
    
def login(request):
    result = User.objects.valLogin(request.POST)
    if result[0]:
        request.session['id'] = result[1].id
        request.session['name'] = result[1].first_name
        context={
            "books": Book.objects.all(),
            "user": result[1]
        }
        print "session id", request.session['id']
        print "session name", request.session['name']

        return redirect('/books', context)
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')

def register(request):
    if request.session['id'] != None:
        return redirect ('/books')
    else:
        context={
            "max": datetime.today().strftime('%Y-%m-%d')
        }
        return render(request, "beltReviewApp/registration.html", context)

def process(request):
    result = User.objects.valCreate(request.POST)
    if result[0]:
        request.session['id'] = result[1].id;
        return redirect('/books')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/register')

def books(request):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        # code here to display reviewed and not reviewed books info if number in url is valid
        context={
            "books": Book.objects.all(),
            "recent": Rating.objects.all().order_by('-created_at')[:3]
        }
        return render(request, "beltReviewApp/bookHome.html", context)

def bookDisplay(request, number):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        # code here to displaybooks info if number in url is valid
        context={
            "book": Book.objects.get(id=number),
            "ratings": Rating.objects.filter(rated_book__id__contains=number),
        }
        return render(request, "beltReviewApp/book.html", context)

def user(request, number):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        # code here to display all user info if number in url is valid
        context = {
            "user": User.objects.get(id=number),
            "ratings": Rating.objects.filter(rater__id__contains=number)
        }
        return render(request, "beltReviewApp/user.html", context)

def update(request, number):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        context={
            "user":User.objects.get(id=number)
        }
        return render(request, "beltReviewApp/userUpdate.html", context)

def userUpdate(request, number):
    result = User.objects.valUserUpdate(request.POST, number)
    if result[0]:
        return redirect('/users/'+number)
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/users/'+number+'/update')
    # code to validate updating user info and redirect to correct page

def deleteUser(request, number):
    pass
    # code to delete user
    return redirect('/')

def add(request):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        context={
            "authors": Author.objects.all()
        }
        return render(request, "beltReviewApp/add.html", context)

def check(request):
    result = User.objects.valBook(request.POST, request.session['id'])
    if result[0]:
        return redirect('/books')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/add')

def review(request, number):
    result = User.objects.valReview(request.POST, request.session['id'], number)
    if result[0]:
        return redirect('/books/'+number)
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/books/'+number)

def delete(request, number):
    User.objects.delete(number)
    request.session.clear()
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')