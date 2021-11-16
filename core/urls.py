from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core import settings

urlpatterns = [
    path('', include('app.cafecode.urls')),
    path('contactus/', include('app.contact_us.urls')),
    path('account/', include('app.account.urls')),
    path('d-admin/', admin.site.urls),
    path('blog/', include('app.blog.urls')),
    path('product/', include('app.product.urls')),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
