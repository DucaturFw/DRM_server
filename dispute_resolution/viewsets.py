from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from url_filter.integrations.drf import DjangoFilterBackend

from dispute_resolution.models import User, ContractCase, ContractStage, \
    NotifyEvent, UserInfo
from dispute_resolution.permissions import CasePermission, \
    NotificationPermission, StagePermission, UserInfoPermission, UserPermission
from dispute_resolution.serializers import UserSerializer, \
    ContractCaseSerializer, ContractStageSerializer, NotifyEventSerializer, \
    UserInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', 'family_name', 'email', 'judge']

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (UserPermission,)

    @action(methods=['get'], detail=True)
    def contracts(self, request, pk=None):
        user = self.get_object()
        return Response([ContractCaseSerializer(contract).data
                         for contract in user.contracts.all()])

    @action(methods=['get'], detail=False)
    def self(self, request):
        if request.user.is_authenticated:
            user = UserSerializer(self.request.user)
            return Response({
                'self': user.data,
                'events': [
                    NotifyEventSerializer(event).data
                    for event in NotifyEvent.objects.filter(
                        seen=False,
                        user_to__in=[self.request.user]
                    ).all()
                ]
            })
        else:
            return Response({'errors': {'auth': 'You are not authorized'}},
                            status=401)


class ContractCaseViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, CasePermission)

    ordering_fields = ('id', 'finished', 'party')
    ordering = ('finished',)

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['party', 'files', 'finished']

    queryset = ContractCase.objects.all()
    serializer_class = ContractCaseSerializer


class ContractStageViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, StagePermission)

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['owner', 'dispute_starter']

    queryset = ContractStage.objects.all()
    serializer_class = ContractStageSerializer


class NotifyEventViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, NotificationPermission)

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['user_to', 'user_by', 'contract', 'stage']

    serializer_class = NotifyEventSerializer

    def get_queryset(self):
        return NotifyEvent.objects.filter(user_to=self.request.user).all()


class UserInfoViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, UserInfoPermission)

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['eth_address', 'organization_name', 'tax_num',
                     'payment_num', 'user', 'files']

    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
