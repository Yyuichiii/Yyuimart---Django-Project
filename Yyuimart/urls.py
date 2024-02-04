from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User_Account.urls')),
    path('products/', include('Product.urls')),
    path('api/', include('API.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)