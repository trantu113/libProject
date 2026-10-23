from datetime import datetime, timezone, tzinfo, timedelta

from bson import ObjectId
from bson.errors import InvalidId
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.shortcuts import render, redirect

from books.db import books_collection, borrows_collection

dt_utc = datetime.fromtimestamp(1700000000, timezone.utc)
vietnam_tz = timezone(timedelta(hours=7))
dt_vn = dt_utc.astimezone(vietnam_tz)

def books(request):
    q = request.GET.get('q', '').strip()

    con_hang = request.GET.get('con_hang', '')

    cacDieuKien = []

    if q:  # neu q = true
        cacDieuKien.append({
            '$or': [
                {'title': {'$regex': q, '$options': 'i'}},
                {'author': {'$regex': q, '$options': 'i'}},
            ]
        })

    if con_hang:
        cacDieuKien.append({'available': {'$gt': 0}})

    if (cacDieuKien):
        dieuKien = {'$and': cacDieuKien}
    else:
        dieuKien = {}

    cursor = books_collection.find(dieuKien)  # lay du lieu tu mongodb

    book_list = []
    for item in cursor:
        item['id'] = str(item['_id'])  # chuyen ma _id trong mongo thanh (string)
        book_list.append(item)

    context = {'book_list': book_list, 'q': q, 'con_hang': con_hang}  # dong goi gui sang html

    return render(request, 'books/book_list.html', context)


@staff_member_required
def bookAdd(request):
    if request.method == 'POST':  # nguoi dung bam "save"
        try:
            available = int(request.POST.get('available', 0))
        except:
            available = 0

        books_collection.insert_one({  # lenh insert_one
            'title': request.POST.get('title', '').strip(),
            'author': request.POST.get('author', '').strip(),
            'category': request.POST.get('category', '').strip(),
            'available': max(available, 0),  # dam bao ko co so luong la am
        })
        return redirect('books')  # back ve trang danh sach

    return render(request, 'books/book_form.html')  # vao trang book_form


@staff_member_required
def bookDelete(request, book_id):
    if request.method == 'POST':  # nguoi dung bam "delete"
        books_collection.delete_one({'_id': ObjectId(book_id)})  # lenh delete_one (ObjectId(book_id)
    return redirect('books')


@staff_member_required
def bookUpdate(request, book_id):
    book = books_collection.find_one({'_id': ObjectId(book_id)})

    if request.method == 'POST':
        try:
            available = int(request.POST.get('available', 0))
        except ValueError:
            available = 0

        books_collection.update_one({'_id': book['_id']},
                                    {'$set': {
                                        'title': request.POST.get('title', '').strip(),
                                        'author': request.POST.get('author', '').strip(),
                                        'category': request.POST.get('category', '').strip(),
                                        'available': max(available, 0),
                                    }}, )
        return redirect('books')

    book['id'] = str(book['_id'])
    return render(request, 'books/book_form.html', {'book': book})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('books')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def borrowRequest(request, book_id):
    if request.method != 'POST':
        return redirect('books')

    try:
        book = books_collection.find_one({'_id': ObjectId(book_id)})
    except InvalidId:
        raise Http404
    if book is None:
        raise Http404

    daCo = borrows_collection.find_one(
        {
            'user_id': request.user.id,
            'book_id': book['_id'],
            'status': {'$in': ['pending', 'borrowed']},
        })

    if daCo:
        messages.warning(request, 'Bạn đã gửi yêu cầu hoặc đang mượn quyển này.')
    # elif book['available'] <= 0:
    # messages.error(request, "Hiện đã hết sách này!")
    else:
        borrows_collection.insert_one({
            'user_id': request.user.id,
            'username': request.user.username,
            'book_id': book['_id'],
            'book_title': book['title'],
            'status': 'pending',
            'requested_at': datetime.now(vietnam_tz),  # luu file ko dung mui gio Viet Nam
        })
        messages.success(request, 'Đã gửi yêu cầu.')
    return redirect('books')


@login_required
def myBooks(request):
    cursor = borrows_collection.find({'user_id': request.user.id}).sort('requested_at', -1)

    borrow_list = []
    for item in cursor:
        item['id'] = str(item['_id'])
        borrow_list.append(item)

    return render(request, 'books/my_books.html', {'borrow_list': borrow_list})
