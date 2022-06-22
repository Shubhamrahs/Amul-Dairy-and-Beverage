from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),

    #---------------------------------------Customer--------------------------------------------------------
    path('userHome/', views.userHome, name='userHome'),
    path('show_items/', views.show_items, name="show_items"),
    path('show_items/<slug:data>', views.show_items, name="show_itemsdata"),
    path('showCart/', views.show_cart, name='show_cart'),
    path('add_cart/<str:id>', views.cart, name='add_cart'),
    path('delete_item_in_cart/<str:id>', views.delete_item_in_cart, name='delete_item_in_cart'),
    path('search', views.search, name='search'),

    #-------------------------------------------Owner---------------------------------------------------------
    path('ownerhome/', views.ownerHome, name='ownerHome'),
    path('show_items_owner/', views.show_items_owner, name="show_items_owner"),
    path('show_items_owner/<slug:data>',
         views.show_items_owner, name="show_items_ownerdata"),
    path('add_item_owner/', views.add_item_owner, name="add_item_owner"),
    path('update_item_owner/<str:id>', views.update_item_owner, name='update_item_owner'),
    path('delete_items_owner/<str:id>', views.delete_items_owner, name='delete_items_owner'),
    path('add_employee/', views.add_employee, name="add_employee"),
    path('show_employee/', views.show_employee, name="show_employee"),
    path('delete_employee/<str:id>', views.delete_employee, name='delete_employee'),

    #-------------------------------------------Employee--------------------------------------------------------------
    path('employeeHome/', views.empHome, name='employeeHome'),
    path('show_items_employee/', views.show_items_employee, name="show_items_employee"),
    path('show_items_employee/<slug:data>',
         views.show_items_employee, name="show_items_employeedata"),
    path('add_item_employee/', views.add_item_employee, name="add_item_employee"),
    path('delete_items_employee/<str:id>', views.delete_items_employee, name='delete_items_employee'),
    path('update_item_employee/<str:id>', views.update_item_employee, name='update_item_employee'),
    
]
