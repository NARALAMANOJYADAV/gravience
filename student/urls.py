from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('counseling.urls')),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve the root styles.css file during development so templates that link to /styles.css work
    from django.views.static import serve
    # Serve the root styles.css during development. Use the built-in serve view with kwargs.
    urlpatterns += [
        path('styles.css', serve, {'path': 'styles.css', 'document_root': str(settings.BASE_DIR)}),
    ]
