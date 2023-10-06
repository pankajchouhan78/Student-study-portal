from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Notes, Homework, Todo
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
# Create your views here.
def home(request):
    return render(request, "home.html")

def notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('descriptions') 
        notes = Notes.objects.create(
            user = request.user,
            title = title,
            descriptions = desc
        )
        notes.save()
        messages.success(request, f"Notes Added from {request.user.username} Successfully ")
        return redirect('/notes/')
    
    notes = Notes.objects.filter(user= request.user)
    context = {
        "Notes": notes,
    }
    return render(request, "notes.html", context)

def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

def detail_notes(request, pk = None):
    notes = Notes.objects.filter(id = pk)
    print(notes)
    context = {
        'Notes':notes,
    }
    return render(request, "notes_detail.html", context)

def homework(request):
    if request.method == "POST":
        try:
            finished = request.POST['finished']
            if finished == "on":
                finished = True
            else:
                finished = False
        except:
            finished = False

        user = request.user
        subject = request.POST['subject']
        title = request.POST['title']
        description = request.POST['description']
        due = request.POST['due']
        

        homework = Homework.objects.create(
            user = user,
            subject = subject,
            title = title,
            description = description,
            due = due,
            is_finished = finished,
        )
        homework.save()
        messages.success(request, f"Homework Added from {request.user.username} !!")
        
    homework = Homework.objects.filter(user = request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'Homework': homework,
        'homework_done':homework_done,
    }
    return render (request,"homework.html", context)

def update_homework(request, pk=None):
    homework = Homework.objects.get(id = pk)
    if homework.is_finished == True:
        print("hellow")
        homework.is_finished = False
    else:
        print("mahi")
        homework.is_finished = True
    homework.save()
    return redirect('/homework/')

def delete_homework(request, pk=None):
    Homework.objects.get(id = pk).delete()
    return redirect('/homework/')


def youtube(request):
    if request.method == "POST":
        search = request.POST['search']
        video = VideosSearch(search, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':search,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc = ""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
            'results':result_list,
        }
        return render(request, "youtube.html", context)
    return render(request, "youtube.html")

def todo(request):
    if request.method == "POST":
        try:
            finished = request.POST['finished']
            if finished == "on":
                finished = True
            else:
                finished = False
        except:
            finished = False

        user = request.user
        title = request.POST['title']
        Todo.objects.create(
            user = user,
            title = title,
            is_finished = finished,
        )
        messages.success(request, f"Todo Added from {request.user.username} Successfully !!")
        return redirect('todo')
    
    todo = Todo.objects.filter(user = request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'Todos':todo,
        'todos_done':todos_done
    }
    return render(request,"todo.html",context)

def update_todo(request, pk=None):
    todo = Todo.objects.get(id = pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('/todo/')


def delete_todo(request, pk=None):
    Todo.objects.get(id = pk).delete()
    return redirect('/todo/')

def book(request):
    if request.method == "POST":
        search = request.POST['search']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + search
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
        context = {
            'results':result_list,
        }
        return render(request, "books.html",context)

    return render(request, "books.html")

def dictionary(request):
    if request.method == "POST":
        text = request.POST['search']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms,
            }
            return render(request, "dictionary.html", context)
        except Exception as e:
            print(e)
    return render(request, "dictionary.html")

def wiki(request):
    if request.method == "POST":
        try:
            text = request.POST['search']
            search = wikipedia.page(text)
            context = {
                'search':text,
                'title':search.title,
                'link':search.url,
                'details':search.summary
            }
            return render(request, "wiki.html", context)
        except:
            return redirect('wiki')
    return render(request, "wiki.html")