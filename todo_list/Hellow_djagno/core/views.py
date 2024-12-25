from django.shortcuts import render, redirect
from .forms import SignUp 
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from .models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    # Check if 'q' parameter is present in the GET request for search functionality
    if 'q' in request.GET:
        q = request.GET['q']
        # Filter the Todo items based on the search query
        all_todo = Todo.objects.filter(todo_name__icontains=q, user=request.user)
        # Render the search results template
        return render(request, "core/search_results.html", {'todos': all_todo, 'query': q})
    
    # Handle POST request for adding new Todo item
    if request.method == 'POST':
        task = request.POST.get("task")
        if task:
            new_todo = Todo(user=request.user, todo_name=task)
            new_todo.save()

    # Retrieve all Todo items for the user
    all_todo = Todo.objects.filter(user=request.user)
        
    # Render the main todo template
    return render(request, "core/todo.html", {'todos': all_todo})



def delete(request, name):
    todo = Todo.objects.get(user=request.user, todo_name=name)
    todo.delete()
    return redirect('home-page')


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 6:
            messages.error(request, 'password must be atlest 6 charcther')
            redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'these user alardy exist')
            redirect('register')

        newuser = User.objects.create_user(username=username, email=email, password=password)
        newuser.save()
        messages.success(request, "congraglation you register it know login ")
        return redirect("login")
    return render(request, 'core/register.html', {})

def login_view(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        passw = request.POST.get('pass')
        validated_user = authenticate(username=uname, password=passw)
        if validated_user is not None:
            auth_login(request, validated_user)
            return redirect("home-page")
        else:
            messages.error(request, 'wrong user detail or user does not exist')
            return redirect('login')
    return render(request, 'core/login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login')

def progres(request):
    process = Todo.objects.filter(status=False)
    return render(request, 'core/prossec.html', {'process': process})


def update(request, name):
    get_todo = Todo.objects.get(user=request.user, todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')