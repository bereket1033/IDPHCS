from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.models import Host, Idp, NGO, Camp, Image
from .serializers import HostSerializer, IdpSerializer, NGOSerializer, CampSerializer, ImageSerializer
from datetime import datetime
from django.conf import settings
import os
from django.contrib.auth.hashers import check_password




@api_view(['PUT'])
def update_host(request, host_id):
    try:
        host = Host.objects.get(pk=host_id)
    except Host.DoesNotExist:
        return Response({"Message": "There is no user account by this ID"},status=status.HTTP_404_NOT_FOUND)

    serializer = HostSerializer(host, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_idp(request, idp_id):
    try:
        idp = Idp.objects.get(pk=idp_id)
    except Idp.DoesNotExist:
        return Response({"Message": "There is no user account by this ID"},status=status.HTTP_404_NOT_FOUND)

    serializer = IdpSerializer(idp, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"Message": "There is no user account by this ID"},serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_ngo(request, ngo_id):
    try:
        ngo = NGO.objects.get(pk=ngo_id)
    except NGO.DoesNotExist:
        return Response({"Message": "There is no user account by this ID"},status=status.HTTP_404_NOT_FOUND)

    serializer = NGOSerializer(ngo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_camp(request, camp_id):
    try:
        camp = Camp.objects.get(pk=camp_id)
    except Camp.DoesNotExist:
        return Response({"Message": "There is no user account by this ID"},status=status.HTTP_404_NOT_FOUND)

    serializer = CampSerializer(camp, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Assuming the image file is sent in the request
        image_file = request.FILES['image']

        # Assuming you have a user profile associated with the request user
        user_profile = request.user.actorprofile

        # Check if an image is already uploaded for the user profile
        existing_image = Image.objects.filter(profile=user_profile).first()
        if existing_image:
            return Response({"message": "Profile photo is already uploaded"}, status=400)

        # Create a new Image instance
        image = Image(profile=user_profile, created_at=datetime.now(), deleted_at=None, status='Active')

        # Save the uploaded image to the filesystem
        image.image_url = handle_uploaded_file(image_file)

        # Save the image instance
        image.save()

        # Serialize the image data for response
        serializer = ImageSerializer(image)

        return Response(serializer.data)

    return Response({'error': 'No image file provided'}, status=400)

def handle_uploaded_file(f):
    # Define the upload directory
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    # Generate a unique filename
    filename = str(datetime.now().timestamp()) + '_' + f.name

    # Write the uploaded file to the filesystem
    with open(os.path.join(upload_dir, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Return the URL where the file is saved
    return os.path.join('images', filename)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    if request.method == 'POST':
        # Retrieve the old and new passwords from the request data
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Retrieve the authenticated user
        user = request.user

        # Check if the provided old password matches the user's current password
        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # Update the password for the user
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)