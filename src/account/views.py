from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from common.django_utils import arender
from .forms import CustomUserCreationForm, AuthenticationForm , CustomAuthenticationForm
from .models import CustomUser
from django.contrib import auth
from django.contrib.auth import alogin, alogout
from django.contrib.auth import aauthenticate
from django.shortcuts import redirect
from common.auth import aanonymous_required
from django.contrib.auth.decorators import login_required

@aanonymous_required
async def home(request) -> HttpResponse:
   # return HttpResponse('Estamos na home da tua conta') 
   return render(request, 'account/home.html')   

@aanonymous_required
async def register(request) -> HttpResponse:    
   if request.method == 'POST':
       form = CustomUserCreationForm(request.POST)
       if await form.ais_valid():
           await form.asave()
           return redirect('login')
 
   else:
       form = CustomUserCreationForm()
       
   context = {'register_form': form}
   return await arender(request, 'account/register.html',context) 

@aanonymous_required
async def login(request) -> HttpResponse:
   if request.method == 'POST':
       form = CustomAuthenticationForm(request, data=request.POST)
       if await form.ais_valid():
          email = request.POST['username']
          passwd = request.POST['password']
          user: CustomUser | None = await auth.aauthenticate(
             request,
             username=email,
             password=passwd,
          )
          if user:
               await auth.alogin(request, user)
               return redirect (
                  'writer-dashboard' if user.is_writer else 'client-dashboard'
               )
          #     msg = (
           #       'Thanks for returning, {}! You were successfully logged in.' if user.is_writer else
            #      'Welcome! You have successfully logged in.'
             #  )
              # return redirect('home')
          
   else:
         form = CustomAuthenticationForm()
   context = {'login_form': form}
   return await arender(request, 'account/login.html',context)

@login_required(login_url='login')
async def logout(request:HttpRequest) -> HttpResponse:
    await alogout(request)
    return redirect('/')