from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Student
# Create your views here.

def index(request):
     context = {}
     context['name'] = 'sai'
     return render(request, 'index.html',context)

def signup(request):
    if request.method == 'GET':
        context = {}
        return render (request, 'signup.html',context)
    elif request.method == 'POST':
        context = {}
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        ramid = request.POST['ramid']
        course = request.POST['course']
        psw = request.POST['psw']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            print("New User")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, password=psw)
            login(request, user)
            stu = Student(user=user,ram_id=ramid,course=course)
            stu.save()
            return render(request, 'sconfpage.html', context)

def sconfpage(request):
    return render(request, 'sconfpage.html')

def login_request(request):
    if request.method =='GET':
        context = {}
        return render (request, 'login.html', context)
    if request.method =='POST':
        context = {}
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect('sconfpage')
        else:
            context['message'] = "invalid username or password"
            return render(request, 'login.html', context)

def logout_request(request):
    logout(request)
    return redirect ('index')

#@csrf_exempt
#def givedata(request):     
#    if request.method == 'GET':                AN EXAMPLE HTTP REQUEST HANDLER
#        context = {                            TO INTERFACE WITH THE RFID PROTOTYPE
#            'name' : 'sai',
#            'id': 'R02089475'
#        }
#        return JsonResponse(context)
#    if request.method == 'POST':
#        name = request.POST['name']
#        context = {
#            'name' : name,
#            'id ' : 'R02089477'
#        }
#        return JsonResponse(context)