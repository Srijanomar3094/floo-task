from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
import json

def user_register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        name = data.get("name", "").strip()

        if not email or not password or not name:
            return JsonResponse({"error": "Email, password, and name are required"}, status=400)

        if len(password) < 6:
            return JsonResponse({"error": "Password must be at least 6 characters long"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        name_parts = name.split()
        first_name = name_parts[0]
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=email, password=password, email=email,
            first_name=first_name, last_name=last_name
        )

        return JsonResponse({"message": "User registered successfully"}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)



def user_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()

        if not email or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)


def user_logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in"}, status=400)

    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)
