from django.conf import settings

def global_settings(request):
    return {
        "SITE_DOMAIN": getattr(settings, "SITE_DOMAIN", ""),
    }
