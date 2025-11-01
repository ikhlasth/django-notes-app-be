from rest_framework import serializers
from rest_framework.reverse import reverse
from notes.models import Note

class NoteSerializer(serializers.HyperlinkedModelSerializer):
  _links = serializers.SerializerMethodField()
  class Meta:
    model = Note
    fields = ['id', 'title', 'body', 'tags', 'created_at', 'updated_at', '_links']
  
  def get__links(self, obj):
    request = self.context.get('request')
    return [
      {'rel': 'self', 'href': reverse('note-list', request=request), 'actions':'POST', 'types':['application/json']},
      {'rel': 'self', 'href': reverse('note-detail', kwargs={'pk':obj.id}, request=request), 'actions':'GET', 'types':['application/json']},
      {'rel': 'self', 'href': reverse('note-detail', kwargs={'pk':obj.id}, request=request), 'actions':'PUT', 'types':['application/json']},
    ]