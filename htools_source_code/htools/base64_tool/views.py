from django.shortcuts import render
import base64


def base64_encoder_decoder(request):
    result = None
    error = None
    operation = None

    if request.method == "POST":
        text = request.POST.get("text")
        operation = request.POST.get("operation")

        if not text:
            error = "Please enter text."
        else:
            try:
                if operation == "encode":
                    encoded_bytes = base64.b64encode(text.encode("utf-8"))
                    result = encoded_bytes.decode("utf-8")

                elif operation == "decode":
                    decoded_bytes = base64.b64decode(text.encode("utf-8"))
                    result = decoded_bytes.decode("utf-8")

                else:
                    error = "Invalid operation selected."

            except Exception:
                error = "Invalid Base64 input for decoding."

    return render(request, "base64_tool/base64.html", {
        "result": result,
        "error": error,
        "operation": operation
    })
