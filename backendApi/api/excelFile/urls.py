from rest_framework import routers
from django.urls import path, include
from . import views



urlpatterns = [
    path("fileDownload/", views.fileDownload, name="fileDownload"),
    path("sendMail/", views.sendMail, name="sendMail"),
    path("feedback/<int:id>/<str:mail>/", views.feedback, name="feedback"),
    path("feedbackPage/<int:id>/<str:mail>/", views.feedbackPage, name="feedbackPage"),
    path("allResponse/<int:id>/", views.allResponse, name="allResponse"),
]