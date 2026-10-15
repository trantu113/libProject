from django.shortcuts import render, redirect
from matplotlib.style import available

from books.db import books_collection


def books(request):
    cursor = books_collection.find({})  # lay du lieu tu mongodb

    book_list = []
    for item in cursor:
        item['id'] = str(item['_id'])  # chuyen ma _id trong mongo thanh (string)
        book_list.append(item)

    context = {'book_list': book_list}  # dong goi gui sang html

    return render(request, 'books/book_list.html', context)


def bookAdd(request):
    if request.method == 'POST': # nguoi dung bam "save"
        try:
            available = int(request.POST.get('available', 0))
        except:
            available = 0

        books_collection.insert_one({
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'category': request.POST.get('category'),
            'available': int(request.POST.get('available', 0)),
        })
        return redirect('books') # back ve trang danh sach

    return render(request, 'books/book_form.html') # vao trang book_form
