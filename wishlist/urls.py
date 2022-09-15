from django.urls import path
from wishlist.views import show_wishlist, return_xml, return_json,return_json_based_on_id, return_xml_based_on_id

app_name = 'wishlist'

urlpatterns = [
    path('', show_wishlist, name='show_wishlist'),
    path('xml/', return_xml, name='return_xml'),
    path('json/', return_json, name='return_json'),
    path('json/<int:id>', return_json_based_on_id, name='return_json_based_on_id'),
    path('xml/<int:id>', return_xml_based_on_id, name='return_xml_based_on_id'),
]