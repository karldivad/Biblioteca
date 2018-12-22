from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Book

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
        'picture': auth0user.extra_data['picture']
    }

    books_list = Book.objects.all().order_by('title')
    paginator = Paginator(books_list, 3)
    #print(books)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    print(books_list[0].authors.all())

    args = {'auth0User': auth0user, 'books': books}

    return render(request, 'dashboard.html', args)
