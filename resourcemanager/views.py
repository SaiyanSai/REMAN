from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Student, Device, Staff, Allowed_Users , Device_logs #, Uniquekeys 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
# Create your views here.


def index(request):             #view to display the index page
     context = {}
     context['name'] = 'sai'
     return render(request, 'index.html',context)

def devicelogs(request):
    all_logs = Device_logs.objects.all()
    context = {'all_logs' : all_logs}
    return render(request, 'devicelogs.html', context)

def student_register(request):            #view for users to sign up
    user = request.user
    try:
        staff = Staff.objects.get(user = user)
    except:
         return HttpResponse("User not autheticated to view this page")
    if request.method == 'GET': #renders the signup page in GET
        context = {}            #adds user to the database in POST
        return render (request, 'student_register.html',context)
    elif request.method == 'POST':
        context = {}
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        ramid = request.POST['ramid']
        course = request.POST['course']
        psw = request.POST['psw']
        rfid_uid = request.POST["rfiduid"]
        user_exist = False
        try:
            print(1)
            User.objects.get(username=username)
            print(2)
            user_exist = True
           
        except:     
            print("New User")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=fname, last_name=lname, password=psw)
            login(request, user)
            stu = Student(user=user,ram_id=ramid,course=course,rfid_uid = rfid_uid)
            stu.save()
            return render(request, 'sconfpage.html', context)
        else:
            print(3)
            context['message'] = "User already exists please login"
            print(4)
            return render(request, 'student_register.html',context)
            print(5)

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

def device_register(request):
    user = request.user
    try:
        staff = Staff.objects.get(user = user)
    except:
         return HttpResponse("User not autheticated to view this page")
    if request.method == 'GET':
        context = {}
        return render(request, 'device_register.html', context)
    if request.method == 'POST':
        context = {}
        deviceid = request.POST['deviceid']
        deviceman = request.POST['deviceman']
        devicename = request.POST['devicename']
        roomnumber = request.POST['roomnumber']
        building = request.POST['building']
        if not deviceid or not deviceman or not devicename or not roomnumber or not building:
            context['message'] = 'A field was left blank'
            return render(request, 'device_register.html',context)
        device_exist = False
        try:
            Device.objects.get(device_id = deviceid)
            device_exist = True
        except:
            print('new device')
        if not device_exist:
            device = Device(device_id = deviceid, device_manufacturer = deviceman, device_name = devicename, room_number= roomnumber, hall = building)
            device.save()
            context['message'] = 'DEVICE ADDED SUCCESFULLY'
            return render(request, 'device_register.html', context)
        
def staff_register(request):
    if request.method == 'GET':
        context = {}
        return render(request, 'staff_register.html', context)
    elif request.method == 'POST':
        context = {}
        username = request.POST['username']
        psw = request.POST['psw']
        fname = request.POST['fname']
        lname = request.POST['lname']
        staffid = request.POST['staffid']
        unikey = request.POST['uniquekey']
        email = request.POST['email']
#    unikey_exist = False
#    try:
#        Uniquekeys.objects.get(unikey = unikey)
#        unikey_exist = True
#    except:
#        print('unikey error')
#        context['message'] = 'UNIKEY PROVIDED DOESNT EXIST'
#        return render(request, 'staff_register.html', context)
#    if unikey_exist:
#        print('unikey exist')
    user_exist = False
    try:
            User.objects.get(username=username)
            user_exist = True
           
    except:     
            print("New User")
    if not user_exist:
            user = User.objects.create_user(username=username,email = email, first_name=fname, last_name=lname, password=psw)
            login(request, user)
            staff = Staff(user=user,staff_id = staffid)
            staff.save()
            return render(request, 'sconfpage.html', context)
    else:
            context['message'] = "User already exists please login"
            return render(request, 'staff_register.html',context)
    
@csrf_exempt

def check_if_allowed(Student, Device):
    is_allowed = False
    if Student.id is not None:
        num_res = Device.allowed_users.filter(user = Student).count()
        if num_res > 0:
            is_allowed = True
    return is_allowed

@csrf_exempt
def givedata(request):     
    if request.method == 'GET':            #    AN EXAMPLE HTTP REQUEST HANDLER
        context = {                        #    TO INTERFACE WITH THE RFID PROTOTYPE
            'name' : 'sai',
            'id': 'R02089475'
        }
        return JsonResponse(context)
    if request.method == 'POST':
#         context = {                        #    TO INTERFACE WITH THE RFID PROTOTYPE
#             'name' : 'sai',
#             'id': 'R02089475'
#         }
#         return JsonResponse(context)
      
       if 'uidVal' in request.POST and 'deviceId' in request.POST:
          uid = request.POST['uidVal']
          deviceid = request.POST['deviceId']
          context = {
               'uid' : uid,
               'deviceid' : deviceid
          }
          try:
              student = Student.objects.get(rfid_uid = uid)
              print("user exist")
          except:
              context['msg'] = "User doesnt exist in database"
              return JsonResponse(context)
          try: 
              device = Device.objects.get()
              print("device exist")
          except:
              context['msg'] = "Device does not exist in database"
              return JsonResponse(context)
          is_allowed = check_if_allowed(student, device)
          context = {}
          context['permission'] = is_allowed
          if is_allowed == False:
            return JsonResponse(context)
          if is_allowed == True:
            current_time = datetime.now()
            new_time = current_time - timedelta(hours=4)
            print(new_time)
            log = Device_logs(user = student, username = student.user.username, device = device, dev_id = device.device_id, ram_id = student.ram_id, room_number  =device.room_number, hall = device.hall, timeoflogin = new_time)
            log.save()    
       elif 'uidVal' not in request.POST:
 #         deviceid = request.POST['deviceId']
          context = {
 #             'deviceid' : deviceid,
               'msg' : 'error no uid'
          }
       elif 'deviceId' not in request.POST:
        uid = request.POST['uidVal']
        context = {
               'uid' : uid,
               'msg' : 'error no deviceId'
          }
       return JsonResponse(context)
