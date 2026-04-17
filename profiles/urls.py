from django.urls import path
from .views import ProfileListCreateView, ProfileDetailView, api_docs, health_check

urlpatterns = [
    path('', api_docs, name='api-docs'),
    path('health/', health_check, name='health'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list'),
    path('profiles/<str:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),
]