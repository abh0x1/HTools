from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("tools/url-status_checker/", include("url_status_checker.urls")),
    path("tools/header-grabber/", include("header_grabber.urls")),
    path("tools/web-screenshot/", include("web_screenshot.urls")),
    path("tools/ip-info/", include("ip_information.urls")),
    path("tools/password-generator/", include("password_generator.urls")),
    path("tools/password-strength-checker/",
         include("pass_strength_checker.urls")),
    path("tools/hash-generator/", include("hash_generator.urls")),
    path("tools/base64-tool/", include("base64_tool.urls")),
    path("tools/social-finder/", include("social_finder.urls")),
    path("tools/whois-checker/", include("whois_checker.urls")),
    path("", include("home.urls")),
]
