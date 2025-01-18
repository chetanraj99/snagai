from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from core.serializers import ReportSerializer, DescriptionSerializer
from core.models import Report, Description
from rest_framework.decorators import api_view
from sentence_transformers import SentenceTransformer, util  # type: ignore
import faiss
import numpy as np

# Create your views here.
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()


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
    # Fetch database data
        reports = list(Report.objects.values_list('description', flat=True))
        if not reports:
            return Response({"error": "No reports found in the database."}, status=status.HTTP_404_NOT_FOUND)

        # Validate user input
        des = request.data.get('description')
        if not des:
            return Response({"error": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Encode query and use precomputed vectors for similarity search
        try:
            # Precompute and load vector embeddings (only once, outside this API logic)
            # Example: FAISS, Milvus, Pinecone, etc.
            description_embeddings = model.encode(reports)  # Replace with precomputed embeddings if applicable
            index = faiss.IndexFlatL2(description_embeddings.shape[1])  # Replace with your vector index
            index.add(np.array(description_embeddings))  # Ensure this is done only once

            # Encode query embedding
            query_embedding = model.encode([des])

            # Perform vector similarity search
            N = 5  # Number of top matches
            distances, indices = index.search(np.array(query_embedding), N)

            # Prepare matches
            matches = [
                {
                    "description": reports[idx],
                    "similarity_score": 1 - distances[0][i]  # Adjusted score for cosine similarity
                }
                for i, idx in enumerate(indices[0])
            ]

            return Response({"matches": matches}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

