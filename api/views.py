from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.urls import reverse
from api import models
import json
# from rest_framework.request import Request
# from rest_framework.versioning import BaseVersioning
# from rest_framework.versioning import QueryParameterVersioning
# from rest_framework.versioning import URLPathVersioning

# class ParamVersion(BaseVersioning):
#     def determine_version(self, request, *args, **kwargs):
#         version = request.query_params.get('version')
#         return version

class UsersView(APIView):

    # versioning_class = QueryParameterVersioning
    # versioning_class = URLPathVersioning
    def get(self, request, *args, **kwargs):
        # version = request._request.GET.get('version')
        # print(version)
        # version = request.query_params.get('version')
        # print(version)
        print(request.version)
        print(request.versioning_scheme)
        print(request.versioning_scheme.reverse(viewname='user', request=request)) # return url with viewname from below 
        # url(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view(), name='user'),
        print(reverse(viewname='user', kwargs={'version':1}))

        return HttpResponse('用户列表')


class DjangoView(APIView):

    def post(self, request, *args, **kwargs):
        print(type(request._request))
        # from django.core.handlers.wsgi import WSGIRequest
        return HttpResponse('POST & Body')


# from rest_framework.parsers import JSONParser, FormParser

class ParserView(APIView):
    # parser_classes = [JSONParser,FormParser]
    # can parser both Json and x-www-form-urlencoded data
    def post(self, request, *args, **kwargs):
        """
        Allow clients to sent JSON data
        a. content-type: application/json
        b. {'name':'alex', age:18}
        """

        print(request.data) ## getting parsered data, not using request.body with restframework Parser classes

        return HttpResponse('POST & Body')


from rest_framework import serializers

class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()  ## same as below
    title = serializers.CharField()  ## 'title' variable name needs to match the database


class RolesView(APIView):
    def get(self, request, *args, **kwargs):

        # roles = models.Role.objects.all().values('id', 'title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)
        # # ret = json.dumps(roles) ## cannot directly use roles as its django querysets

        # roles = models.Role.objects.all()
        # ser = RolesSerializer(instance=roles, many=True)
        # # ser.data
        # ret = json.dumps(ser.data, ensure_ascii=False)

        # to return only the first item
        roles = models.Role.objects.all().first() 
        ser = RolesSerializer(instance=roles, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)

        return HttpResponse(ret)

# class UserInfoSerializer(serializers.Serializer):

#     # user_type = serializers.IntegerField()
#     # xxx = serializers.CharField(source="user_type")
#     """
#     returned values from above
#     [{"xxx": "1", "username": "王冰", "password": "124"}, {"xxx": "1", "username": "刘莫", "password": "124"}, {"xxx": "2", "username": "张坤", "password": "124"}, {"xxx": "3", "username": "陆华", "password": "124"}]
#     """
#     user_type = serializers.CharField(source="get_user_type_display")
#     """
#     [{"user_type": "普通用户", "username": "王冰", "password": "124"}, {"user_type": "普通用户", "username": "刘莫", "password": "124"}]
#     """
#     username = serializers.CharField()
#     password = serializers.CharField()
#     gp = serializers.CharField(source="group.title")
#     # rls = serializers.CharField(source="roles.all")
#     rls = serializers.SerializerMethodField()

#     def get_rls(self, row):  ## same can be applied to group and user_type
#         role_obj_list = row.roles.all()

#         ret = []
#         for item in role_obj_list:
#             ret.append({'id':item.id, 'title':item.title})
#         return ret

# class MyField(serializers.CharField):  ## rarely used
#     def to_representation(self, value):    
#         return "xxxx"

# class UserInfoSerializer(serializers.ModelSerializer):
#     oooo = serializers.CharField(source="get_user_type_display")
#     rls = serializers.SerializerMethodField()
#     gp = serializers.CharField(source="group.title")
#     x1 = MyField(source='username')

#     class Meta:
#         model = models.UserInfo
#         # fields = "__all__"
#         fields = ['id', 'username', 'password', 'oooo', 'rls', 'gp', 'x1']


#     def get_rls(self, row):  ## same can be applied to group and user_type
#         role_obj_list = row.roles.all()

#         ret = []
#         for item in role_obj_list:
#             ret.append({'id':item.id, 'title':item.title})
#         return ret

class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='xxx') 
    ## above provides a link rather than data, xxx (or normally use pk) corresponds to the xxx in urls.py for gp view

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        depth = 1  ## 1-10  but should be no more than 3 to 4 in use otherwise taking too much time retrieving data


class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):

        # roles = models.Role.objects.all().values('id', 'title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)
        # # ret = json.dumps(roles) ## cannot directly use roles as its django querysets

        # roles = models.Role.objects.all()
        # ser = RolesSerializer(instance=roles, many=True)
        # # ser.datasource="roles.all"
        # ret = json.dumps(ser.data, ensure_ascii=False)

        # to return only the first item
        roles = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=roles, many=True, context={'request': request})
        ## needs to add the context={'request': request} for the group hyperlink to work
        ret = json.dumps(ser.data, ensure_ascii=False)
        # print(ret)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"

class GroupView(APIView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('xxx')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)
