from django.urls import path
from . import views

urlpatterns = [
    path('', views.committees, name="committees"),
    path('social/', views.social, name="social"),
    path('media/', views.media, name="media"),
    path('cultural/', views.cultural, name="cultural"),
    path('scientific/', views.scientific, name="scientific"),
    path('sports/', views.sports, name="sports"),
    path('volunteer/', views.volunteer, name="volunteer"),
    path('toggle_committee/<int:committee_id>/', views.toggle_committee, name='toggle_committee'),
]
