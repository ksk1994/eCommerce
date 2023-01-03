from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("add_wish_list/<int:item_id>", views.add_wish_list, name="add_wish_list"),
    path("wishlists", views.wishlists, name="wishlists"),
    path("close/<int:itemid>", views.close, name="close"),
    path("add_comment/<int:itemid>", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("search", views.search, name="search")
]
