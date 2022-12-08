from django.db import transaction
from django.utils.translation import gettext as _
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
from ..errors import UserNotAuthorized, UserNotFound
from .api import get_learner_skill_levels


class LearnerSkillLevelsView(APIView):
    """
        **Use Cases**

            Get, create, update, or delete a specific user preference.

        **Example Requests**

            GET /api/user/v1/preferences/{username}/{preference_key}

        **Response Values for GET**

            If the specified username or preference does not exist, an HTTP
            404 "Not Found" response is returned.

            If a user without "is_staff" access requests preferences for a
            different user, a 404 error is returned.

            If the user makes the request for her own account, or makes a
            request for another account and has "is_staff" access, an HTTP 200
            "OK" response is returned that contains a JSON string.

        **Example Requests**

            GET /api/user/v1/preferences/{username}/{preference_key}
    """
    authentication_classes = (
        JwtAuthentication,
        BearerAuthenticationAllowInactiveUser,
        SessionAuthenticationAllowInactiveUser
    )
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, job_id):
        """
        GET /api/user/v1/skill_level/{job_id}/
        """
        try:
            learner_skill_levels = get_learner_skill_levels(user=request.user, job_id=job_id)
        except UserNotFound:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except UserNotAuthorized:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(learner_skill_levels)
