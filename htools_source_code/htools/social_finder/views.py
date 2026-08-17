from django.shortcuts import render
import requests

def social_finder(request):
    results = {}
    username = None

    if request.method == "POST":
        username = request.POST.get("username")

        if username:
            sites = {
                "GitHub": f"https://github.com/{username}",
                "Instagram": f"https://www.instagram.com/{username}/",
                "Facebook": f"https://www.facebook.com/{username}",
                "Twitter": f"https://twitter.com/{username}",
                "Snapchat": f"https://www.snapchat.com/add/{username}",
            }

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            for site, url in sites.items():
                try:
                    response = requests.get(url, headers=headers, timeout=5)

                    if response.status_code == 200:
                        results[site] = {
                            "url": url,
                            "status": "Found"
                        }
                    else:
                        results[site] = {
                            "url": url,
                            "status": "Not Found"
                        }

                except requests.RequestException:
                    results[site] = {
                        "url": url,
                        "status": "Error"
                    }

    return render(request, "social_finder/finder.html", {
        "results": results,
        "username": username
    })