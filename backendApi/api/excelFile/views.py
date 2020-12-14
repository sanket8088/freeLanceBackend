from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re
from rest_framework.renderers import JSONRenderer
import json
from uuid import uuid4
import base64
from django.shortcuts import render
from xlsxwriter.workbook import Workbook
# import pandas as pd
import xlsxwriter
import os
from backendApi import settings
from io import BytesIO
from django.http.response import HttpResponse

from backendApi import settings
from django.core.mail import send_mail
from .models import Response, SendMailSave

#html email sending
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime


@csrf_exempt       
def fileDownload(request):
    try:
        workbook = xlsxwriter.Workbook('Template.xlsx')
        worksheet = workbook.add_worksheet("Sheet 1")
        cell_format = workbook.add_format()
        # cell_format.set_pattern(1)  # This is optional when using a solid fill.
       
        cell_format.set_align('center')
        cell_format.set_bold()
        cell_format.set_align('vcenter')
        cell_format.set_bottom(1)
        cell_format.set_top(1)
        cell_format.set_left(1)
        cell_format.set_right(1)
        worksheet.set_column('A:E', 30)
        # worksheet.set_row(1, 50)
        worksheet.write('A1', 'Name', cell_format)
        worksheet.write('B1', 'Email ID' ,cell_format)
        worksheet.write('C1', 'Organization Name', cell_format)
        worksheet.write('D1', 'Address', cell_format)
        worksheet.write('E1', 'Price (in Rupees)', cell_format)
        worksheet.write('F1', 'Date', cell_format)
        workbook.close()
        newUrl = os.path.join(settings.BASE_DIR,  'Template.xlsx')
        if os.path.exists(newUrl):
            with open(newUrl, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(newUrl)
                fh.close()
                os.remove(newUrl)
                return response
    except Exception as e:
        print(e)
        return JsonResponse({ "status" : 400, "success": "User does not exist but logging out"})


@csrf_exempt       
def sendMail(request):
    try:
        subject = request.POST["heading"]
        instructions = request.POST["instructions"]
        attention = request.POST["attention"]
        message = request.POST["message"]
        footer = request.POST["footer"]
        userId = request.POST["userId"]
        toMail = request.POST["email"]
        organization = request.POST["organization"]
        name = request.POST["name"]
        amount = request.POST["amount"]
        attachment = request.FILES["attachment"]
        cc="['sanket.nihal@gmail.com]"
        file = SendMailSave(username_id=userId, subject=subject, instructions=instructions, attention=attention, message=message, footer=footer, toMail=toMail,amount = amount, name =name, organization = organization, responded=0)
        file.save()
        pathToFIle = attachment.temporary_file_path()
        url = settings.HOSTED_URL+"/api/excel/feedbackPage/" + str(userId) +"/" +toMail + "/" +str(file.id)+"/"
        to = toMail
        UserModel = get_user_model()
        user = UserModel.objects.get(id=userId)
        # res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
        html_content = render_to_string("sendMail.html", {"instructions" : instructions, "attention" :attention, "message": message, "footer" : footer, "url" :url,  })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject,
            text_content,
            user.email,
            [to]
        )
        attachmentFile = open(pathToFIle, 'rb')
        email.attach(attachment.name, attachmentFile.read())   
        email.attach_alternative(html_content, "text/html")
        email.send()
        return JsonResponse({ "status" : 200, "success": "Mail sent"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "success": "Mail sent"})
        

@csrf_exempt       
def feedback(request, id, mail):
    try:
        desc= request.POST["description"]
        resp = request.POST["response"]
        emailId = int(request.POST["emailId"])
        SendMailSave.objects.filter(id=emailId).update(responded=1)
        newObj = Response(username_id=id, response=resp, description=desc, respose_email=mail, emailReply_id = emailId)
        newObj.save()
        return JsonResponse({ "status" : 200, "success": "Mail sent"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "success": "Mail sent"})
        

@csrf_exempt       
def feedbackPage(request,id,mail,mailId):
    try:
        return render(request, "response.html")
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "success": "Mail sent"})
        

@csrf_exempt       
def noResponse(request,id):
    try:
        allData = SendMailSave.objects.filter(username_id=id).filter(responded=0)
        sendData=[]
        for data in allData:
            temp={}
            temp["id"] =data.id
            temp["subject"] =data.subject
            temp["toMail"] =data.toMail
            temp["organization"]=data.organization
            temp["amount"] =data.amount
            temp["date"] = data.created_at
            sendData.append(temp)
        return JsonResponse(sendData,safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "success": "Mail sent"})
        


@csrf_exempt       
def compareMails(request,id):
    try:
        allEmail = SendMailSave.objects.filter(username_id=id)
        
        allData = Response.objects.filter(username_id=id)
        print(allData)
        print(allEmail)
           
        return JsonResponse({ "status" : 200, "success": "Mail sent", "totalMail" : len(allEmail) , "responsedMail" : len(allData)})
      
    except Exception as e:
        print(e)
        return JsonResponse({ "status" : 400, "success": "Mail sent"})



@csrf_exempt       
def resendMail(request,id):
    try:
        allData = SendMailSave.objects.get(id=id)
        toMail =allData.toMail
        userId =allData.username_id
        instructions =allData.instructions
        attention = allData.attention
        message= allData.message
        footer =allData.footer
        subject= allData.subject
        # to = allData["toMail"]
        url = settings.HOSTED_URL+"/api/excel/feedbackPage/" + str(userId) +"/" +toMail + "/" +str(id)+"/"
        html_content = render_to_string("sendMail.html", {"instructions" : instructions, "attention" :attention, "message": message, "footer" : footer, "url" :url,  })
        text_content = strip_tags(html_content)
        UserModel = get_user_model()
        user = UserModel.objects.get(id=userId)
        email = EmailMultiAlternatives(
            subject,
            text_content,
            user.email,
            [toMail]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return JsonResponse({ "status" : 200, "success": "Mail sent"})
      
    except Exception as e:
        print(e)
        return JsonResponse({ "status" : 400, "error": "Mail not sent"})


@csrf_exempt       
def allResponse(request,id):
    try:
        allData = Response.objects.filter(username_id=id)
        print(allData)
        sendData=[]
        for data in allData:
            a = {}
            a["senderMail"] = data.respose_email
            a["response"] = data.response
            a["description"] = data.description
            sendData.append(a)
            
        return JsonResponse(sendData,safe=False)
      
    except Exception as e:
        print(e)
        return JsonResponse({ "status" : 400, "success": "Mail sent"})