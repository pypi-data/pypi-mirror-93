from django.urls import path

from kaf_pas.ckk.views import item

urlpatterns = [

    path('Item/Fetch/', item.Item_Fetch),
    path('Item/Add', item.Item_Add),
    path('Item/Update', item.Item_Update),
    path('Item/Replace', item.Item_Replace),
    path('Item/Remove', item.Item_Remove),
    path('Item/Lookup/', item.Item_Lookup),
    path('Item/Info/', item.Item_Info),
    path('Item/CheckRecursives/', item.Item_CheckRecursives),
    path('Item/GetQtyChilds/', item.GetQtyChilds),
    path('Item/GetGrouping/', item.GetGrouping),
]
