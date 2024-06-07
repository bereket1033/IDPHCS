from django.contrib import admin
from .models import UserType, ActorProfile,Image, Camp, Idp, Host, NGO, Story, Photo, Sharing, Comment, Notification, Resource, Message, IdpCampAssociation, IdpVolunteerAssociation, IdpNGOAssociation, ActorProfileResourceAssociation, ResourceIdpAssociation, Connection

# Register your models here.

admin.site.register(UserType)
admin.site.register(ActorProfile)
admin.site.register(Image)
admin.site.register(Camp)
admin.site.register(Idp)
admin.site.register(Host)
admin.site.register(NGO)
admin.site.register(Story)
admin.site.register(Photo)
admin.site.register(Sharing)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Resource)
admin.site.register(Message)
admin.site.register(IdpCampAssociation)
admin.site.register(IdpVolunteerAssociation)
admin.site.register(IdpNGOAssociation)
admin.site.register(ActorProfileResourceAssociation)
admin.site.register(ResourceIdpAssociation)
admin.site.register(Connection)
