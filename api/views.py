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
    # pid = serializers.CharField(source='id')
    # pwd = serializers.CharField(source='password')

    class Meta:
        model = models.UserInfo
        fields = "__all__"
        # fields = ['pid', 'username', 'password', 'group', 'roles', 'pwd']
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

    def post(self, request, *args, **kwargs):
        print(request.data)



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



##########################################
class XXValidator(object):
    def __init__(self, base):
        # self.base = str(base)
        self.base = base

    # def __call__(self, value):
    #     if value != self.base:
    #         message = 'This field must be %s.' % self.base
    #         raise serializers.ValidationError(message)

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '标题必须以%s为开头' % self.base
            raise serializers.ValidationError(message)


    def set_context(self, serializer_field):
        pass

class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required':'标题不能为空'}, validators=[XXValidator('老男人')])   # put here the field you want to validate

    # def validate_title(self, value):
    #     from rest_framework import exceptions
    #     raise exceptions.ValidationError('看你不顺眼')
    #     return value

class UserGroupView(APIView):

    def post(self, request, *args, **kwargs):
        print(request.data)
        ## {'name': 'dft', 'title': 'dtf'}
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
            ## dtf
        else:
            print(ser.errors)
        
        return HttpResponse('提交数据')


from api.utils.serializers.pager import PagerSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

# class MyPageNumberPagination(PageNumberPagination):

#     page_size = 2
#     page_query_param = 'page'
#     page_size_query_param = 'size'
#     max_page_size = 18

# class MyPageNumberPagination(LimitOffsetPagination):

#     default_limit = 5
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#     max_limit = 15

class MyPageNumberPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 5
    ordering = 'id'  ## important .. must define the property used for retrieving the data

    page_size_query_param = 'size'
    max_page_size = 18

class Pager1View(APIView):

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()

        # pg = PageNumberPagination()
        # pg = MyPageNumberPagination()
        # pg = LimitOffsetPagination()
        # http://localhost:8000/api/v1/pager1/?offset=4&limit=5
        # pg = MyPageNumberPagination()
        # pg = CursorPagination()
        pg = MyPageNumberPagination()

        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # print(pager_roles)

        ser = PagerSerialiser(instance=pager_roles, many=True)
        # print(ser.data)
        # ret = json.dumps(ser.data, ensure_ascii=False)
        # return HttpResponse(ret)
        # return Response(ser.data)  
        return pg.get_paginated_response(ser.data)  


# from api.utils.serializers.pager import PagerSerialiser
# from rest_framework.generics import GenericAPIView
# class View1View(GenericAPIView):
#     queryset= models.Role.objects.all()
#     serializer_class = PagerSerialiser
#     pagination_class = PageNumberPagination

#     def get(self, request, *args, **kwargs):
#         roles = self.get_queryset()
#         print(roles)
#         pager_roles = self.paginate_queryset(roles)
#         print(pager_roles)
#         ser = self.get_serializer(instance=pager_roles, many=True)
#         return Response(ser.data)


# from api.utils.serializers.pager import PagerSerialiser
# from rest_framework.viewsets import GenericViewSet
# class View1View(GenericViewSet):
#     queryset= models.Role.objects.all()
#     serializer_class = PagerSerialiser
#     pagination_class = PageNumberPagination

#     def list(self, request, *args, **kwargs):
#         roles = self.get_queryset()
#         print(roles)
#         pager_roles = self.paginate_queryset(roles)
#         print(pager_roles)
#         ser = self.get_serializer(instance=pager_roles, many=True)
#         return Response(ser.data)


from api.utils.serializers.pager import PagerSerialiser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

# class View1View(ListModelMixin, CreateModelMixin, GenericViewSet):
#     queryset= models.Role.objects.all()
#     serializer_class = PagerSerialiser
#     pagination_class = PageNumberPagination

    # def list(self, request, *args, **kwargs):
    #     roles = self.get_queryset()
    #     print(roles)
    #     pager_roles = self.paginate_queryset(roles)
    #     print(pager_roles)
    #     ser = self.get_serializer(instance=pager_roles, many=True)
    #     return Response(ser.data)

class View1View(ModelViewSet):
    queryset= models.Role.objects.all()
    serializer_class = PagerSerialiser
    pagination_class = PageNumberPagination



######################################

class TestView(APIView):

    def get(self, request, *args, **kwargs):
        roles = models.Role.objects.all()
        
        # pg = CursorPagination()
        pg = MyPageNumberPagination()

        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # print(pager_roles)

        ser = PagerSerialiser(instance=pager_roles, many=True)
        # print(ser.data)
        # ret = json.dumps(ser.data, ensure_ascii=False)
        # return HttpResponse(ret)
        return Response(ser.data)  
        # return pg.get_paginated_response(ser.data)  