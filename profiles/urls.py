from django.urls import path
from .views import ProfileListCreateView, ProfileDetailView, api_docs

urlpatterns = [
    path('', api_docs, name='api-docs'),
    path('profiles/', ProfileListCreateView.as_view(), name='profile-list'),
    path('profiles/<str:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),
]