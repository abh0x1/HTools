import whois
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    context = {}

    if request.method == "POST":
        domain = request.POST.get("domain", "").strip()

        # Clean domain input
        domain = domain.replace("https://", "").replace("http://", "")
        domain = domain.replace("www.", "").split("/")[0]

        if not domain:
            context["error"] = "Please enter a valid domain name."
            return render(request, "whois_checker/index.html", context)

        try:
            data = whois.whois(domain)

            # Helper function to safely extract values
            def clean_value(value):
                if isinstance(value, list):
                    return value[0]
                return value if value else "Not Available"

            whois_data = {
                "domain_name": clean_value(data.domain_name),
                "registrar": clean_value(data.registrar),
                "registrar_url": clean_value(getattr(data, "registrar_url", None)),
                "reseller": clean_value(getattr(data, "reseller", None)),
                "whois_server": clean_value(getattr(data, "whois_server", None)),
                "referral_url": clean_value(getattr(data, "referral_url", None)),
                "updated_date": clean_value(data.updated_date),
                "creation_date": clean_value(data.creation_date),
                "expiration_date": clean_value(data.expiration_date),
                "name_servers": data.name_servers if data.name_servers else [],
                "status": data.status if data.status else [],
                "emails": data.emails if data.emails else [],
                "dnssec": clean_value(getattr(data, "dnssec", None)),
                "name": clean_value(getattr(data, "name", None)),
                "org": clean_value(getattr(data, "org", None)),
                "address": clean_value(getattr(data, "address", None)),
                "city": clean_value(getattr(data, "city", None)),
                "state": clean_value(getattr(data, "state", None)),
                "registrant_postal_code": clean_value(getattr(data, "registrant_postal_code", None)),
                "country": clean_value(getattr(data, "country", None)),
            }

            context["result"] = whois_data

        except Exception:
            context["error"] = "Unable to fetch WHOIS data. Please check the domain."

    return render(request, "whois_checker/index.html", context)
