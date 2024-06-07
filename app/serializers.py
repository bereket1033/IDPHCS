from rest_framework import serializers
from .models import Message, Connection, Story, Photo, Comment, Complain, Report, Resource, Announcement, Sharing
from django.contrib.auth.models import User

class MessageSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'message_text', 'sent_at']

    def get_sender(self, obj):
        return {'name': obj.sender.profile.user.username}

    def get_receiver(self, obj):
        return {'name': obj.receiver.profile.user.username}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'comment_text', 'commented_at', 'created_at', 'deleted_at', 'status']
        read_only_fields = ['id', 'user', 'commented_at', 'created_at', 'deleted_at', 'status']

class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class SharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = '__all__'