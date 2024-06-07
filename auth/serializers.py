from rest_framework import serializers
from app.models import ActorProfile, NGO, Camp, Host, IDPPre, Idp, IdpCampAssociation
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    # Include fields from the User model
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    # Add more fields as needed

    class Meta:
        model = ActorProfile
        fields = ['user_id', 'username', 'email', 'location', 'phone_number', 'user_type']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class NGOSerializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = '__all__'

class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = '__all__'

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class IDPPreSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDPPre
        fields = ['id', 'email', 'phone_number', 'first_name', 'last_name']

class IDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idp
        fields = '__all__' 

class IdpCampAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdpCampAssociation
        fields = '__all__'