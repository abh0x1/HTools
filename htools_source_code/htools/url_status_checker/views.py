from django.shortcuts import render
import requests
from concurrent.futures import ThreadPoolExecutor


def index(request):
    """
    Show the main page where users enter URLs
    """
    return render(request, "url_status_checker/index.html")


def check_single_url_status(url):
    """
    Check the status of ONE website URL
    Returns a message about whether it's working or not
    """
    try:
        # Try to visit the website
        response = requests.get(url, timeout=5)
        status_code = response.status_code

        # Check what kind of response we got
        if status_code == 200:
            return f"✅ {url} >>> Working perfectly! (Code: {status_code})"
        elif status_code == 300:
            return f"↪️ {url} >>> Redirected elsewhere (Code: {status_code})"
        elif status_code == 403:
            return f"⛔ {url} >>> Access forbidden (Code: {status_code})"
        elif status_code == 404:
            return f"❌ {url} >>> Page not found (Code: {status_code})"
        elif status_code >= 500:
            return f"🔥 {url} >>> Server error (Code: {status_code})"
        else:
            return f"❓ {url} >>> Unknown response (Code: {status_code})"

    except requests.exceptions.RequestException:
        # If we can't even connect to the website
        return f"🚫 {url} >>> Cannot reach this website"


def check_status(request):  # CHANGED BACK TO ORIGINAL NAME
    """
    Main function that handles URL checking
    """
    results = []

    # Only run if user submitted the form (clicked "Check URLs")
    if request.method == "POST":
        # Get the URLs the user typed
        urls_text = request.POST.get("urls", "")

        # Split by lines and clean up
        url_lines = urls_text.splitlines()

        cleaned_urls = []

        for url in url_lines:
            url = url.strip()
            if not url:  # Skip empty lines
                continue

            # Add http:// if no protocol specified
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            cleaned_urls.append(url)

        # Check all URLs at the same time (using 10 "workers")
        if cleaned_urls:
            with ThreadPoolExecutor(max_workers=10) as executor:
                # Check all URLs simultaneously
                results = list(executor.map(
                    check_single_url_status, cleaned_urls))

    # Show the results page
    return render(
        request,
        "url_status_checker/result.html",
        {"results": results}
    )
