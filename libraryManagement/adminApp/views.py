from django.shortcuts import redirect, render,get_object_or_404
from .models import *
from userApp.models import *
from datetime import date,timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def admindash(request):
    books = Books.objects.all().order_by('-id')
    dbooks = books[:4]
    users = User.objects.all().order_by('-id')
    borrows = Borrows.objects.all().order_by('-id')
    overduebooks = borrows.filter(return_date = date.today(),status = False)
    context = {
        'books':books,
        'users':users,
        'borrows':borrows,
        'overduebooks':overduebooks,
        'dbooks':dbooks
    }
    return render(request,'admindash.html',context)

def adminallbooks(request):
    books = Books.objects.all().order_by('-id')
    return render(request,'adminallbooks.html',{'books':books})

def addbooks(request):
    cat = category.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        isbn = request.POST.get('isbn')
        images = request.FILES.get('images')
        copies = request.POST.get('copies')
        categorys = request.POST.get('category')
        des = request.POST.get('description')
        author = request.POST.get('author')
        catobj = get_object_or_404(category,slug=categorys)
        Books.objects.create(
            title = title,
            ISBN = isbn,
            author = author,
            image = images,
            copies =copies,
            description = des,
            category =catobj
        )
        return redirect('viewbooks')
    return render(request,'addbooks.html',{"category":cat})

def editbook(request,slug):
    cat = category.objects.all()
    book = get_object_or_404(Books,slug=slug)
    if request.method == 'POST':
        categorys = request.POST.get('category')
        catobj = get_object_or_404(category,slug=categorys)
        book.title = request.POST.get('title')
        book.ISBN = request.POST.get('isbn')
        if request.FILES.get('images'):
            book.image = request.FILES.get('images')
        book.copies = request.POST.get('copies')
        book.description = request.POST.get('description')
        book.author = request.POST.get('author')
        book.category = catobj
        book.save()
        return redirect('viewbooks')
    return render(request,'editbook.html',{'category':cat,'book':book})

def deletebook(request,slug):
    book = get_object_or_404(Books,slug=slug)
    book.delete()
    return redirect('viewbooks')

def deleteuser(request,id):
    user = get_object_or_404(User,id=id)
    user.delete()
    return redirect('admindash')

def adminsearchbook(request):
    if request.method == 'POST':
        keyword = request.POST.get('search','').strip()
        if keyword:
            books = Books.objects.filter(title__icontains = keyword)
            return render(request,'adminallbooks.html',{'books':books})
    return redirect('adminallbooks')

def overduebooks(request):
    overdue_users = Borrows.objects.filter(return_date=date.today(), status=False).values_list('user', flat=True).distinct()

    for user_id in overdue_users:
        # Get only overdue books for this specific user
        user_books = Borrows.objects.filter(user_id=user_id, return_date=date.today(), status=False)
        user_email = user_books[0].user.email  # Get the user's email

        if user_email:
            subject = "Library Book Overdue Notice"

            # Pass only the user's books to the template
            html_content = render_to_string('email.html', {'books': user_books, 'user': user_books[0].user})
            text_content = strip_tags(html_content)

            # Send email to the user with their overdue books only
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user_email],  # Send email directly to user
                reply_to=[settings.EMAIL_HOST_USER]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

    return render(request, 'overduebooks.html', {'books': Borrows.objects.filter(return_date=date.today(), status=False)})

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        return redirect('index')