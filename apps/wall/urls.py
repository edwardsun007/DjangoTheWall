from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index), ### home page
    url(r'^login$',views.login, name="login"),
    url(r'^register$',views.register, name="register"),
    url(r'^wall$',views.renderWall,name="renderWall"),
    url(r'^post_msg$',views.post_msg,name="post_msg"),
    url(r'^post_cmt$',views.post_cmt,name="post_cmt"),
    url(r'^del_msg/(?P<number>\d+)$',views.del_msg,name="del_msg"),
    url(r'^del_cmt/(?P<number>\d+)$',views.del_cmt,name="del_cmt"),
    url(r'^logout$',views.logOut,name="logOut")
]