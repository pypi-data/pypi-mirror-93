from django.urls import path

from kaf_pas.planing.views import production_order_made_history

urlpatterns = [

    path('Production_order_made_history/Fetch/', production_order_made_history.Production_order_made_history_Fetch),
    path('Production_order_made_history/Add', production_order_made_history.Production_order_made_history_Add),
    path('Production_order_made_history/Update', production_order_made_history.Production_order_made_history_Update),
    path('Production_order_made_history/Remove', production_order_made_history.Production_order_made_history_Remove),
    path('Production_order_made_history/Lookup/', production_order_made_history.Production_order_made_history_Lookup),
    path('Production_order_made_history/Info/', production_order_made_history.Production_order_made_history_Info),
    path('Production_order_made_history/Copy', production_order_made_history.Production_order_made_history_Copy),

]
