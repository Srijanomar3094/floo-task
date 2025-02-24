from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import LostItem, FoundItem
import json
from django.contrib.auth.models import User

def lost_items(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["name", "description", "location", "date_lost"]

            if not all(key in data for key in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            item = LostItem.objects.create(
                lost_by=request.user,
                name=data["name"],
                description=data["description"],
                location=data["location"],
                date_lost=data["date_lost"]
            )
            return JsonResponse({"message": "Lost item reported", "id": item.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "GET":
        items = LostItem.objects.select_related("lost_by").values(
            "id", "name", "description", "location", "date_lost", "is_found",
            "lost_by__first_name", "lost_by__last_name"
        )
        
        formatted_items = [
            {
                "id": item["id"],
                "lost_by": f"{item['lost_by__first_name']} {item['lost_by__last_name']}".strip(),
                "item": item["name"],
                "description": item["description"],
                "location": item["location"],
                "date_lost": item["date_lost"],
                "is_found": item["is_found"]
            }
            for item in items
        ]

        return JsonResponse({"lost_items": formatted_items}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def found_items(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            required_fields = ["name", "description", "location", "date_found"]

            if not all(key in data for key in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            item = FoundItem.objects.create(
                found_by=request.user,
                name=data["name"],
                description=data["description"],
                location=data["location"],
                date_found=data["date_found"]
            )
            return JsonResponse({"message": "Found item reported", "id": item.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    elif request.method == "GET":
        items = FoundItem.objects.select_related("found_by").values(
            "id", "name", "description", "location", "date_found", "claimed",
            "found_by__first_name", "found_by__last_name","image"
        )

        formatted_items = [
            {
                "id": item["id"],
                "found_by": f"{item['found_by__first_name']} {item['found_by__last_name']}".strip(),
                "item": item["name"],
                "description": item["description"],
                "location": item["location"],
                "date_found": item["date_found"],
                "claimed": item["claimed"],
                "image": item['image']
            }
            for item in items
        ]

        return JsonResponse({"found_items": formatted_items}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)



def match_items(request):
    matched = []
    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    
    for lost in lost_items:
        for found in found_items:
            if (
                lost.name.lower() == found.name.lower() and 
                lost.location.lower() == found.location.lower()
            ):
                matched.append({
                    "lost_item": lost.name, 
                    "found_item": found.name, 
                    "found_location": found.location
                })
    
    return JsonResponse({"matches": matched})


def delete_lost_item(request, id):
    if request.method == "DELETE":
        try:
            LostItem.objects.filter(id=id).update(status=False)
            return JsonResponse({"message": "Lost item removed"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Lost item not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)


def delete_found_item(request, id):
    if request.method == "DELETE":
        try:
            LostItem.objects.filter(id=id).update(status=False)
            return JsonResponse({"message": "Found item removed"}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Found item not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=405)



############# OPTIONAL FEATURES #################################


def claim_found_item(request, item_id):
    if request.method == "POST":
        try:
            item = FoundItem.objects.get(id=item_id)
            if item.claimed:
                return JsonResponse({"error": "Item already claimed"}, status=400)

            item.claimed = True
            item.save()
            return JsonResponse({"message": "Item successfully claimed"}, status=200)
        except FoundItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def nearby_lost_items(request):
    location = request.GET.get("location")
    if not location:
        return JsonResponse({"error": "Location parameter is required"}, status=400)

    items = LostItem.objects.filter(location__icontains=location).values(
        "id", "name", "description", "location", "date_lost", "is_found"
    )
    return JsonResponse({"lost_items": list(items)}, status=200)



def upload_found_item_image(request):
    if request.method == "POST" and request.FILES.get("image") and request.POST.get("item_id"):
        item_id = request.POST["item_id"]
        try:
            item = FoundItem.objects.get(id=item_id)
            image = request.FILES["image"]
            item.image = image
            item.save()
            return JsonResponse({"message": "Image uploaded successfully", "image_url": item.image.url}, status=201)
        except FoundItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

    return JsonResponse({"error": "Invalid request or missing file"}, status=400)


def user_lost_items_history(request):
    user_id = request.GET.get("user_id")
    if not user_id:
        return JsonResponse({"error": "User ID parameter is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        items = LostItem.objects.filter(lost_by=user).values(
            "id", "name", "description", "location", "date_lost", "is_found"
        )
        return JsonResponse({"lost_items": list(items)}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)