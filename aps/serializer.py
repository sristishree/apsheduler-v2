from rest_framework import serializers

from .models import tasks

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tasks
        fields = ('coid', 'command','starttime')