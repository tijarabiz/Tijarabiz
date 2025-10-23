from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("apps.website.urls")),
    path("core/", include("apps.core.urls")),
    path("planner/", include("apps.planner.urls")),
    path("clients/", include("apps.clients.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("staff/", include("apps.staff.urls")),
    path("marketing/", include("apps.marketing.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("trends/", include("apps.trends.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
