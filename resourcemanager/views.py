from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Student
# Create your views here.

def index(request):             #view to display the index page
     context = {}
     context['name'] = 'sai'
     return render(request, 'index.html',context)

def signup(request):            #view for users to sign up
    if request.method == 'GET': #renders the signup page in GET
        context = {}            #adds user to the database in POST
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

def sconfpage(request):                         #view to render a sample confirmation page
    return render(request, 'sconfpage.html')    # is being used to see if a user is able to login
                                                # will be replaced by a new home page later     


def login_request(request):                    # A view to authenticate the user and log him in                
    if request.method =='GET':                 # GET renders a login page 
        context = {}                           # POST authenticates the user and logs him in 
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

def logout_request(request):                    #A view to logout the user
    logout(request)                             # nothing more to say here :)                    
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