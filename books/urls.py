from django.urls import path

from books import views

urlpatterns = [
    path('', views.books, name='books'), # trang books
    path('add/', views.bookAdd, name='bookAdd'), # trang add book
    path('delete/<str:book_id>/',views.bookDelete, name='bookDelete'),
    path('update/<str:book_id>/',views.bookUpdate, name='bookUpdate'),
    path('borrow/<str:book_id>/', views.borrowRequest, name='borrowRequest'),
]