from django.utils import timezone
import os
from typing import Any, Dict, List, Optional
from django.db.models.query import  QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from .models import *
from .form import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

#---I WROTE THIS CODE---

@login_required
def userDetailsApi(request,id):
      
    appuser=AppUser.objects.get(id=id)
    print(appuser.id)
    return render(request,'screens/userDetailsApi.html',{"appuser":appuser})

#--- END OF CODE THAT I WROTE---


# Create your views here.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("../")

# This view handles user login.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('./home')  # Redirect to a success page
            else:
                return HttpResponse("Your account is disabled.")

        else:
            form=UserLoginForm()
            return render(request, 'screens/login.html',{"form":form,"error":"Invalid login details"})

    else:
        form=UserLoginForm()
    # If it's a GET request or if authentication failed, render the login page with the form
    return render(request, 'screens/login.html',{"form":form})

# This view handles user registration.
def register(request):
    

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'email' in user_form.cleaned_data:
                profile.email = request.POST['email']
               

            profile.save()
            Status.objects.create(appuser=profile)
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'screens/register.html',
                  {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})

#---I WROTE THIS CODE---

# This view displays the user's homepage.
@login_required
def home(request):
    user = request.user  # Get the authenticated user
    context = {'user': user}
    appuser=AppUser.objects.get(user=user)
    print(appuser.name)
    return render(request, 'screens/home.html', {'user': user,'appuser':appuser})
#---END OF CODE THAT I WROTE---    

#---I WROTE THIS CODE---
# This view allows users to update their profile
class UserProfileUpdate(UpdateView):
   model = AppUser
   fields = ['name', 'email','profile_image','background_image','bio']
   template_name="screens/update_user_profile.html"
   
   def get_success_url(self):
        return reverse_lazy('home') 
   
   def form_valid(self, form):
        # Get the current instance of AppUser
        app_user = AppUser.objects.get(id=self.kwargs['pk'])
        


        
        

        # Save the form and return the response
        return super().form_valid(form)
#---END OF CODE THAT I WROTE---   
   
#---I WROTE THIS CODE---   
# This view displays the user's homepage for a specific contact.   
@login_required
def userHome(request,contact_username):
    user = request.user  # Get the authenticated user
    context = {'user': user}
    appuser=AppUser.objects.get(user=user)
    contact=AppUser.objects.get(user__username=contact_username)
    print(appuser.name)
    return render(request, 'screens/home.html', {'user': user,'appuser':appuser,'contact':contact})
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# This view allows users to follow or unfollow other users.
@login_required
def follow(request):
  user=request.user 
  appuser=AppUser.objects.get(user=user)
  
  if request.method== 'POST': 
   following=request.POST['following']
   contact=AppUser.objects.get(user__username=following)
   instance1, created1 = Followings.objects.get_or_create(current_user=appuser, following=contact)
   instance2,created2=Followings.objects.get_or_create(current_user=contact,following=appuser)
   
   if created1 and created2:
      
      return render(request,'screens/home.html',{'user': user,'appuser':appuser,'contact':contact})
   else:
      instance1.delete()
      instance2.delete()
      return render(request,'screens/home.html',{'user': user,'appuser':appuser,'contact':contact})
  else:
      return HttpResponseRedirect('../home') 
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# This view allows users to delete a post from their gallery.
@login_required
def deletePost(request,id):
  
  post=Gallery.objects.get(id=id)
  post.delete()
  return HttpResponseRedirect('../home')
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# This view allows users to update their status.
@login_required
def updateStatus(request,id):
  
  if request.method=='POST':
    statusText=request.POST['statusText']
    status=Status.objects.get(appuser__id=id)
    status.status=statusText
    status.created_at=timezone.now()
    status.save()
  
  return HttpResponseRedirect('../home#status_container')
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# This view sets up a chat room for users to chat with each other.
@login_required
def chatRoom(request, contact_username):
    current_username=request.user.username
    print("Current username is ", current_username )
    print("Contact username is ", contact_username )
    roomName=create_chatroom(current_username,contact_username)
    print(roomName)
    
    return render(request, 'screens/chat_room.html', {'room_name': roomName,'username':current_username })
#---END OF CODE THAT I WROTE---

#---I WROTE THIS CODE---
# This function creates a chat room name based on the user names.
def create_chatroom(user1, user2):
    # Compare the user strings and arrange them alphabetically
    if user1 < user2:
        chatroom = f"chat_{user1}_{user2}"
    else:
        chatroom = f"chat_{user2}_{user1}"
    
    return chatroom

#---END OF CODE THAT I WROTE---