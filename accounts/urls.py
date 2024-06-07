from django.urls import path
from .views import update_host, update_idp, update_ngo, update_camp, upload_image, update_password

urlpatterns = [
    path('hosts/<int:host_id>/', update_host, name='update_host'),
    path('idps/<int:idp_id>/', update_idp, name='update_idp'),
    path('ngos/<int:ngo_id>/', update_ngo, name='update_ngo'),
    path('camps/<int:camp_id>/', update_camp, name='update_camp'),
    path('upload_image/', upload_image, name='upload_image'),
    path('update_password/', update_password, name='update_password'),

]
