from django.conf.urls import url, include
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'xxxxx', views.View1View)
router.register(r'rt', views.View1View)

urlpatterns = [
    # url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view(), name='user'),
    # url(r'^(?P<version>[v1|v2]+)/django/$', views.DjangoView.as_view(), name='django'),
    # url(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view(), name='parser'),
    # url(r'^(?P<version>[v1|v2]+)/roles/$', views.RolesView.as_view()),
    # url(r'^(?P<version>[v1|v2]+)/userinfo/$', views.UserInfoView.as_view()),
    # url(r'^(?P<version>[v1|v2]+)/group/(?P<xxx>\d+)$', views.GroupView.as_view(), name='gp'),
    # url(r'^(?P<version>[v1|v2]+)/usergroup/$', views.UserGroupView.as_view()),
    # url(r'^(?P<version>[v1|v2]+)/pager1/$', views.Pager1View.as_view()),
    # url(r'^(?P<version>[v1|v2]+)/v1/$', views.View1View.as_view({'get':'list', 'post':'create'})),
    # url(r'^(?P<version>[v1|v2]+)/v1/(?P<pk>\d+)/$', views.View1View.as_view({'get':'retrieve', 'delete':'destroy', 'put':'update', 'patch':'partial_update'})),
    
    url(r'^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view(), name='uuu'),

    url(r'^(?P<version>[v1|v2]+)/', include(router.urls)),
]