from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.serializers import ReportSerializer, DescriptionSerializer
from core.models import Report, Description
# Create your views here.


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


class DescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = DescriptionSerializer
    queryset = Description.objects.all()

    def create(self, request, *args, **kwargs):
        # Access request data
        data = request.data

        # Custom validation or logic before saving
        if 'required_field' in data:
            return Response({'error': 'required_field is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use serializer to validate and save data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Perform additional actions if needed
        self.perform_create(serializer)

        # Customize the response
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Object created successfully!', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        # Save the object to the database
        serializer.save()


'''
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer

    def create(self, request, *args, **kwargs):
        # Access request data
        data = request.data

        # Custom validation or logic before saving
        if 'required_field' not in data:
            return Response({'error': 'required_field is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use serializer to validate and save data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Perform additional actions if needed
        self.perform_create(serializer)

        # Customize the response
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'message': 'Object created successfully!', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        # Save the object to the database
        serializer.save()
'''
