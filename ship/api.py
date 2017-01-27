# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from assessment.auth import TokenAuthSupportQueryString
from .injection_setup import logic
from .serializers import ShipSerializer


class ShipViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    authentication_classes = (TokenAuthSupportQueryString,)
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = ShipSerializer
    default_limit = 20

    def list(self, request):  # pylint: disable=unused-argument
        ships = self.get_queryset()

        page = self.paginate_queryset(ships)
        return self.get_paginated_response(page)

    def get_queryset(self):
        user = self.request.user
        user_ids = [user.id] + self.request.query_params.getlist('user_id')

        query_kwargs = {
            'user_ids': user_ids,
            'id': self.request.query_params.get('id'),
            'ids': self.request.query_params.getlist('ids'),
            'status': self.request.query_params.get('status'),
            'order_by': self.request.query_params.get('order_by'),
        }

        ships, __ = logic.get_ships(**query_kwargs)
        return ships

    def create(self, request):
        data = self.request.data.copy()

        # We want to override the user ID to be the authenticated user.
        data['user_id'] = self.request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        ships, __ = logic.get_ships(
            id=pk,
            user_ids=[request.user.id],
        )
        return Response(self.serializer_class(ships[0]).data)

    def update(self, request, pk=None):
        raise NotImplementedError(
            'Please implement ``ship.api:ShipViewSet.update``'
        )

    def destroy(self, request, pk=None):  # pylint: disable=unused-argument
        logic.delete_ship(id=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
