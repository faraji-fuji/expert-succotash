import requests
from django.http import HttpResponse
from django.conf import settings
from .models import Chat
from .serializers import ChatSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_list_or_404, get_object_or_404
from telegram import Bot

api_token = settings.TELEGRAM_TESTBOAT_SPACEFORCE_BOT_TOKEN


class ChatList(APIView):
    """
    List all chats, or create a new chat.
    """
    def get(self, request):        
        chats = get_list_or_404(Chat)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChatDetail(APIView):
    """
    Retrieve, update or delete a chat instance.
    """
    def get(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
    
    def put(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        chat = get_object_or_404(Chat, pk=pk)
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
