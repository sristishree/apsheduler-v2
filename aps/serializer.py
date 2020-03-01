from rest_framework import serializers

from .models import tasks

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = tasks
        fields = ('diagID','starttime', 'jobtype','lookup_id','job_runs','job_success')