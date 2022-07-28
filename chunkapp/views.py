from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File as DjangoFile
from django.core.files.base import ContentFile
from django.conf import settings
from . models import File 
import pandas as pd
import shutil
import time
import os
# Create your views here.
def home(request):
    if request.method == 'POST':
        file_data = request.FILES.get("file")
        file_count = request.POST.get("file_count") or 2
        file = File.objects.create(file=file_data)
        url = file.file.url
        url = str(settings.BASE_DIR)+url.replace("/","\\")
        if url.split(".")[-1] not in ["json","csv"]:
            messages.error(request, "Please upload csv or json file")
            return redirect(request.META.get("HTTP_REFERER"))
        
        if url.split(".")[-1] == 'csv':
            df = pd.read_csv(url)
            rows_per_file = df.shape[0] // file_count
            folder_name = str(settings.BASE_DIR) + "\\temp\\" + str(int(time.time()*1000))
            os.makedirs(folder_name)
            for row_start in range(0, df.shape[0], rows_per_file):
                new_file  = df[row_start:row_start+rows_per_file]
                new_file.to_csv(f"{folder_name}/chunk_{row_start}.csv")

            outputfile = str(settings.MEDIA_ROOT) + f"\\processed-files\\folder_name"
            shutil.make_archive(outputfile, 'zip', folder_name)
            file.processed_file = f"/processed-files/folder_name.zip"
            file.save()
        return redirect("download", file.id)

        if url.split(".")[-1] == 'json':
            df = pd.read_json(url)
            rows_per_file = df.shape[0] // file_count
            folder_name = str(settings.BASE_DIR) + "\\temp\\" + str(int(time.time()*1000))
            os.makedirs(folder_name)
            for row_start in range(0, df.shape[0], rows_per_file):
                new_file  = df[row_start:row_start+rows_per_file]
                new_file.to_json(f"{folder_name}/chunk_{row_start}.json",indent=1,orient='records')

            outputfile = str(settings.MEDIA_ROOT) + f"\\processed-json-files\\folder_name"
            shutil.make_archive(outputfile, 'zip', folder_name)
            file.processed_file = f"/processed-json-files/folder_name.zip"
            file.save()
        return redirect("download", file.id)
        
    return render(request, 'home.html')

def download(request, file_id):
    file = File.objects.filter(id=file_id).first()
    context = {"file":file}
    return render(request, 'download.html',context)


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exist")
            return redirect("register")

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exist")
            return redirect("register")

        if len(username)< 4:
            messages.error(request, "Username must be atleast 4 characters")
            return redirect("register")

        if not username.isalnum():
            messages.error(request, "username must be Alph-Numeric")
            return redirect("register")

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
        messages.success(request, "Your account has been successfully created")
        return redirect("login")
    
    return render(request,'register.html')

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, "Invalid Credential")
            return redirect("login")
    
    return render(request,'sign_in.html')