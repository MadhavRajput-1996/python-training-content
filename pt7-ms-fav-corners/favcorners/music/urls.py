from django.urls import path
from . import views

urlpatterns = [
    path('add-category/', views.add_category, name='add_category'),
     path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('search/', views.search_song, name='search_song'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('most-viewed/', views.most_viewed_songs, name='most_viewed_songs'),
    path('add_song_to_category/', views.add_song_to_category, name='add_song_to_category'),
    path('delete_song/<int:song_id>/', views.delete_song, name='delete_song'),
]
