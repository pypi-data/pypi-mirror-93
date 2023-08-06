from django.urls import path

from kaf_pas.planing.views import production_order_made_history_grouped_view

urlpatterns = [

    path('Production_order_made_history_grouped_view/Fetch/', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Fetch),
    path('Production_order_made_history_grouped_view/Add', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Add),
    path('Production_order_made_history_grouped_view/Update', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Update),
    path('Production_order_made_history_grouped_view/Remove', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Remove),
    path('Production_order_made_history_grouped_view/Lookup/', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Lookup),
    path('Production_order_made_history_grouped_view/Info/', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Info),
    path('Production_order_made_history_grouped_view/Copy', production_order_made_history_grouped_view.Production_order_made_history_grouped_view_Copy),

]
