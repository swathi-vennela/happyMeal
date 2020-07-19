from django.urls import path
# from .views import(
#         menu,
#         ItemListView,
#         ItemCreateView,
#         add_to_cart,
#         remove_from_cart,
#         remove_single_item_from_cart,
#         OrderSummaryView,
#         filterItems,
#         search,
#         add_review,
#         edit_review,
#         delete_review,
#         detail,
#     )
from .views import *
from . import views

app_name = 'core'

urlpatterns = [
    path('menu/', menu , name='menu'),
    path('filter/', filterItems, name='filter'),
    path('search/', search, name='search'),
    # path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product/<slug>', detail, name='product'),
    # path('item/new/', ItemCreateView.as_view(), name='product-create'),
    path('item/new/', create_item, name='product-create'),
    path('chef-list/',chef_list, name='chef-list'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/',add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/',remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/',remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('addreview/<slug>/', views.add_review, name='add_review'),
    path('edit_review/<slug>/<review_id>',views.edit_review, name='edit_review'),
    path('delete_review/<slug>/<review_id>',views.delete_review, name='delete_review'),
]