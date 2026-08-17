from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import time

def landing_page(request):
    today_date = time.strftime("%B %d, %Y")
    context = {
        "current_time": today_date
    }
    return render(request, "home/landing.html", context)

@login_required
def dashboard(request):
    return render(request, "home/dashboard.html")
