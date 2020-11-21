from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes
from cryptography.fernet import Fernet
import base64
import time
from .utils import emailConfirmation
from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        userMail = str(validated_data["email"])
        message_bytes = userMail.encode('ascii')
        resetKey = base64_bytes = base64.b64encode(message_bytes)
        finalKey = str(resetKey)[2:len(str(resetKey))]
        current_milli_time = lambda: int(round(time.time() * 1000))
        instance.reset_key = str(finalKey) + str(current_milli_time())
        emailConfirmation(validated_data["email"], instance.reset_key )
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    class Meta:
        model = User
        extra_kwargs={"password" : {"write_only" :True}}
        fields = ("email", "password", "is_active", "is_staff", "is_superuser", "address", "contact_number", "organisation", "first_name", "last_name")
        

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ["id","email"]
        