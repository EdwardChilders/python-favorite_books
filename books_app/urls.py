from django.urls import path
from . import views


urlpatterns = [
  # renders
    path('', views.index),
    path('books', views.books),
    path('books/<int:b_id>', views.view_book),
    
    # redirects
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('add_favorite/<int:b_id>', views.add_favorite),
    path('remove_favorite/<int:b_id>', views.remove_favorite),
    path('update_book/<int:b_id>', views.update_book),
    path('delete_book/<int:b_id>', views.delete_book),
]
