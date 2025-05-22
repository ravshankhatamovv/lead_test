from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Lead
from .serializers import LeadSerializer, LeadStatusUpdateSerializer
from apps.account.permissions import (
    OnlyProspectCanPermission,
    OnlyAttornyCanPermission
)


class LeadViewSet(viewsets.ModelViewSet):
    """Lead endpoints"""
    queryset = Lead.objects.all()
    queryset = Lead.objects.all()

    def get_permissions(self):
        if self.action == 'update_status':
            permission_classes = [OnlyAttornyCanPermission, IsAuthenticated]
        else:
            permission_classes = [OnlyProspectCanPermission, IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "update_status":
            return LeadStatusUpdateSerializer
        return LeadSerializer

    def get_serializer_class(self):
        if self.action == "update_status":
            return LeadStatusUpdateSerializer
        return LeadSerializer


    @action(detail=True, methods=["patch"], url_path="update-status")
    def update_status(self, request, pk=None):
        lead = self.get_object()
        serializer = self.get_serializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Status updated successfully",
                "status": serializer.data["status"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)