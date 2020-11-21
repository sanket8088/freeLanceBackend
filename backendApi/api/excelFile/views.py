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
        return JsonResponse({ "status" : 200, "success": "User does not exist but logging out"})