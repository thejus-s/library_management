from django.http import Http404
from django.shortcuts import redirect, render,get_object_or_404
from adminApp.models import *
from .models import *
from datetime import date,timedelta
from django.db.models import Count

def index(request):
    print(request.session.get('userid'))
    books = Books.objects.all().order_by('-id')
    popbooks = Books.objects.all().annotate(borrow_count = Count('book_borrows')).order_by('-borrow_count')
    newbooks = books[:2]
    fbook = books[:4]
    context = {
        'books':books,
        'newbooks':newbooks,
        "popular_books":popbooks,
        'featured_books':fbook
    }
    return render(request,'index.html',context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = get_object_or_404(User,email=email,password=password)
            if user.role == 'User':
                request.session['userid'] = user.id
                return redirect("index")
            elif user.role == 'Admin':
                request.session['adminid'] = user.id
                return redirect('admindash')
        except Http404 :
            return render(request,'login.html',{'error':"Invalid email or password."})
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            return render(request,'Register.html',{'error':'Email already exist.'})
        User.objects.create(
            fname = fname,
            lname = lname,
            email = email,
            phone = phone,
            password = password
        )
        return redirect('login')
    return render(request,'Register.html')

def allbooks(request):
    books = Books.objects.all().order_by("-id")
    context = {
        "books":books,
    }
    return render(request,'allbooks.html',context)

def borrow(request,slug):
    # print(slug)
    userid = request.session.get('userid')
    book = get_object_or_404(Books,slug=slug)
    user = get_object_or_404(User,id=userid)
    try:
        Borrows.objects.create(
            book=book,
            user=user,
            return_date = date.today()+timedelta(days=15)
        )
        book.copies-=1
        book.save()
    except Exception as e:
        print(e)
    return redirect('profile')

def returnbook(request,bid):
    borrow = get_object_or_404(Borrows,id=bid)
    if borrow:
        borrow.book.copies+=1
        borrow.returned_at = date.today()
        borrow.status = True
        borrow.book.save()
        borrow.save()
        return redirect('profile')
    return redirect('profile')

def searchbook(request):
    if request.method == 'POST':
        keyword = request.POST.get('search','').strip()
        if keyword:
            books = Books.objects.filter(title__icontains = keyword)
            return render(request,'allbooks.html',{'books':books})
    return redirect('allbooks')

def userprofile(request):
    userid = request.session.get('userid')
    user = get_object_or_404(User,id=userid)
    borrowedbook = user.user_borrows.all().order_by('-id')
    returnbookcount= borrowedbook.filter(user=user,status=False).count()
    # print(bo)
    context={
        'user':user,
        'borrowedbook':borrowedbook,
        'returnbookcount':returnbookcount
    }
    return render(request,'userprofile.html',context)

def editprofile(request):
    user = get_object_or_404(User,id=request.session.get('userid'))
    if request.method == "POST":
        user.fname = request.POST.get('fname')
        user.lname = request.POST.get('lname')
        if User.objects.filter(email=request.POST.get('email')).exists() and user.email != request.POST.get('email'):
            return render(request,'editprofile.html',{'error':'Email already exist.'})
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.password = request.POST.get('password')
        user.save()
        return redirect('profile')
    return render(request,'editprofile.html',{'user':user})

def logout(request):
    if 'userid' in request.session:
        del request.session['userid']
        return redirect('index')