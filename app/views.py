from django.db import models as django_models  # Import Django models module
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Message, Connection, Story, Photo, Comment, Complain, Report, Image, Resource, Announcement, Sharing, Camp, NGO, Idp, Host
from .serializers import MessageSerializer, ConnectionSerializer, StorySerializer, PhotoSerializer, UserSerializer, CommentSerializer, ComplainSerializer, ReportSerializer, ResourceSerializer, AnnouncementSerializer, SharingSerializer, MessageSerializerAll
from datetime import datetime
import os
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, other_party_id):
    try:
        # Retrieve the authenticated user's ID
        authenticated_user_id = request.user.id
        
        # Retrieve messages between the authenticated user and the specified other party
        messages = Message.objects.filter(
            (django_models.Q(sender_id=authenticated_user_id) & django_models.Q(receiver_id=other_party_id)) |
            (django_models.Q(sender_id=other_party_id) & django_models.Q(receiver_id=authenticated_user_id))
        )
        
        # Serialize the messages using the modified serializer
        serializer = MessageSerializer(messages, many=True)
        
        # Return the serialized messages in JSON format
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Message.DoesNotExist:
        return Response({"message": "Messages not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    try:
        # Retrieve all messages
        messages = Message.objects.all()
        
        # Serialize the messages
        serializer = MessageSerializerAll(messages, many=True)
        
        # Return the serialized messages in JSON format
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Message.DoesNotExist:
        return Response({"error": "Messages not found"}, status=status.HTTP_404_NOT_FOUND)


#Connections 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_connection(request):
    # Extract the follower and followed_by from the request data
    follower_id = request.data.get('follower')
    followed_by_id = request.data.get('followed_by')

    # Check if a connection already exists
    existing_connection = Connection.objects.filter(follower_id=follower_id, followed_by_id=followed_by_id).first()

    if existing_connection:
        if existing_connection.current_status:
            # Connection exists and is active
            return Response({'message': 'Already connected.'}, status=status.HTTP_200_OK)
        else:
            # Connection exists but is inactive, so reactivate it
            existing_connection.current_status = True
            existing_connection.save()
            serializer = ConnectionSerializer(existing_connection)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # If no existing connection, create a new one
    serializer = ConnectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connections(request):
    connections = Connection.objects.all()

    # Serialize connections along with full follower and followed_by profiles
    serialized_connections = []
    for connection in connections:
        follower_profile = User.objects.get(id=connection.follower_id)
        followed_by_profile = User.objects.get(id=connection.followed_by_id)
        serialized_connection = {
            'id': connection.id,
            'follower': UserSerializer(follower_profile).data,
            'followed_by': UserSerializer(followed_by_profile).data,
            'created_at': connection.created_at,
            'current_status': connection.current_status
        }
        serialized_connections.append(serialized_connection)

    return Response(serialized_connections)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connection(request, connection_id):
    try:
        connection = Connection.objects.get(id=connection_id)

        # Retrieve full profiles of the follower and followed_by users
        follower_profile = User.objects.get(id=connection.follower_id)
        followed_by_profile = User.objects.get(id=connection.followed_by_id)

        # Serialize the connection along with full follower and followed_by profiles
        serialized_connection = {
            'id': connection.id,
            'follower': UserSerializer(follower_profile).data,
            'followed_by': UserSerializer(followed_by_profile).data,
            'created_at': connection.created_at,
            'current_status': connection.current_status
        }

        return Response(serialized_connection)

    except Connection.DoesNotExist:
        return Response({"message": "Connection not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_connection(request, connection_id):
    try:
        connection = Connection.objects.get(id=connection_id)
        connection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Connection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# Story
from .models import ActorProfile

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def story_list_create(request):
    if request.method == 'GET':
        # Retrieve all stories with associated IDP information
        stories = Story.objects.all()
        serialized_stories = []
        for story in stories:
            # Retrieve full information about the associated IDP from Django auth table
            idp_info = User.objects.get(id=story.idp.user_id)
            serialized_story = {
                'id': story.id,
                'idp_info': {
                    'id': idp_info.id,
                    'username': idp_info.username,
                    'email': idp_info.email,
                    # Include other IDP information as needed
                },
                'story_text': story.story_text,
                'shared_at': story.shared_at,
                'created_at': story.created_at,
                # Retrieve photos associated with the story from the Photo table
                'photos': [photo.image_url for photo in story.photos.all()]
            }
            # Retrieve comments associated with the story and serialize them
            comments = Comment.objects.filter(post=story.id)
            serialized_comments = CommentSerializer(comments, many=True).data
            serialized_story['comments'] = serialized_comments
            
            serialized_stories.append(serialized_story)
        return Response(serialized_stories, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # Retrieve the ActorProfile instance associated with the authenticated user
        actor_profile = ActorProfile.objects.get(user=request.user)
        
        # Set the idp field to the ID of the ActorProfile
        request.data['idp'] = actor_profile.id

        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def story_detail(request, pk):
    try:
        story = Story.objects.get(pk=pk)
    except Story.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StorySerializer(story, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Story updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        story.delete()
        return Response({"message": "Story deleted successfully"}, status=status.HTTP_200_OK)

    
@api_view(['GET'])
def get_story_by_id(request, story_id):
    try:
        # Retrieve the story by its ID
        story = Story.objects.get(pk=story_id)
        
        # Retrieve full information about the associated IDP from Django auth table
        idp_info = User.objects.get(id=story.idp.user_id)
        
        # Construct a dictionary with story details along with IDP information and photo URLs
        serialized_story = {
            'id': story.id,
            'idp_info': {
                'id': idp_info.id,
                'username': idp_info.username,
                'email': idp_info.email,
                # Include other IDP information as needed
            },
            'story_text': story.story_text,
            'shared_at': story.shared_at,
            'created_at': story.created_at,
            # Retrieve photos associated with the story from the Photo table
            'photos': [photo.image_url for photo in story.photos.all()]
        }
        
        # Retrieve comments associated with the story and serialize them
        comments = Comment.objects.filter(post=story.id)
        serialized_comments = CommentSerializer(comments, many=True).data
        serialized_story['comments'] = serialized_comments
        
        # Return the serialized story along with comments
        return Response(serialized_story, status=status.HTTP_200_OK)
    
    except Story.DoesNotExist:
        return Response({"message": "Story not found"}, status=status.HTTP_404_NOT_FOUND)

    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_images(request, story_id):
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        uploaded_photos = []
        for image in images:
            photo = Photo(image_url='', created_at=timezone.now(), deleted_at=None, status='Active', story_id=story_id)
            photo.image_url = handle_uploaded_file(image)
            photo.save()
            uploaded_photos.append(photo)
        
        serializer = PhotoSerializer(uploaded_photos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'No image files provided'}, status=status.HTTP_400_BAD_REQUEST)

def handle_uploaded_file(f):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    filename = str(timezone.now().timestamp()) + '_' + f.name
    with open(os.path.join(upload_dir, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join('images', filename)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    try:
        story_id = request.data.get('post')
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        return Response({"message": "Story not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # Assuming authenticated user is the commenter
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        if comment.user != request.user:
            return Response({"message": "You don't have permission to edit this comment"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        if comment.user != request.user:
            return Response({"message": "You don't have permission to delete this comment"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_complain(request):
    serializer = ComplainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(complained_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_complains(request):
    complains = Complain.objects.all()
    serialized_complains = []
    for complain in complains:
        # Retrieve full information about the complained_by user
        complained_by_user = User.objects.get(id=complain.complained_by.id)
        complained_to_user = User.objects.get(id=complain.complained_to.id)
        
        # Serialize the complain along with the full user details
        serialized_complain = {
            'id': complain.id,
            'complained_by': UserSerializer(complained_by_user).data,
            'complained_to': UserSerializer(complained_to_user).data,
            'description': complain.description,
            'created_at': complain.created_at,
            'deleted_at': complain.deleted_at,
            'status': complain.status
        }
        serialized_complains.append(serialized_complain)

    return Response(serialized_complains, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_complain_by_id(request, complain_id):
    try:
        complain = Complain.objects.get(pk=complain_id)
        
        # Retrieve full information about the complained_by user
        complained_by_user = User.objects.get(id=complain.complained_by.id)
        complained_to_user = User.objects.get(id=complain.complained_to.id)
        
        # Serialize the complain along with the full user details
        serialized_complain = {
            'id': complain.id,
            'complained_by': UserSerializer(complained_by_user).data,
            'complained_to': UserSerializer(complained_to_user).data,
            'description': complain.description,
            'created_at': complain.created_at,
            'deleted_at': complain.deleted_at,
            'status': complain.status
        }
        
        return Response(serialized_complain, status=status.HTTP_200_OK)
    except Complain.DoesNotExist:
        return Response({"message": "Complain not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_complain(request, complain_id):
    try:
        complain = Complain.objects.get(pk=complain_id)
        if complain.complained_by != request.user:
            return Response({"message": "You don't have permission to edit this complain"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ComplainSerializer(complain, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Complain.DoesNotExist:
        return Response({"message": "Complain not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_complain(request, complain_id):
    try:
        complain = Complain.objects.get(pk=complain_id)
        if complain.complained_by != request.user:
            return Response({"message": "You don't have permission to delete this complain"}, status=status.HTTP_403_FORBIDDEN)
        
        complain.delete()
        return Response({"message": "Complain deleted successfully"}, status=status.HTTP_200_OK)
    except Complain.DoesNotExist:
        return Response({"message": "Complain not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
    serializer = ReportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_reports(request):
    reports = Report.objects.all()
    serialized_reports = []
    for report in reports:
        serialized_report = ReportSerializer(report).data
        serialized_report['reported_by'] = UserSerializer(User.objects.get(id=report.reported_by_id)).data
        serialized_report['reported_to'] = UserSerializer(User.objects.get(id=report.reported_to_id)).data
        serialized_reports.append(serialized_report)
    return Response(serialized_reports, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_by_id(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        serialized_report = ReportSerializer(report).data
        serialized_report['reported_by'] = UserSerializer(User.objects.get(id=report.reported_by_id)).data
        serialized_report['reported_to'] = UserSerializer(User.objects.get(id=report.reported_to_id)).data
        return Response(serialized_report, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_report(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        # if report.reported_by != request.user:
        #     return Response({"message": "You don't have permission to edit this report"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Report.DoesNotExist:
        return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_report(request, report_id):
    try:
        report = Report.objects.get(pk=report_id)
        # if report.reported_by != request.user:
        #     return Response({"message": "You don't have permission to delete this report"}, status=status.HTTP_403_FORBIDDEN)
        
        report.delete()
        return Response({"message": "Report deleted successfully"}, status=status.HTTP_200_OK)
    except Report.DoesNotExist:
        return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_connected_stories(request):
    user_id = request.user.id

    # Find all connections where the current user is a follower
    connections = Connection.objects.filter(follower_id=user_id, current_status=True)

    # Collect IDs of users followed by the current user
    followed_user_ids = [connection.followed_by_id for connection in connections]

    # Retrieve stories from users followed by the current user
    stories = Story.objects.filter(idp__user_id__in=followed_user_ids).distinct()

    # Serialize the stories with detailed information
    serialized_stories = []
    for story in stories:
        idp_info = User.objects.get(id=story.idp.user_id)  # Assuming `idp` is a ForeignKey to a User profile
        serialized_story = {
            'id': story.id,
            'idp_info': {
                'id': idp_info.id,
                'username': idp_info.username,
                'email': idp_info.email,
                # Include other IDP information as needed
            },
            'story_text': story.story_text,
            'shared_at': story.shared_at,
            'created_at': story.created_at,
            'photos': [photo.image_url for photo in story.photos.all()]  # Assuming photos is a related name
        }

        # Retrieve comments associated with the story and serialize them
        comments = Comment.objects.filter(post=story)
        serialized_comments = CommentSerializer(comments, many=True).data
        serialized_story['comments'] = serialized_comments
        
        serialized_stories.append(serialized_story)

    return Response(serialized_stories, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    first_name = request.query_params.get('first_name')
    last_name = request.query_params.get('last_name')
    email = request.query_params.get('email')
    phone_number = request.query_params.get('phone_number')
    user_type = request.query_params.get('user_type')

    # Start with all users
    users = User.objects.all()

    # Apply filters based on query parameters
    if first_name:
        users = users.filter(first_name__icontains=first_name)
    if last_name:
        users = users.filter(last_name__icontains=last_name)
    if email:
        users = users.filter(email__icontains=email)
    if phone_number:
        users = users.filter(actorprofile__phone_number__icontains=phone_number)
    if user_type:
        users = users.filter(actorprofile__user_type__icontains=user_type)

    # Serialize the filtered users along with ActorProfile and profile image
    serialized_users = []
    for user in users:
        actor_profile = ActorProfile.objects.filter(user=user).first()
        profile_image = None
        if actor_profile:
            image_instance = Image.objects.filter(profile=actor_profile).first()
            if image_instance:
                profile_image = image_instance.image_url

        serialized_user = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'actor_profile': {
                'location': actor_profile.location if actor_profile else None,
                'phone_number': actor_profile.phone_number if actor_profile else None,
                'user_type': actor_profile.user_type if actor_profile else None,
                # Include other ActorProfile information as needed
            },
            'profile_image': profile_image,
            # Include other user information as needed
        }
        serialized_users.append(serialized_user)

    return Response(serialized_users, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_resource(request):
    serializer = ResourceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resource(request, resource_id):
    try:
        resource = Resource.objects.get(pk=resource_id)
        serialized_resource = ResourceSerializer(resource).data
        serialized_resource['provider'] = UserSerializer(User.objects.get(id=resource.provider_id)).data
        serialized_resource['provided_to'] = UserSerializer(User.objects.get(id=resource.provided_to_id)).data
        return Response(serialized_resource, status=status.HTTP_200_OK)
    except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_resources(request):
    resources = Resource.objects.all()
    serialized_resources = []
    for resource in resources:
        serialized_resource = ResourceSerializer(resource).data
        serialized_resource['provider'] = UserSerializer(User.objects.get(id=resource.provider_id)).data
        serialized_resource['provided_to'] = UserSerializer(User.objects.get(id=resource.provided_to_id)).data
        serialized_resources.append(serialized_resource)
    return Response(serialized_resources, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_resource(request, resource_id):
    try:
        resource = Resource.objects.get(pk=resource_id)
        serializer = ResourceSerializer(resource, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_resource(request, resource_id):
    try:
        resource = Resource.objects.get(pk=resource_id)
        resource.delete()
        return Response({"message": "Resource deleted successfully"}, status=status.HTTP_200_OK)
    except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approve_resource(request, resource_id):
    try:
        resource = Resource.objects.get(pk=resource_id)
        resource.approved = True
        resource.save()
        return Response({"message": "Resource approved successfully"}, status=status.HTTP_200_OK)
    except Resource.DoesNotExist:
        return Response({"message": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resources_by_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        provided_resources = Resource.objects.filter(provider=user)
        received_resources = Resource.objects.filter(provided_to=user)
        
        serialized_provided_resources = ResourceSerializer(provided_resources, many=True).data
        serialized_received_resources = ResourceSerializer(received_resources, many=True).data
        
        for resource in serialized_provided_resources:
            resource['provider'] = UserSerializer(user).data
            resource['provided_to'] = UserSerializer(User.objects.get(id=resource['provided_to'])).data if resource['provided_to'] else None
        
        for resource in serialized_received_resources:
            resource['provider'] = UserSerializer(User.objects.get(id=resource['provider'])).data if resource['provider'] else None
            resource['provided_to'] = UserSerializer(user).data
        
        return Response({
            'provided_resources': serialized_provided_resources,
            'received_resources': serialized_received_resources
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_announcement(request):
    # Extracting the created_by field from the request data
    created_by_id = request.data.get('created_by')

    # Check if the created_by_id is provided in the request data
    if created_by_id is None:
        return Response({"error": "created_by field is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the provided created_by_id is valid
    try:
        user = User.objects.get(pk=created_by_id)
    except User.DoesNotExist:
        return Response({"error": "Invalid created_by user"}, status=status.HTTP_400_BAD_REQUEST)

    # Assign the validated user to the created_by field in the request data
    request.data['created_by'] = user.id

    # Serialize the request data with the modified created_by field
    serializer = AnnouncementSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_announcements(request):
    announcements = Announcement.objects.all()
    serialized_announcements = []
    for announcement in announcements:
        serialized_announcement = AnnouncementSerializer(announcement).data
        serialized_announcement['created_by'] = UserSerializer(User.objects.get(id=announcement.created_by_id)).data
        serialized_announcements.append(serialized_announcement)
    return Response(serialized_announcements, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_announcement_by_id(request, pk):
    try:
        announcement = Announcement.objects.get(pk=pk)
        serialized_announcement = AnnouncementSerializer(announcement).data
        serialized_announcement['created_by'] = UserSerializer(User.objects.get(id=announcement.created_by_id)).data
        return Response(serialized_announcement, status=status.HTTP_200_OK)
    except Announcement.DoesNotExist:
        return Response({"message": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_announcements_by_created_by(request, id):
    try:
        announcements = Announcement.objects.filter(created_by=id)
        serialized_announcements = []
        for announcement in announcements:
            serialized_announcement = AnnouncementSerializer(announcement).data
            serialized_announcement['created_by'] = UserSerializer(User.objects.get(id=announcement.created_by_id)).data
            serialized_announcements.append(serialized_announcement)
        return Response(serialized_announcements, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(pk=announcement_id)
        
        serializer = AnnouncementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Announcement.DoesNotExist:
        return Response({"message": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_announcement(request, announcement_id):
    try:
        announcement = Announcement.objects.get(pk=announcement_id)        
        announcement.delete()
        return Response({"message": "Announcement deleted successfully"}, status=status.HTTP_200_OK)
    except Announcement.DoesNotExist:
        return Response({"message": "Announcement not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sharing(request):
    serializer = SharingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_sharings(request):
    sharings = Sharing.objects.all()
    serializer = SharingSerializer(sharings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sharing_by_id(request, sharing_id):
    try:
        sharing = Sharing.objects.get(pk=sharing_id)
        serializer = SharingSerializer(sharing)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sharing.DoesNotExist:
        return Response({"message": "Sharing not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_sharing(request, sharing_id):
    try:
        sharing = Sharing.objects.get(pk=sharing_id)
        serializer = SharingSerializer(sharing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Sharing.DoesNotExist:
        return Response({"message": "Sharing not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_sharing(request, sharing_id):
    try:
        sharing = Sharing.objects.get(pk=sharing_id)
        sharing.delete()
        return Response({"message": "Sharing deleted successfully"}, status=status.HTTP_200_OK)
    except Sharing.DoesNotExist:
        return Response({"message": "Sharing not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_reports(request):
    # Fetch counts from various models
    user_count = User.objects.count()
    story_count = Story.objects.count()
    comment_count = Comment.objects.count()
    resource_count = Resource.objects.count()
    active_connection_count = Connection.objects.filter(current_status=True).count()
    announcement_count = Announcement.objects.count()
    sharing_count = Sharing.objects.count()

    # Fetch counts for the additional models
    camp_count = Camp.objects.count()
    ngo_count = NGO.objects.count()
    idp_count = Idp.objects.count()
    host_count = Host.objects.count()

    # Calculate average comments per story
    avg_comments_per_story = Comment.objects.values('post').annotate(count=Count('id')).aggregate(avg=Avg('count'))['avg']

    # Create report dictionary
    report = {
        'total_users': user_count,
        'total_stories': story_count,
        'total_comments': comment_count,
        'total_resources': resource_count,
        'active_connections': active_connection_count,
        'average_comments_per_story': avg_comments_per_story,
        'total_announcements': announcement_count,
        'total_sharings': sharing_count,
        'total_camps': camp_count,
        'total_ngos': ngo_count,
        'total_idps': idp_count,
        'total_hosts': host_count,
    }

    return Response(report, status=status.HTTP_200_OK)