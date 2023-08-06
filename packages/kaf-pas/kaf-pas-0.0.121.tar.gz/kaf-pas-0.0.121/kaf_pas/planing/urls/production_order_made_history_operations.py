from django.urls import path

from kaf_pas.planing.views import production_order_made_history_operations

urlpatterns = [

    path('Production_order_made_history_operations/Fetch/', production_order_made_history_operations.Production_order_made_history_operations_Fetch),
    path('Production_order_made_history_operations/Add', production_order_made_history_operations.Production_order_made_history_operations_Add),
    path('Production_order_made_history_operations/Update', production_order_made_history_operations.Production_order_made_history_operations_Update),
    path('Production_order_made_history_operations/Remove', production_order_made_history_operations.Production_order_made_history_operations_Remove),
    path('Production_order_made_history_operations/Lookup/', production_order_made_history_operations.Production_order_made_history_operations_Lookup),
    path('Production_order_made_history_operations/Info/', production_order_made_history_operations.Production_order_made_history_operations_Info),
    path('Production_order_made_history_operations/Copy', production_order_made_history_operations.Production_order_made_history_operations_Copy),

]
