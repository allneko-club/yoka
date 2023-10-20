from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('thread/', views.ThreadListView.as_view(), name='thread_list'),
    path('thread/category/<slug:slug>/', views.CategoryThreadListView.as_view(), name='category_threads'),
    path('thread/<uuid:pk>/', views.ReplyListInThreadView.as_view(), name='thread_detail'),
    path('thread/create/', views.CreateThreadView.as_view(), name='create_thread'),
    path('thread/<uuid:pk>/update/', views.UpdateThreadView.as_view(), name='update_thread'),
    path('search/thread/', views.SearchThreadView.as_view(), name='search_thread'),
]
