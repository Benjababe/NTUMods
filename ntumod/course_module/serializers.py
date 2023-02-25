# Serializer helps us translate json and python data types because front end application
# send json data type and receive json data types it also controls what we receive on
# front end applications and what we should send back to front end as we don't want to
# send all the field from db to user

from rest_framework import serializers
from .models import Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
