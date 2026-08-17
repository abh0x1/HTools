from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def site_checker(request):
    context = {}

    if request.method == "POST":
        url = request.POST.get("url")
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                title = soup.title.string if soup.title else "No title found"
                context = {"url": url, "status": "UP", "title": title}
            else:
                context = {"url": url, "status": "DOWN",
                           "code": res.status_code}
        except Exception as e:
            context = {"error": str(e)}

    return render(request, "web_screenshot/checker.html", context)
