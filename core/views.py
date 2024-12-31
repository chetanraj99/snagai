from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.serializers import ReportSerializer, DescriptionSerializer
from core.models import Report, Description
from rest_framework.decorators import api_view
from sentence_transformers import SentenceTransformer, util  # type: ignore


# Create your views here.
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


# class DescriptionViewSet(viewsets.ModelViewSet):
#     serializer_class = DescriptionSerializer
#     queryset = Description.objects.all()

#     def create(self, request, *args, **kwargs):
#         # Access request data
#         data = request.data

#         # Custom validation or logic before saving
#         if 'required_field' in data:
#             return Response({'error': 'required_field is missing.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Use serializer to validate and save data
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)

#         # Perform additional actions if needed
#         self.perform_create(serializer)

#         # Customize the response
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {'message': 'Object created successfully!', 'data': serializer.data},
#             status=status.HTTP_201_CREATED,
#             headers=headers
#         )

#     def perform_create(self, serializer):
#         # Save the object to the database
#         serializer.save()


@api_view(['GET', 'POST', 'PUT', "PATCH", "DELETE",])
def description_api(request, pk=None):
    if request.method == "GET":
        id = pk
        if id is not None:
            description = Description.objects.get(id=id)
            serializer = DescriptionSerializer(description)
            return Response(serializer.data)
        stu = Description.objects.all()
        serializer = DescriptionSerializer(stu, many=True)
        return Response(serializer.data)

    if request.method == "POST":

        reports = Report.objects.all().values()
        print(reports)
        descriptions = []
        # serializer = DescriptionSerializer(data=request.data)
        # Lightweight BERT variant

        for report in reports:
            descriptions.append(report['description'])
        print(descriptions)
        # description_embeddings = model.encode(descriptions)

        print(request.data)
        # query = report.data
        # print(query)

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response({"msg": "data saved into database"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Full update
    if request.method == "PUT":
        id = pk
        stu = Description.objects.get(pk=id)
        serializer = DescriptionSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Complete Data has been updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partial update
    if request.method == "PATCH":
        id = pk
        stu = Description.objects.get(pk=id)
        serializer = DescriptionSerializer(
            stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Partial Data has been updated"})
        return Response(serializer.errors)

    if request.method == "DELETE":
        id = pk
        print(request.data)
        stu = Description.objects.get(pk=id)
        stu.delete()
        return Response({"msg": "data deleted"})


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
