from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    # path('/', home_view), 
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('auth/', include('auth.urls')),
    path('accountmgt/', include('accounts.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
