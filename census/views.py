from django.shortcuts import render
from rest_framework import generics, status, response
from rest_framework.permissions import IsAuthenticated
from  authentication.authentication import BearerTokenAuthentication
from django.db.models import Count
from .serializers import CensusSerializer
from datetime import datetime, time
from rest_framework.views import APIView
from .models import *


class CensusApiView(APIView):
    
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        census = Census.objects.filter(user=request.user).first()

        if not census:
            census = Census()
        
        serializer = CensusSerializer(census)
        return response.Response({"message": "success", "detail": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        census = Census.objects.filter(user=request.user).first()

        if census:
            serializer = CensusSerializer(census, data=request.data, partial=True)
        else:
            serializer = CensusSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
            return response.Response({"message": "success", "detail": serializer.data}, status=status.HTTP_200_OK)
        return response.Response({"message": "failed", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
