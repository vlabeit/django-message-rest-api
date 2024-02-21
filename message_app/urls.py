from django.urls import path, include
from rest_framework.routers import DefaultRouter
from message_app.views.message import MessageViewSet
from message_app.views.users import UserLoginApiView, UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('message', MessageViewSet, basename="message")

urlpatterns = [
    path('auth/login/', UserLoginApiView.as_view()),
    path('', include(router.urls))
]
