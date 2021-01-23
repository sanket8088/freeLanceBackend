from rest_framework import routers
from django.urls import path, include
from . import views



urlpatterns = [
    path("fileDownload/", views.fileDownload, name="fileDownload"),
    path("sendMail/", views.sendMail, name="sendMail"),
    path("feedback/<int:id>/<str:mail>/", views.feedback, name="feedback"),
    path("feedbackPage/<int:id>/<str:mail>/<int:mailId>/", views.feedbackPage, name="feedbackPage"),
    path("allResponse/<int:id>/", views.allResponse, name="allResponse"),
    path("noResponse/<int:id>/", views.noResponse, name="noResponse"),
    path("compareMails/<int:id>/", views.compareMails, name="compareMails"),
    path("resendMail/<int:id>/", views.resendMail, name="resendMail"),
    path("allUserOrders/<int:id>/", views.allUserOrders, name="allUserOrders"),
    path("singleUserCompany/", views.singleUserCompany, name="singleUserCompany"),

]