from django.urls import path
from .views import (
    lost_items,
    found_items,
    match_items,
    delete_lost_item,
    delete_found_item
)

urlpatterns = [
    path("lost-items/", lost_items, name="report_lost_item"),
    path("found-items/", found_items, name="report_found_item"),
    path("match-items/", match_items, name="match_items"),
    path("lost-items/<int:id>/", delete_lost_item, name="delete_lost_item"),
    path("found-items/<int:id>/", delete_found_item, name="delete_found_item"),
]
