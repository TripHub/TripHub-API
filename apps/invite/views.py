from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import NotFound, PermissionDenied, \
    ValidationError

from .models import Invite
from .constants import PENDING
from .serializers import InviteSerializerSimple


class InviteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing, retrieving and accepting invites."""
    serializer_class = InviteSerializerSimple
    lookup_field = 'uid'

    def get_queryset(self):
        """Gets invites for trips user is involved in."""
        return Invite.objects.filter(
            Q(trip__owner=self.request.user) |
            Q(trip__members__in=[self.request.user]))

    @detail_route()
    def accept(self, request, uid=None):
        try:
            # get the invite
            invite = Invite.objects.filter(status=PENDING).get(uid=uid)
            # check the correct user is attempting to join
            if invite.email != self.request.user.email:
                raise PermissionDenied()
            # check the user isn't already involved in the trip
            is_user_owner = invite.trip.owner == self.request.user
            is_user_member = invite.trip.members.filter(
                pk=self.request.user.pk).exists()
            if is_user_owner or is_user_member:
                raise ValidationError(
                    'User is already a member or owner of the trip.')
            # update the invite status
            invite.trip.add_member(self.request.user)
            invite.accept()
            return Response(status=status.HTTP_200_OK)
        except Invite.DoesNotExist:
            raise NotFound()
