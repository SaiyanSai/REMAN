from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def index(request):
     context = {}
     context['name'] = 'sai'
     return render(request, 'index.html',context)

def signup(request):
    context = {}
    return render (request, 'signup.html',context)

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