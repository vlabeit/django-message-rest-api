from message_app import serializers as message_serializers
from rest_framework import viewsets, filters
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from message_app import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class UserViewSet(viewsets.ModelViewSet):
    """Simple temporary User API, handle creating and updating users with Token authantication"""
    serializer_class = message_serializers.UserSerializer
    queryset = User.objects.all().order_by('id')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateUserPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields= ('username',)


class UserLoginApiView(ObtainAuthToken):
    """Create User auth toekn API"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

