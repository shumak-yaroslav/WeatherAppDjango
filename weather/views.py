import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .models import City, Book
from .forms import CityForm, BooksForm
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy



def index(request):
    appid = 'f46d79c27b583ccb65a25ba89f055e8c'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"]
        }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'weather/upload.html', context)

def books_list(request):
    books = Book.objects.all()
    return render(request, 'weather/book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BooksForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return  redirect('book_list')
    else:
        form = BooksForm()
    return render(request, 'weather/upload_book.html', {
        'form': form
    })

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return  redirect('book_list')

class BookListView(ListView):
    model = Book
    template_name = 'weather/class_book_list.html'
    context_object_name = 'books'

class UploadBookView(CreateView):
    model = Book
    form_class = BooksForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'weather/upload_book.html'

