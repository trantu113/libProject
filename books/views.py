from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def books(request):
    return render(request, "books/book_list.html") # locate book_list html