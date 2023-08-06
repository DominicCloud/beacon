from django.urls import path
from primary import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('log-in', views.loginUser, name="login"),
    path('log-out', views.logoutUser, name="logout"),
    path('register', views.registerUser, name="register"),
    path('trending_events', views.trending_events, name="trending_events"),
    path('design_event', views.design, name="desginpage"),
    path('interested', views.interestedevents, name="interestedevents"),
]