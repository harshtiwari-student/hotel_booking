from django.urls import path
from . import views
from app.views import RoomRegister,RoomList,RoomDelete,RoomUpdate

urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path(
        "request_password_reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),  
    path("reset_password/<uname>/",views.reset_password,name="reset_password"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("aboutus/",views.aboutus,name="aboutus"),
    path("contact/",views.contact,name="contact"),
    path("searchproduct/",views.searchproduct,name="searchproduct"),
    path("home/", views.home, name="home"),
    path("bookroom/<roomid>/", views.bookroom, name="bookroom"),
    path("final_payment/", views.final_payment, name="final_payment"),
    path('RoomRegister/',RoomRegister.as_view(),name="RoomRegister"),
    path('RoomList/',RoomList.as_view(),name="RoomList"),
    path('RoomDelete/<int:pk>',RoomDelete.as_view(),name="RoomDelete"),
    path('RoomUpdate/<int:pk>',RoomUpdate.as_view(),name="RoomUpdate")
]