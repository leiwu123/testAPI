from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from django.urls import reverse
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


from rest_framework.parsers import JSONParser, FormParser

class ParserView(APIView):
    parser_classes = [JSONParser,FormParser]
    # can parser both Json and x-www-form-urlencoded data
    def post(self, request, *args, **kwargs):
        """
        Allow clients to sent JSON data
        a. content-type: application/json
        b. {'name':'alex', age:18}
        """

        print(request.data) ## getting parsered data, not using request.body with JSON data

        return HttpResponse('POST & Body')