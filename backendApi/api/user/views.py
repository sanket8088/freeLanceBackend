from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, AllUserSerializer
from .models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re
from rest_framework.renderers import JSONRenderer
import json
from uuid import uuid4
import base64
from .utils import sendMail
from django.shortcuts import render 



def generateToken():
    rand_token = str(uuid4())
    return rand_token


@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
    print(request.POST)

        
    username = request.POST["email"]
    password = request.POST["password"]
    
    # if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
    #     return JsonResponse({ "status" : 400,"error": "Email id is not valid."})
    # if len(password) <= 7:
    #     return JsonResponse({ "status" : 400,"error": "Password not valid"})
        
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop("password")

            if user.email_verified == "0":
                return JsonResponse({ "status" : 400, "error" : "Your account hasn't been activated."})

            if user.session_token != "0":
                # user.session_token = "0"
                # user.save()
                # return JsonResponse({ "status" : 400, "error": "Previous session exists"})
                token= user.session_token
                login(request, user)
            else:
                token = generateToken()
                user.session_token = token
                user.save()
                login(request, user)
            a = {"token": token, "user": usr_dict}
            return JsonResponse({"status" : 200,"token": token, "user": usr_dict})
            
        else:
            return JsonResponse({ "status" : 400, "error" : "Invalid password"})

    except UserModel.DoesNotExist:
        return JsonResponse({ "status" : 400, "error": "Email not registered"})


@csrf_exempt       
def signout(request, id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = 0
        user.save()
        logout(request)
        return JsonResponse({ "status" : 200, "success" : "logout successful"})
    except UserModel.DoeNotExist:
        return JsonResponse({ "status" : 200, "success": "User does not exist but logging out"})

@csrf_exempt
def update(request):
    if not request.method == "POST":
        return JsonResponse({ "status" : 400, "error": "Send a post request with valid parameters only."})
    UserModel = get_user_model()
    if "email" in request.POST:
        mail = request.POST["email"]
    elif request.POST["resetKey"]:
        resetKey = request.POST["resetKey"]
        try:
            tempUser = UserModel.objects.get(reset_key=resetKey)
            mail = tempUser.email
        except Exception as e:
            return JsonResponse({ "status" : 400, "error" : "Invalid Token"})

    try:
        user = UserModel.objects.get(email=mail)
        user.session_token = 0
        for key, val in dict(request.POST).items():
            if key != "email":
                if key == "password":
                    user.set_password(request.POST[key])
                else:
                    setattr(user, key, val[0])
        user.save()
    except Exception as e:
        return JsonResponse({ "status" : 400, "error" : "mail id does not exist"})
    return JsonResponse({"status" : 200,"success" : "upadted successful"})



@csrf_exempt
def forgot_password(request):
    if not request.method == "POST":
        return JsonResponse({ "status" : 400, "error": "Send a post request with valid parameters only."})
    mail = request.POST["email"]
    UserModel = get_user_model()
    try:
  
        user = UserModel.objects.get(email=mail)
        reset_token = user.reset_key
        sendMail(mail,reset_token)
        return JsonResponse({"status" : 200, "success": "A reset link has been sent on registered mail id."})
    except Exception as e:
        print(e)
        return JsonResponse({"status" : 400, "error": "Not a registered mail id"})

    


@csrf_exempt
def reset_password(request):
    if not request.method == "POST":
        return JsonResponse({"status" : 400, "error": "Send a post request with valid parameters only."})
    mail = request.POST["email"]
    sendMail(mail)
    return JsonResponse({"status": 200, "success": "upadted successful"})
    

@csrf_exempt
def confirm_email(request,reset_token):
    if not request.method == "GET":
        return JsonResponse({"status" : 400, "error": "Send a get request with valid parameters only."})
    UserModel = get_user_model()
    UserModel.objects.filter(reset_key=reset_token).update(email_verified=1)
    return render(request, "awaiting_response.html") 
    # return JsonResponse({"status" : 200, "success": "upadted successful"})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {"create": {AllowAny}}
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except Exception as e:
            print(e)
            return [permission() for permission in self.permission_classes]
