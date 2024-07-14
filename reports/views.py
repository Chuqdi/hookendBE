from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from blocks.models import Block
from reports.models import Report
from users.models import User
from users.serializers import SignUpSerializer
from utils.helpers import generateAPIResponse



class ReportUserView(APIView):
    def patch(self, request, *args, **kwargs):
        reported_by = request.user
        reporting_id = request.data.get("reporting_id")
        reason = request.data.get("reason")
        blocking = request.data.get("blocking")

        try:
            reporting = User.objects.get(id=reporting_id)
        except User.DoesNotExist as e:
            return generateAPIResponse({}, "User not found", status.HTTP_400_BAD_REQUEST)
        report = Report.objects.create(
            reported_by = reported_by,
            reporting = reporting,
            reason = reason
        )

        if blocking:
            block = Block.objects.get_or_create(
            blocking=reporting,
            blocked_by=reported_by,
            reason=reason,
        )
        
        user  = SignUpSerializer(
            reported_by,
        )

        return generateAPIResponse(user.data, "User reported successfully", status.HTTP_201_CREATED)