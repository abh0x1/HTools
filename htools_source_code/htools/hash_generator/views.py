from django.shortcuts import render
import hashlib


def generate_hash(request):
    hash_result = None
    selected_algo = None
    error = None

    if request.method == "POST":
        text = request.POST.get("text")
        algorithm = request.POST.get("algorithm")

        if not text:
            error = "Please enter text."
        else:
            try:
                encoded_text = text.encode('utf-8')

                if algorithm == "md5":
                    hash_result = hashlib.md5(encoded_text).hexdigest()
                elif algorithm == "sha1":
                    hash_result = hashlib.sha1(encoded_text).hexdigest()
                elif algorithm == "sha256":
                    hash_result = hashlib.sha256(encoded_text).hexdigest()
                elif algorithm == "sha512":
                    hash_result = hashlib.sha512(encoded_text).hexdigest()
                else:
                    error = "Invalid algorithm selected."

                selected_algo = algorithm

            except Exception:
                error = "Something went wrong."

    return render(request, "hash_generator/hash.html", {
        "hash_result": hash_result,
        "selected_algo": selected_algo,
        "error": error
    })
