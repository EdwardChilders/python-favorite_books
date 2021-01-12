from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# renders

def index(request):
    return render(request, 'index.html')


def books(request):
    if 'uuid' not in request.session:
        return redirect('/')
    user_logged = User.objects.get(id=request.session['uuid'])
    context = {
        'user': user_logged,
        'all_books': Book.objects.all()
    }
    return render(request, 'books.html', context)


def view_book(request, b_id):
    if 'uuid' not in request.session:
        return redirect('/')
    user_logged = User.objects.get(id=request.session['uuid'])
    context = {
        'user': user_logged,
        'book': Book.objects.get(id=b_id)
    }
    return render(request, 'viewed_book.html', context)

# redirects

def register(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_browns)
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_browns
        )
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/books')


def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/books')


def logout(request):
    request.session.flush()
    return redirect('/')


def add_book(request):
    print(request.POST)
    errors = User.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    else:
        user_logged = User.objects.get(id=request.session['uuid'])
        book_created = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['description'],
            uploaded_by_id_one = user_logged
        )
        book_created.favorites_by_many.add(user_logged)

    return redirect('/books')


def add_favorite(request, b_id):
    user_logged = User.objects.get(id=request.session['uuid'])
    book = Book.objects.get(id=b_id)
    book.favorites_by_many.add(user_logged)
    return redirect('/books')


def remove_favorite(request, b_id):
    user_logged = User.objects.get(id=request.session['uuid'])
    book = Book.objects.get(id=b_id)
    book.favorites_by_many.remove(user_logged)
    return redirect(f'/books/{book.id}')


def update_book(request, b_id):
    print(request.POST)
    errors = User.objects.book_validator(request.POST)
    book = Book.objects.get(id=b_id)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book.id}')
    else:
        book.title = request.POST['title']
        book.desc = request.POST['description']
        book.save()
    return redirect('/books')


def delete_book(request, b_id):
    delete_book = Book.objects.get(id=b_id)
    delete_book.delete()
    return redirect('/books')
