from django.shortcuts import render
from .models import User
from .serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import HttpResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class SnippetList(APIView):
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['User']

        token, created = Token.objects.get_or_create(user=serializer)
        return Response({
            'token': token.key
        })

        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #

class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        token = Token.objects.create(user=...)
        print(token.key)
        return Response(serializer.data)

    def post(self, request,pk, *args, **kwargs):
        serializer = SnippetSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

def patch_api(request,pk, format=None):
    if request.content_type == 'application/json':
        body = request.body
        body = body.decode('utf-8')
        body = json.loads(body)
        if 'id' in body:
            id = body['id']
            User.objects.filter(id=pk).update(id = id)
            return HttpResponse("id Updated",status=status.HTTP_201_CREATED)
        elif 'name' in body:
            name = body['name']
            User.objects.filter(id=pk).update(name=name)
            return HttpResponse("Name Updated", status=status.HTTP_201_CREATED)
        elif 'email' in body:
            email = body['email']
            User.objects.filter(id=pk).update(email=email)
            return HttpResponse("email Updated", status=status.HTTP_201_CREATED)
        else:
            password = body['password']
            User.objects.filter(id=pk).update(password=password)
            return HttpResponse("password updated",status=status.HTTP_201_CREATED)
    return HttpResponse("sucess", status=200)
