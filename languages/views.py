from django.http import Http404
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguageList(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        languages = Language.objects.all()

        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageDetail(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Language.objects.get(id=pk)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        language = self.get_object(pk)
        serializer = LanguageSerializer(language)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        language = self.get_object(pk)
        serializer = LanguageSerializer(language, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        language = self.get_object(pk)
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)