from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db.models import Q
from .models import Book, BookContent
from .forms import BookForm, BookFormAdd, AuthorFormAdd
import base64

import json


def index(request):
    if request.user.is_authenticated:
        return redirect("dashboard/")
    return render(request, 'index.html')


@login_required
def dashboard(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')

    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture'],
        'role': auth0user.extra_data['role']
    }

    #print(user.https://rules)

    form = BookForm(request.POST)

    """books_list = Book.objects.all().order_by('title')
    paginator = Paginator(books_list, 3)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    args = {'auth0User': auth0user, 'books': books, 'form': form}"""

    if form.is_valid():

        title_q = form.cleaned_data['title']
        year_q = form.cleaned_data['year']
        author_q = form.cleaned_data['author']

        books_list = Book.objects.all()

        if year_q :
            books_list = books_list.filter(content={'year': year_q})
        if title_q != "" :
            books_list = books_list.filter(title__icontains='.' + title_q + '.')

        if author_q != "":
            books_list = books_list.filter(authors__name__icontains=author_q)

        books_list = books_list.order_by('title')

        paginator = Paginator(books_list, 3)
        page = request.GET.get('page')
        books = paginator.get_page(page)

        args = {'auth0User': auth0user, 'books': books, 'form': form}
        return render(request, 'dashboard.html', args)

    return render(request, 'dashboard.html')


def handle_uploaded_file(f):
    return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf8')

@login_required
def bookadd(request):

    form = BookFormAdd(request.POST, request.FILES)

    if form.is_valid() and request.method == 'POST':
        title_q = form.cleaned_data['title']
        year_q = form.cleaned_data['year']
        edition_q = form.cleaned_data['edition']
        base64_img = handle_uploaded_file(request.FILES['image'])
        copies_q = form.cleaned_data['copies']
        rating_q = form.cleaned_data['rating']
        authors_q = form.cleaned_data['authors']

        if title_q != "" and year_q  and edition_q and base64_img and copies_q and rating_q and authors_q != []:
            newCon = BookContent(year=year_q, edition=edition_q, image=base64_img, copies=copies_q, rating=rating_q)
            newB = Book(title=title_q, content=newCon)
            newB.save()
            for i in authors_q:
                newB.authors.add(i)
            newB.save()
            return redirect("/dashboard")

        return render(request, 'bookadd.html', {'form': form})
    return render(request, 'bookadd.html', {'form': form})

@login_required
def bookdelete(request,id):
    Book.objects.get(pk=id).delete()
    #Book.objects.filter(Book=book).delete()
    return redirect("/dashboard")


@login_required
def bookedit(request, id):

    bookref = Book.objects.get(pk=id)

    data = {'title': bookref.title, 'year': bookref.content.year, 'edition': bookref.content.edition, 'copies': bookref.content.copies, 'rating': bookref.content.rating, 'authors': [s.pk for s in list(bookref.authors.all())]}

    form = BookFormAdd(initial=data)

    if request.method == 'POST':
        title_q = request.POST.get('title')
        year_q = request.POST.get('year')
        edition_q = request.POST.get('edition')
        hay_imagen = False
        try:
            base64_img = handle_uploaded_file(request.FILES['image'])
            hay_imagen = True
        except MultiValueDictKeyError:
            hay_imagen = False


        copies_q = request.POST.get('copies')
        rating_q = request.POST.get('rating')
        authors_q = request.POST.get('authors')

        if title_q != "" and year_q  and edition_q and copies_q and rating_q and authors_q != []:
            bookref.title = title_q
            bookref.content.year = year_q
            bookref.content.edition = edition_q
            bookref.content.copies = copies_q
            bookref.content.rating = rating_q
            bookref.save()
            bookref.authors.clear()
            for i in authors_q:
                bookref.authors.add(i)
            bookref.save()
            return redirect("/dashboard")

        return render(request, 'bookedit.html', {'form': form, 'data': data})
    return render(request, 'bookedit.html', {'form': form, 'data': data})

