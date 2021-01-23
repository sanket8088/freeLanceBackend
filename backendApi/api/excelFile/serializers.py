from rest_framework import serializers
from .models import SendMailSave


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendMailSave
        fields = ["toMail", "organization"]
        