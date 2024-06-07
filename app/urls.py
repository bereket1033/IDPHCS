from django.urls import path
from . import views

urlpatterns = [
    # Connection URLs
    path('connections/', views.get_connections, name='get_connections'),
    path('connections/create/', views.create_connection, name='create_connection'),
    path('connections/<int:connection_id>/', views.get_connection, name='get_connection'),
    path('connections/<int:connection_id>/delete/', views.delete_connection, name='delete_connection'),

    # Story URLs
    path('stories/', views.story_list_create, name='story-list-create'),
    path('stories/<int:pk>/', views.story_detail, name='story-detail'),
    path('stories/<int:story_id>/images/', views.upload_images, name='upload_image'),
    path('stories/<int:story_id>/detail/', views.get_story_by_id, name='get_story_by_id'),
    path('connected-stories/', views.get_connected_stories, name='get_connected_stories'),

    # Comment URLs
    path('comments/', views.create_comment, name='create_comment'),
    path('comments/<int:comment_id>/', views.get_comment, name='get_comment'),
    path('comments/<int:comment_id>/update/', views.update_comment, name='update_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # Complain URLs
    path('complains/', views.create_complain, name='create_complain'),
    path('complains/all/', views.get_all_complains, name='get_all_complains'),
    path('complains/<int:complain_id>/', views.get_complain_by_id, name='get_complain_by_id'),
    path('complains/<int:complain_id>/update/', views.update_complain, name='update_complain'),
    path('complains/<int:complain_id>/delete/', views.delete_complain, name='delete_complain'),

    # Report URLs
    path('reports/', views.create_report, name='create_report'),
    path('reports/all/', views.get_all_reports, name='get_all_reports'),
    path('reports/<int:report_id>/', views.get_report_by_id, name='get_report_by_id'),
    path('reports/<int:report_id>/update/', views.update_report, name='update_report'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),

    # Resource URLs
    path('resources/', views.create_resource, name='create_resource'),
    path('resources/all/', views.get_all_resources, name='get_all_resources'),
    path('resources/<int:resource_id>/', views.get_resource, name='get_resource'),
    path('resources/<int:resource_id>/update/', views.update_resource, name='update_resource'),
    path('resources/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),
    path('resources/<int:resource_id>/approve/', views.approve_resource, name='approve_resource'),
    path('resources/user/<int:user_id>/', views.get_resources_by_user, name='get_resources_by_user'),

    # Announcement URLs
    path('announcements/', views.create_announcement, name='create_announcement'),
    path('announcements/all/', views.get_all_announcements, name='get_announcements'),
    path('announcements/<int:pk>/', views.get_announcement_by_id, name='get_announcement_by_id'),
    path('announcements/<int:announcement_id>/update/', views.update_announcement, name='update_announcement'),
    path('announcements/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),
    path('announcements/user/<int:id>/', views.get_announcements_by_created_by, name='get_announcements_by_user'),

    # Sharing URLs
    path('sharings/', views.create_sharing, name='create_sharing'),
    path('sharings/all/', views.get_all_sharings, name='get_all_sharings'),
    path('sharings/<int:sharing_id>/', views.get_sharing_by_id, name='get_sharing_by_id'),
    path('sharings/<int:sharing_id>/update/', views.update_sharing, name='update_sharing'),
    path('sharings/<int:sharing_id>/delete/', views.delete_sharing, name='delete_sharing'),

    path('search-users/', views.search_users, name='search_users'),
    path('totalreports/', views.get_reports, name='get_reports'),
    path('messages/', views.get_all_messages, name='get_all_messages'),

    
]
