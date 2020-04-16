from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
import datetime
from user.models import Profile

# def get_author(user):

#     qs = Author.objects.filter(user=user)
#     if qs.exists():
#         return qs[0]
#     return None

@login_required
def index(request):
    author = get_object_or_404(Profile, user=request.user)
    todos = Task.objects.all() #quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager
    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category
            content = title + " -- " + date + " " + category #content
            author = request.user
            Todo = Task(title=title, content=content, due_date=date, category=Category.objects.get(name=category), task_author=author)
            Todo.save() #saving the todo 
            return redirect("all_todo_list") #reloading the page
        
        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            for todo_id in checkedlist:
                todo = Task.objects.get(id=int(todo_id)) #getting todo id
                todo.delete() #deleting todo
    context = {

        "todos": todos, 
        "categories":categories
    }

    return render(request, 'usertodo/index.html', context)