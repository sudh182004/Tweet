from django.contrib import admin
from django.urls import path
from App import views
from .views import Tweetcreate,Tweetedit,like,comment,dashboard
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home,name='home'),
    path("login/",views.Login,name="login"),
    path("logout/",views.Logout, name="logout"),
    path("signin/",views.Signin, name="signin"),
    path("create/", Tweetcreate, name="create"),
    path("edit/<int:id>/", Tweetedit, name="edit"),
    path("like/<int:id>/", like, name="like"),
    path("dashboard/", dashboard, name="dashboard"),
    path("comment/<int:id>/", comment, name="comment"),
]
