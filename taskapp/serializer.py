from rest_framework import serializers
from taskapp.models import *
from datetime import datetime

# CustomUser model serializer
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'



