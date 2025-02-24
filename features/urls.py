from django.urls import path
from .views import *

urlpatterns = [
    path("lost-items/", lost_items, name="report_lost_item"),
    path("found-items/", found_items, name="report_found_item"),
    path("match-items/", match_items, name="match_items"),
    path("lost-items/<int:id>/", delete_lost_item, name="delete_lost_item"),
    path("found-items/<int:id>/", delete_found_item, name="delete_found_item"),
    
    #####--------OPTIONAL FEATURES----#######
    path("lost-items/claim/<int:item_id>/", claim_found_item, name="claim_found_item"),
    path("nearby-lost-items/", nearby_lost_items, name="nearby_lost_items"),
    path("found-items/upload-image/", upload_found_item_image, name="upload_found_item_image"),
    path("lost-items/history/", user_lost_items_history, name="user_lost_items_history"),
]
