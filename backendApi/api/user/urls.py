from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='languages')

urlpatterns = [
    path("login/", views.signin, name="signin"),
    path("logout/<int:id>/", views.signout, name="signout"),
    path("update/", views.update, name="update"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password/<str:reset_token>/", views.reset_password, name="reset_password"),
    path("confirm_email/<str:reset_token>/", views.confirm_email, name="reset_password"),
    path("", include(router.urls))
]