from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import LostItem, FoundItem
import json

import json
from django.http import JsonResponse
from .models import LostItem, FoundItem

import json
from django.http import JsonResponse
from .models import LostItem, FoundItem

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
            "found_by__first_name", "found_by__last_name"
        )

        formatted_items = [
            {
                "id": item["id"],
                "found_by": f"{item['found_by__first_name']} {item['found_by__last_name']}".strip(),
                "item": item["name"],
                "description": item["description"],
                "location": item["location"],
                "date_found": item["date_found"],
                "claimed": item["claimed"]
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
