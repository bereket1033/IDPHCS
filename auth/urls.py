from django.urls import path
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UserProfileAPIView, UserListAPIView, register_ngo, register_host, register_camp, register_volunteer, register_idppre, register_idp, activate_user, deactivate_user



urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', UserProfileAPIView, name='user_profile'),
    path('users/', UserListAPIView, name='user-list'),
    path('register-ngo/', register_ngo, name='register_ngo'),
    path('register-host/', register_host, name='register_host'),
    path('register_camp/',register_camp, name='register_camp'),
    path('register_volunteer/', register_volunteer, name='register_volunteer'),
    path('register_idppre/', register_idppre, name='register_idppre'),
    path('register_idp/', register_idp, name='register_idp'),
    path('activate-user/<int:user_id>/', activate_user, name='activate-user'),
    path('deactivate-user/<int:user_id>/', deactivate_user, name='deactivate-user'),

]