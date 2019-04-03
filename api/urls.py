from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view(), name='user'),
    url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='django'),
    url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view(), name='parser'),
    url(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/group/(?P<xxx>\d+)$', views.GroupView.as_view(), name='gp'),
    url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view()),
    url(r'^(?P<version>[v1|v2]+)/pager1/$', views.Pager1View.as_view()),
]