from django.shortcuts import render
import re


def check_strength(request):
    strength = None
    score = 0
    suggestions = []
    password = ""   
    if request.method == "POST":
        password = request.POST.get("password", "")

        if password:
            length = len(password)

            if length >= 8:
                score += 1
            else:
                suggestions.append("Use at least 8 characters.")

            if length >= 12:
                score += 1

            if re.search(r"[A-Z]", password):
                score += 1
            else:
                suggestions.append("Add uppercase letters.")

            if re.search(r"[a-z]", password):
                score += 1
            else:
                suggestions.append("Add lowercase letters.")

            if re.search(r"[0-9]", password):
                score += 1
            else:
                suggestions.append("Add numbers.")

            if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                score += 1
            else:
                suggestions.append("Add special symbols.")

            if score <= 2:
                strength = "Weak"
            elif score <= 4:
                strength = "Moderate"
            elif score == 5:
                strength = "Strong"
            else:
                strength = "Very Strong"

    return render(request, "pass_strength_checker/checker.html", {
        "strength": strength,
        "score": score,
        "suggestions": suggestions,
        "password": password
    })
