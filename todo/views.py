from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
# Create your views here.
# def say_hello(request):
#     return HttpResponse("Hello World")


def get_todo_list(request):
    results = Item.objects.all()
    return render(request,"todo_list.html",{'items':results})

def create_an_item(request):
    if request.method=="POST":
        # a post request - user is submitting the form
        form = ItemForm(request.POST,request.FILES)
        # creates a new form from ItemForm and is populated with the requests
        if form.is_valid():
            form.save()
        return redirect(get_todo_list)    
        # just need to call save we do not need to define items because it knows from the original form class what fields there are
        
        # new_item = Item()
        # new_item.name = request.POST.get('name')
        # new_item.done = 'done' in request.POST
        # new_item.save()
    else:
        # user hasn't submitted for the page has just been rendered so return an empty form
        form = ItemForm()
        
    return render(request,"item_form.html", {'form':form})


def edit_an_item(request, id):
    item = get_object_or_404(Item, pk=id)
    # pk means primary key
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(get_todo_list)  
    else:
        form = ItemForm(instance=item)
   
    return render(request,"item_form.html", {'form':form})

def toggle_status(request,id):
    item = get_object_or_404(Item, pk=id)
    item.done=not item.done
    item.save()
    return redirect(get_todo_list)
    