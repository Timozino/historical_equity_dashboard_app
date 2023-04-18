
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from dashboard.views import TradingAccountViewSet
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
    openapi.Info(
        title="historical equity dashboard app by Timson",
        default_version='v1',
        description="API documentation using Swagger/OpenAPI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="timsonfoli@gmail.com"),
        license=openapi.License(name="ATAFRICA TEAM License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'TradingAccount', TradingAccountViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('open-api/', include(router.urls)),
    path('docs/', include_docs_urls(title='API Documentation')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]



admin.site.site_header = "Historical Equity Dashboard App"
admin.site.site_title = "Historical Equity Dashboard App"
admin.site.index_title = "Historical Equity Dashboard App"



urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
