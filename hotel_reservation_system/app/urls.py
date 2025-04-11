from django.urls import path
from . import views
# from app.views import ProductRegister,ProductList,Productdelete,ProductUpdate

urlpatterns = [
    path("", views.index, name="index"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
]