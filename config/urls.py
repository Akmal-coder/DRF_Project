from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from materials.views import api_root  # Этот импорт должен работать

urlpatterns = [
    path('', api_root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('materials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )