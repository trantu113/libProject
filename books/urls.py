from django.urls import path

from books import views

urlpatterns = [
    path('', views.books, name='books'),  # trang books
    path('add/', views.bookAdd, name='bookAdd'),  # trang add book
    path('delete/<str:book_id>/', views.bookDelete, name='bookDelete'),
    path('update/<str:book_id>/', views.bookUpdate, name='bookUpdate'),
    path('borrow/<str:book_id>/', views.borrowRequest, name='borrowRequest'),
    path('my-books/', views.myBooks, name='myBooks'),
    path('staff/borrows/', views.borrowManage, name='borrowManage'),
    path('staff/borrows/<str:borrow_id>/approve/', views.borrowApprove, name='borrowApprove'),
    path('staff/borrows/<str:borrow_id>/reject/', views.borrowReject, name='borrowReject'),
    path('staff/borrows/<str:borrow_id>/return/', views.borrowReturn, name='borrowReturn'),
    path('staff/history/', views.borrowHistory, name='borrowHistory'),
    path('qr/<str:borrow_id>/', views.borrowQR, name='borrowQR'),
    path('staff/borrows/<str:borrow_id>/scan/', views.borrowScan, name='borrowScan'),
]
