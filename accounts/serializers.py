from rest_framework import serializers
from app.models import Host, Idp, NGO, Camp, Image

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        exclude = ['profile'] 

class IdpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        exclude = ['profile']

class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        exclude = ['profile']

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        exclude = ['profile']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'