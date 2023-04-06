from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('axtar/',views.axtar,name='axtar'),
    path("xeber/",views.xeber, name="xeber"),
    path("addnews/",views.addnews, name="addnews"),
    path("categori/<int:id>",views.categori, name="categori"),
    path("delete/",views.delete, name="delete"),
    path("contact/",views.contact, name="contact"),
    path("contact/addcontact/",views.addcontact, name="addcontact"),
    path("about/",views.about, name="about"),
    path("singlepage/<int:id>",views.singlepage, name="singlepage"),
    path('myapi/' , views.NewsdataView.as_view()),

    # path("page/addpage/",views.addpage, name="addpage")
  
]