from django.urls import path

from kaf_pas.ckk.views import item_refs_location

urlpatterns = [

    path('Item_refs_location/Fetch/', item_refs_location.Item_refs_location_Fetch),
    path('Item_refs_location/Add', item_refs_location.Item_refs_location_Add),
    path('Item_refs_location/Update', item_refs_location.Item_refs_location_Update),
    path('Item_refs_location/Remove', item_refs_location.Item_refs_location_Remove),
    path('Item_refs_location/Lookup/', item_refs_location.Item_refs_location_Lookup),
    path('Item_refs_location/Info/', item_refs_location.Item_refs_location_Info),
    path('Item_refs_location/Copy', item_refs_location.Item_refs_location_Copy),

]
