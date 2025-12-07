import os

def bunny(request):
    return {
        "bunny_host": os.getenv("BUNNY_CDN_PULL_ZONE_HOSTNAME", ""),
        "bunny_storage_zone": os.getenv("BUNNY_STORAGE_ZONE", ""),
    }
