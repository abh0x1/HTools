# ip_information/views.py
from django.shortcuts import render
import ipaddress
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError


def ip_info(request):
    result = None
    user_ip = request.META.get("REMOTE_ADDR")

    if request.method == "POST":
        ip = request.POST.get("ip")

        try:
            # Handle CIDR notation
            if '/' in ip:
                net = ipaddress.ip_network(ip, strict=False)
                ip_to_check = str(list(net.hosts())[0])  # first usable IP
            else:
                ip_to_check = ip

            ip_obj = ipaddress.ip_address(ip_to_check)

            # Handle private or loopback IPs first
            if ip_obj.is_private or ip_obj.is_loopback:
                result = {
                    "ip": ip,
                    "version": f"IPv{ip_obj.version}",
                    "is_private": ip_obj.is_private,
                    "is_global": ip_obj.is_global,
                    "is_loopback": ip_obj.is_loopback,
                    "error": "Private or loopback IP – WHOIS not available"
                }
            else:
                # Public IP – perform WHOIS lookup
                try:
                    whois = IPWhois(ip_to_check)
                    data = whois.lookup_rdap()
                    network = data.get("network", {})
                    objects = data.get("objects", {})

                    contacts = []
                    for obj in objects.values():
                        contact = obj.get("contact", {})
                        roles = obj.get("roles", [])
                        contacts.append({
                            "roles": ", ".join(roles) if roles else "N/A",
                            "name": contact.get("name", "N/A"),
                            "organization": contact.get("organization", "N/A"),
                            "email": contact.get("email", [{}])[0].get("value") if contact.get("email") else "N/A",
                            "phone": contact.get("phone", [{}])[0].get("value") if contact.get("phone") else "N/A",
                            "address": contact.get("address", [{}])[0].get("value") if contact.get("address") else "N/A",
                        })

                    result = {
                        "ip": ip,
                        "version": f"IPv{ip_obj.version}",
                        "is_private": ip_obj.is_private,
                        "is_global": ip_obj.is_global,
                        "is_loopback": ip_obj.is_loopback,
                        "asn": data.get("asn", "N/A"),
                        "asn_org": data.get("asn_description", "N/A"),
                        "asn_country": data.get("asn_country_code", "N/A"),
                        "registry": data.get("asn_registry", "N/A"),
                        "network_name": network.get("name", "N/A"),
                        "cidr": network.get("cidr", "N/A"),
                        "ip_range": f'{network.get("start_address", "N/A")} - {network.get("end_address", "N/A")}',
                        "network_type": network.get("type", "N/A"),
                        "status": network.get("status", "N/A"),
                        "created": network.get("created", "N/A"),
                        "updated": network.get("last_changed", "N/A"),
                        "contacts": contacts
                    }

                except IPDefinedError:
                    result = {
                        "error": "This IP is private/reserved – WHOIS not available"}
                except Exception:
                    result = {"error": "WHOIS lookup failed"}

        except ValueError:
            result = {"error": "Invalid IP address / CIDR"}

    return render(request, "ip_information/index.html", {
        "result": result,
        "user_ip": user_ip
    })
