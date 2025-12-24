from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostListView, PostDetailView, PostCreateView, MyPostsListView, EventCreateView,EventDetailView
from django.views.decorators.cache import never_cache


urlpatterns = [
    path("", views.index, name="index"),
    
    path("login/", auth_views.LoginView.as_view(template_name="saaf/login.html",), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    # .as_view() converts a class-based view into a function that Django’s URL dispatcher can use.
    # This allows us to use class-based views in our URL patterns just like function-based views.
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),


    path("posts/", never_cache(PostListView.as_view()), name="post-list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path('my-posts/', never_cache(MyPostsListView.as_view()), name='my-posts'),
    path('user/<str:username>/', views.user_profile, name='user-profile'),
    path("posts/<int:pk>/delete/", views.delete_post, name="post-delete"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="comment-delete"),

    path('events/<int:post_id>/new/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete-event'),
    path('events/<int:pk>/join/', views.join_event, name='event-join'),
    path('events/<int:pk>/cancel/', views.cancel_event, name='event-cancel'),
    path('events/nearby/', views.nearby_events, name='nearby-events'),
    path('events/search/', views.search_events_by_location, name='search-events-location'),

    path("enhance_story/", views.enhance_story, name="enhance_story"),

]

