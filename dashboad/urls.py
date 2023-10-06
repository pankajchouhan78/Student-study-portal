from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('notes/',notes,name="notes"),
    path('delete_notes/<int:pk>/',delete_notes,name="delete_notes"),
    path('detail_notes/<int:pk>/',detail_notes,name="detail_notes"),

    path('homework/',homework,name="homework"),
    path('update_homework/<int:pk>/',update_homework,name="update_homework"),
    path('delete_homework/<int:pk>/',delete_homework,name="delete_homework"),

    
    path('youtube/',youtube,name="youtube"),
    path('todo/',todo,name="todo"),
    path('update_todo/<int:pk>/',update_todo,name="update_todo"),
    path('delete_todo/<int:pk>/',delete_todo,name="delete_todo"),

    path('book/',book,name="book"),
    path('dictionary/',dictionary,name="dictionary"),
    path('wiki/',wiki,name="wiki"),
]
