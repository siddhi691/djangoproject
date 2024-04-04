from django.urls import path
from django.contrib import admin
from dogsapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.Userlogin),
    path('logout',views.Userlogout),
    path('register',views.register),
    path('home',views.home),
    path('pdetails/<pid>',views.product_details),
    path('catfilter/<cv>',views.catfilter),
     path('register',views.register),
    path("addtocart/<pid>",views.addtocart),
    path("viewcart",views.viewcart),
     path("placeorder",views.placeorder),
     path("updateqty/<qv>/<cid>",views.updateqty),
     path("makepayment",views.makepayment),
     path("remove/<cid>",views.remove),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)