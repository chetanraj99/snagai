from rest_framework import serializers
from .models import Report
from .models import Description

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'description', 'solutions']

class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = ['id', 'description']
        

        
