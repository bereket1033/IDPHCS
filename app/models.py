from django.contrib.auth.models import User
from django.db import models

USER_TYPES = (
    ('IDP', 'IDP'),
    ('Host', 'Host'),
    ('Volunteer', 'Volunteer'),
    ('NDRMC Admin', 'NDRMC Admin'),
    ('Camp Admin', 'Camp Admin'),
    ('NGO', 'NGO'),
)

class UserType(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

class ActorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    user_type = models.CharField(max_length=100, choices=USER_TYPES)

class Image(models.Model):
    profile = models.OneToOneField(ActorProfile, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Camp(models.Model):
    profile = models.OneToOneField(ActorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    current_population = models.IntegerField()
    demographic_info = models.JSONField()
    shelter_type = models.CharField(max_length=100)
    economic_activities = models.TextField()
    health_education_info = models.JSONField()
    status = models.CharField(max_length=100)

class Idp(models.Model):
    profile = models.OneToOneField(ActorProfile, on_delete=models.CASCADE)
    place_of_origin = models.CharField(max_length=100)
    contact_information = models.CharField(max_length=100)
    household_composition = models.IntegerField()
    vulnerability_status = models.CharField(max_length=100)
    health_status = models.CharField(max_length=100)
    documentation_status = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    language_spoken = models.CharField(max_length=100)
    previous_assistance_received = models.CharField(max_length=100)
    protection_concerns = models.CharField(max_length=100)
    economic_status = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

class Host(models.Model):
    profile = models.OneToOneField(ActorProfile, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    preference = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    hosting_experience = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    legal_doc_id = models.CharField(max_length=100)
    economic_status = models.CharField(max_length=100)

class NGO(models.Model):
    profile = models.OneToOneField(ActorProfile, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    capacity = models.IntegerField()
    name = models.CharField(max_length=100)
    legal_doc = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class Story(models.Model):
    idp = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)
    story_text = models.TextField()
    shared_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Photo(models.Model):
    story = models.ForeignKey(Story, related_name='photos', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Sharing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Story, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, related_name='shared_with', on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Story, on_delete=models.CASCADE)
    comment_text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Notification(models.Model):
    user = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    resource_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='provided_resources')
    provided_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_resources')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    approved = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    message_text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='active')

class IdpCampAssociation(models.Model):
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    idpemail = models.EmailField(unique=True)  # Ensure email is unique
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
class IdpVolunteerAssociation(models.Model):
    idp = models.ForeignKey(ActorProfile, on_delete=models.CASCADE, related_name='idp_volunteer_associations')
    volunteer = models.ForeignKey(ActorProfile, on_delete=models.CASCADE, related_name='volunteer_associations')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

class IdpNGOAssociation(models.Model):
    idp = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)

class ActorProfileResourceAssociation(models.Model):
    actor_profile = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

class ResourceIdpAssociation(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    idp = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)
    usage_date = models.DateTimeField(auto_now_add=True)
    quantity_used = models.IntegerField()

class IDPPre(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    current_status = models.BooleanField(default=True)
    
class Report(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reported_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_received')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='Active')

class Complain(models.Model):
    complained_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_made')
    complained_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_received')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default='Active')

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_announcements')