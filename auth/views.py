from django.shortcuts import render
from django.db import transaction
from app.models import ActorProfile, NGO, Host, Camp, IDPPre, Idp, Image,  IdpCampAssociation
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from .serializers import UserProfileSerializer, UserSerializer, CampSerializer, NGOSerializer, HostSerializer, IDPPreSerializer, IDPSerializer, IdpCampAssociationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from rest_framework.permissions import BasePermission






class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to token payload
        try:
            actor_profile = user.actorprofile
            token['user_type'] = actor_profile.user_type
        except ActorProfile.DoesNotExist:
            # Handle the case where ActorProfile does not exist
            pass

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfileAPIView(request):
    if request.method == 'GET':
        try:
            actor_profile = request.user.actorprofile
            serializer = UserProfileSerializer(actor_profile)
            user_type = actor_profile.user_type
            profile_image_url = get_profile_image_url(actor_profile.id)

            data = {"actor_profile": serializer.data, "profileImageUrl": profile_image_url}

            if user_type == 'NGO':
                # Fetch data from the NGO table
                try:
                    ngo_data = NGO.objects.filter(profile__user=request.user)
                    ngo_serializer = NGOSerializer(ngo_data, many=True)
                    data["profile"] = ngo_serializer.data
                    return Response(data)
                except NGO.DoesNotExist:
                    return Response({"error": "NGO data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

            elif user_type == 'Camp Admin':
                # Fetch data from the Camp table
                try:
                    camp_data = Camp.objects.filter(profile__user=request.user)
                    camp_serializer = CampSerializer(camp_data, many=True)
                    data["profile"] = camp_serializer.data
                    return Response(data)
                except Camp.DoesNotExist:
                    return Response({"error": "Camp data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

            elif user_type == 'Host':
                # Fetch data from the Host table
                try:
                    host_data = Host.objects.filter(profile__user=request.user)
                    host_serializer = HostSerializer(host_data, many=True)
                    data["profile"] = host_serializer.data
                    return Response(data)
                except Host.DoesNotExist:
                    return Response({"error": "Host data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

            elif user_type == 'IDP':
                # Fetch data from the IdpCampAssociation table using IDP email
                try:
                    idp_email = actor_profile.user.email
                    idp_camp_association_data = IdpCampAssociation.objects.filter(idpemail=idp_email)
                    idp_camp_association_serializer = IdpCampAssociationSerializer(idp_camp_association_data, many=True)
                    data["idp_camp_association"] = idp_camp_association_serializer.data
                except IdpCampAssociation.DoesNotExist:
                    return Response({"error": "IDP Camp Association data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

                # Fetch data from the IDP table
                try:
                    idp_data = Idp.objects.get(profile__user=request.user)
                    idp_serializer = IDPSerializer(idp_data)
                    data["profile"] = idp_serializer.data
                    return Response(data)
                except Idp.DoesNotExist:
                    return Response({"error": "IDP data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

            elif user_type == 'Volunteer':
                # If user is a Volunteer, only return actor profile details
                return Response(data)
            
            elif user_type == 'NDRMC Admin':
                return Response(data)

            else:
                return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        except ActorProfile.DoesNotExist:
            return Response({"error": "ActorProfile does not exist for this user"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FullUserProfileAPIView(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        actor_profile = user.actorprofile
        serializer = UserProfileSerializer(actor_profile)
        user_type = actor_profile.user_type
        profile_image_url = get_profile_image_url(actor_profile.id)

        data = {"actor_profile": serializer.data, "profileImageUrl": profile_image_url}

        if user_type == 'NGO':
            try:
                ngo_data = NGO.objects.filter(profile__user=user)
                ngo_serializer = NGOSerializer(ngo_data, many=True)
                data["profile"] = ngo_serializer.data
            except NGO.DoesNotExist:
                return Response({"error": "NGO data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        elif user_type == 'Camp Admin':
            try:
                camp_data = Camp.objects.filter(profile__user=user)
                camp_serializer = CampSerializer(camp_data, many=True)
                data["profile"] = camp_serializer.data
            except Camp.DoesNotExist:
                return Response({"error": "Camp data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        elif user_type == 'Host':
            try:
                host_data = Host.objects.filter(profile__user=user)
                host_serializer = HostSerializer(host_data, many=True)
                data["profile"] = host_serializer.data
            except Host.DoesNotExist:
                return Response({"error": "Host data not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        elif user_type == 'IDP':
                # Fetch data from the IdpCampAssociation table using IDP email
                try:
                    idp_email = actor_profile.user.email
                    idp_camp_association_data = IdpCampAssociation.objects.filter(idpemail=idp_email)
                    idp_camp_association_serializer = IdpCampAssociationSerializer(idp_camp_association_data, many=True)
                    data["idp_camp_association"] = idp_camp_association_serializer.data
                except IdpCampAssociation.DoesNotExist:
                    return Response({"error": "IDP Camp Association data not found for this user"}, status=status.HTTP_404_NOT_FOUND)


        elif user_type == 'Volunteer':
            return Response(data)

        elif user_type == 'NDRMC Admin':
            return Response(data)

        else:
            return Response({"error": "Invalid user_type"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except ActorProfile.DoesNotExist:
        return Response({"error": "ActorProfile does not exist for this user"}, status=status.HTTP_404_NOT_FOUND)


def get_profile_image_url(profile_id):
    try:
        image = Image.objects.get(profile_id=profile_id)
        return settings.MEDIA_URL + str(image.image_url)
    except Image.DoesNotExist:
        return None

@api_view(['GET'])
def UserListAPIView(request):
    if request.method == 'GET':
        # Retrieve all users
        users = User.objects.all()

        # Serialize user data
        serializer = UserSerializer(users, many=True)

        # Return serialized data
        return Response(serializer.data)
    
@api_view(['POST'])
def register_ngo(request):
    if request.method == 'POST':
        # Parse incoming JSON
        data = request.data
        
        # Extract user data
        user_data = {
            'username': data.get('username'),
            'email': data.get('email'),
            'password': make_password(data.get('password')),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'is_active': False
        }

        # Extract NGO data
        ngo_data = {
            'name': data.get('name'),
            'location': data.get('location'),
            'capacity': data.get('capacity'),
            'legal_doc': data.get('legal_doc'),
            'country': data.get('country'),
            'status': data.get('status')
        }

        # Extract common actor profile data
        actor_profile_data = {
            'location': data.get('location'),
            'phone_number': data.get('phone_number'),
            'user_type': data.get('user_type')
        }

        try:
            # Register user in Django auth table
            user = User.objects.create(**user_data)

            # Register ActorProfile
            actor_profile_data['user'] = user  # Associate with the created user
            actor_profile = ActorProfile.objects.create(**actor_profile_data)

            # Register NGO
            ngo_data['profile'] = actor_profile  # Associate with the created actor profile
            ngo = NGO.objects.create(**ngo_data)

            # Serialize actor profile data
            serializer = UserProfileSerializer(actor_profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_host(request):
    # Parse incoming JSON
    data = request.data
    
    # Extract user data
    user_data = {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': make_password(data.get('password')),
        'first_name': data.get('firstname'),
        'last_name': data.get('lastname'),
        'is_active': False
    }

    # Extract host data
    host_data = {
        'capacity': data.get('capacity'),
        'preference': data.get('preference'),
        'language': data.get('language'),
        'hosting_experience': data.get('hosting_experience'),
        'location': data.get('location'),
        'contact_info': data.get('contact_info'),
        'legal_doc_id': data.get('legal_doc_id'),
        'economic_status': data.get('economic_status')
    }

    # Extract common actor profile data
    actor_profile_data = {
        'location': data.get('location'),
        'phone_number': data.get('phone_number'),
        'user_type': data.get('user_type')
    }

    try:
        # Register user in Django auth table
        user = User.objects.create(**user_data)

        # Register ActorProfile
        actor_profile_data['user'] = user  # Associate with the created user
        actor_profile = ActorProfile.objects.create(**actor_profile_data)

        # Register Host
        host_data['profile'] = actor_profile  # Associate with the created actor profile
        host = Host.objects.create(**host_data)

        # Serialize actor profile data
        serializer = UserProfileSerializer(actor_profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def register_camp(request):
    if request.method == 'POST':
        # Parse incoming JSON
        data = request.data
        
        # Extract camp data
        camp_data = {
            'name': data.get('name'),
            'location': data.get('location'),
            'capacity': data.get('capacity'),
            'current_population': data.get('current_population'),
            'demographic_info': data.get('demographic_info'),
            'shelter_type': data.get('shelter_type'),
            'economic_activities': data.get('economic_activities'),
            'health_education_info': data.get('health_education_info'),
            'status': data.get('status')
        }

        try:
            # Create Django auth user
            user_data = {
                'username': data.get('username'),
                'email': data.get('email'),
                'password': make_password(data.get('password')),
                'first_name': data.get('firstname'),
                'last_name': data.get('lastname'),
                'is_active': False
            }
            user = User.objects.create(**user_data)

            # Create ActorProfile
            actor_profile_data = {
                'user': user,
                'location': data.get('location'),
                'phone_number': data.get('phone_number'),
                'user_type': data.get('user_type')
            }
            actor_profile = ActorProfile.objects.create(**actor_profile_data)

            # Associate Camp with ActorProfile
            camp_data['profile'] = actor_profile

            # Register Camp
            camp = Camp.objects.create(**camp_data)

            return Response({"message": "Camp registered successfully. Please wait until it is activated by the Admin."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_volunteer(request):
    # Parse incoming JSON
    data = request.data
    
    # Extract user data
    user_data = {
        'username': data.get('username'),
        'email': data.get('email'),
        'password': make_password(data.get('password')),
        'first_name': data.get('firstname'),
        'last_name': data.get('lastname'),
        'is_active': False
    }

    # Extract common actor profile data
    actor_profile_data = {
        'location': data.get('location'),
        'phone_number': data.get('phone_number'),
        'user_type': 'Volunteer'  # Set user type as Volunteer
    }

    try:
        # Register user in Django auth table
        user = User.objects.create(**user_data)

        # Register ActorProfile
        actor_profile_data['user'] = user  # Associate with the created user
        actor_profile = ActorProfile.objects.create(**actor_profile_data)

        # Serialize actor profile data
        serializer = UserProfileSerializer(actor_profile)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_idppre(request):
    data = request.data
    
    idppre_data = {
        'email': data.get('email'),
        'phone_number': data.get('phone_number'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
    }

    try:
        # Check if the email already exists in IdpCampAssociation
        if IdpCampAssociation.objects.filter(idpemail=idppre_data['email']).exists():
            return Response({"error": "An IDP with this email is already associated with a camp."}, status=status.HTTP_400_BAD_REQUEST)

        # Register IDPPre
        idppre = IDPPre.objects.create(**idppre_data)
        
        # Retrieve camp ID from the authenticated user's profile if needed
        camp_id = request.user.id
        
        # Example of associating the IDP with a camp (if camp ID is available)
        idp_camp_association_data = {
            'camp': camp_id,
            'idpemail': idppre_data['email']  # Store the email
        }
        idp_camp_association_serializer = IdpCampAssociationSerializer(data=idp_camp_association_data)
        if idp_camp_association_serializer.is_valid():
            idp_camp_association_serializer.save()
        
        # Serialize IDPPre data
        idppre_serializer = IDPPreSerializer(idppre)
        
        return Response(idppre_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def register_idp(request):
    # Parse incoming JSON
    data = request.data

    # Extract email from the request data
    email = data.get('email')

    try:
        # Check if the email exists in IDPPre
        if IDPPre.objects.filter(email=email).exists():
            # Ensure all required fields are provided
            if all(key in data for key in ['username', 'password', 'location', 'phone_number',
                                           'place_of_origin', 'contact_information', 'household_composition',
                                           'vulnerability_status', 'health_status', 'documentation_status',
                                           'education_level', 'language_spoken', 'previous_assistance_received',
                                           'protection_concerns', 'economic_status', 'age', 'gender']):
                # Extract user data
                user_data = {
                    'username': data.get('username'),
                    'email': email,
                    'password': make_password(data.get('password')),
                    'first_name': data.get('firstname'),
                    'last_name': data.get('lastname')
                }

                # Register user in Django auth table
                user = User.objects.create(**user_data)

                # Extract ActorProfile data
                actor_profile_data = {
                    'user': user,
                    'location': data.get('location'),
                    'phone_number': data.get('phone_number'),
                    'user_type': 'IDP'
                }

                # Register ActorProfile
                actor_profile = ActorProfile.objects.create(**actor_profile_data)

                # Extract IDP data
                idp_data = {
                    'profile': actor_profile,
                    'place_of_origin': data.get('place_of_origin'),
                    'contact_information': data.get('contact_information'),
                    'household_composition': data.get('household_composition'),
                    'vulnerability_status': data.get('vulnerability_status'),
                    'health_status': data.get('health_status'),
                    'documentation_status': data.get('documentation_status'),
                    'education_level': data.get('education_level'),
                    'language_spoken': data.get('language_spoken'),
                    'previous_assistance_received': data.get('previous_assistance_received'),
                    'protection_concerns': data.get('protection_concerns'),
                    'economic_status': data.get('economic_status'),
                    'is_verified': data.get('is_verified', False),
                    'age': data.get('age'),
                    'gender': data.get('gender')
                }

                # Register IDP
                idp = Idp.objects.create(**idp_data)

                # Serialize IDP data
                serializer = IDPSerializer(idp)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Incomplete data provided for IDP registration"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Please Register by any Camp admin first to sign up"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def activate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()

        return Response({"message": "User activated successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def deactivate_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()

        return Response({"message": "User deactivated successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)