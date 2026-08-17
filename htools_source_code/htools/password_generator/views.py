from django.shortcuts import render
import secrets
import string


def generate_password(request):
    password = None
    error = None

    if request.method == "POST":
        try:
            length = int(request.POST.get("length"))

            use_upper = request.POST.get("uppercase")
            use_lower = request.POST.get("lowercase")
            use_digits = request.POST.get("digits")
            use_symbols = request.POST.get("symbols")

            if length < 4:
                error = "Password length must be at least 4."
            else:
                character_pool = ""

                if use_upper:
                    character_pool += string.ascii_uppercase
                if use_lower:
                    character_pool += string.ascii_lowercase
                if use_digits:
                    character_pool += string.digits
                if use_symbols:
                    character_pool += string.punctuation

                if not character_pool:
                    error = "Select at least one character type."
                else:
                    password_chars = []

                    # Ensure at least one character from each selected category
                    if use_upper:
                        password_chars.append(
                            secrets.choice(string.ascii_uppercase))
                    if use_lower:
                        password_chars.append(
                            secrets.choice(string.ascii_lowercase))
                    if use_digits:
                        password_chars.append(secrets.choice(string.digits))
                    if use_symbols:
                        password_chars.append(
                            secrets.choice(string.punctuation))

                    # Fill remaining length
                    while len(password_chars) < length:
                        password_chars.append(secrets.choice(character_pool))

                    # Shuffle securely
                    secrets.SystemRandom().shuffle(password_chars)

                    password = ''.join(password_chars)

        except:
            error = "Invalid input."

    return render(request, "password_generator/generator.html", {
        "password": password,
        "error": error
    })
