import requests
from django.shortcuts import render

SECURITY_HEADERS = {
    "Strict-Transport-Security": "Protects against MITM attacks (HTTPS enforcement)",
    "Content-Security-Policy": "Prevents XSS and data injection",
    "X-Frame-Options": "Prevents clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME-sniffing",
    "Referrer-Policy": "Controls referrer information",
    "Permissions-Policy": "Restricts browser features"
}


def header_form(request):
    if request.method == "POST":
        url = request.POST.get("url")

        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            server_headers = response.headers

            found = 0
            header_status = []

            for key, desc in SECURITY_HEADERS.items():
                is_present = key in server_headers
                if is_present:
                    found += 1

                header_status.append({
                    "name": key,
                    "description": desc,
                    "found": is_present
                })

            score = round((found / len(SECURITY_HEADERS)) * 100, 2)

            context = {
                "url": url,
                "server": server_headers.get("Server", "Not Exposed"),
                "powered_by": server_headers.get("X-Powered-By", "Not Exposed"),
                "headers": header_status,
                "score": score
            }

            return render(request, "header_grabber/header_result.html", context)

        except requests.exceptions.RequestException:
            return render(request, "header_grabber/header_form.html", {
                "error": "Unable to connect to the provided URL."
            })

    return render(request, "header_grabber/header_form.html")
