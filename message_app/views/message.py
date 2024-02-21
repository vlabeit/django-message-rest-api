from rest_framework.response import Response
from rest_framework import status
from message_app import serializers as message_serializers
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework. authentication import TokenAuthentication
from message_app import permissions
from rest_framework import filters
from message_app.models import Message
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class MessageViewSet(viewsets.ModelViewSet):
    """
    This is a ViewSet for handling messages in a Django application.

    Attributes:
        serializer_class: The serializer class used for this viewset is `message_serializers.MessageSerializer`.
        queryset: The default queryset is all Message objects.
        authentication_classes: Uses TokenAuthentication for authenticating users.
        permission_classes: Uses `permissions.ViewMessagePermission` for handling permissions.
        filter_backends: Uses Django's SearchFilter for filtering results.
        search_fields: The fields that can be searched are 'message_from', 'message_to', and 'message_title'.
    """
    serializer_class = message_serializers.MessageSerializer
    queryset = Message.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ViewMessagePermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields= ('message_from', 'message_to', 'message_title',)

    def get_queryset(self):
        # Restrict the queryset to show only the data of the requesting user
        if self.action == 'list' and self.request.user.is_authenticated:
            return Message.objects.filter(Q(message_from=self.request.user) | Q(message_to=self.request.user))
        return Message.objects.all()

    def create(self, request, *args, **kwargs):
        """Create message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cleaned_data = serializer.validated_data

        try:
            user_to = User.objects.get(username=cleaned_data['message_to'])
        except User.DoesNotExist:
            return Response({"message_to": ["Invalid username or user does not exist."]}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(message_to=user_to, message_from=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """Get all of the loged ub user sent and received messages"""
        response = super().retrieve(request, *args, **kwargs)
        instance = self.get_object()

        if not instance.is_viewed:
            instance.is_viewed = True
            instance.save()
        return response

    @action(detail=False, methods=['get'])
    def get_user_received_messages(self, request, user_pk=None):
        """Retrieve all received messages for the loged in user"""
        user_messages = self.get_queryset().filter(message_to=request.user)
        serializer = self.get_serializer(user_messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_unread_messages(self, request, pk=None):
        """Get all loged in user unread messages"""
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        unread_messages = self.get_queryset().filter(message_to=request.user, is_viewed=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)


   # staff api
    def _check_staff_permission(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Authentication required.")
        if not request.user.is_staff:
            raise PermissionDenied("Permission denied. Staff access required.")


    @action(detail=False, methods=['get'], url_path='get_user_messages/(?P<user_pk>[^/.]+)')
    def get_user_messages(self, request, user_pk=None):
        """Staff only - Retrieve all messages for the specified user"""
        try:
            self._check_staff_permission(request)
            user_messages = self.get_queryset().filter(
                Q(message_from=user_pk) | Q(message_to=user_pk)
            )
            serializer = self.get_serializer(user_messages, many=True)
            return Response(serializer.data)
        except AuthenticationFailed as auth_error:
            return Response({"detail": str(auth_error)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as perm_error:
            return Response({"detail": str(perm_error)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_name="get_unread_message_by_user")
    def get_unread_messages_by_user(self, request, pk=None):
        """Staff only - Retrieve all unread messages for the specified user"""
        try:
            self._check_staff_permission(request)
            username = request.query_params.get('user_id')
            unread_messages = self.get_queryset().filter(message_to=username, is_viewed=False)
            serializer_data = [self.get_serializer(message).data for message in unread_messages]

            return Response(serializer_data)
        except AuthenticationFailed as auth_error:
            return Response({"detail": str(auth_error)}, status=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied as perm_error:
            return Response({"detail": str(perm_error)}, status=status.HTTP_403_FORBIDDEN)

