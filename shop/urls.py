from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopapp.urls')), #name your app
    path('auth/', include('social_django.urls', namespace='social')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
