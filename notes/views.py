from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Note
from notes.serializers import NoteSerializer
from django.http import Http404

# Create your views here.
class NoteList(APIView):
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True, context={'request':request})
        return Response({
            'notes':serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NoteDetail(APIView):
    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            # return Response(status=status.HTTP_404_NOT_FOUND)
            raise Http404

    def get(self, request, pk):
        note = self.get_object(pk)
        # serializer = NoteSerializer(note, context={'request': request})
        serializer = NoteSerializer(note)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

    def put(self, request, pk):
        note = self.get_object(pk)
        serializer = NoteSerializer(note, data=request.data, context={'request': request})
        # if serializer.is_valid(raise_exception=True):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        note = self.get_object(pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)