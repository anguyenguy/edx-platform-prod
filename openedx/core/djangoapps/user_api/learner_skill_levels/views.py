from collections import defaultdict

from django.contrib.auth.models import User  # lint-amnesty, pylint: disable=imported-auth-user
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser

from .api import get_learner_skill_levels
from .utils import get_top_skill_categories_for_job, get_job_holder_usernames


class LearnerSkillLevelsView(APIView):
    """
        **Use Cases**

            Returns top 5 job categories along with current's user and average score for the given job id.

        **Request format**

            GET /api/user/v1/skill_level/{job_id}/

        **Response Values for GET**

            If the specified job_id doesn't exist, an HTTP
            404 "Not Found" response is returned.

            If a logged in user makes a request with an existing job, an HTTP 200
            "OK" response is returned that contains a JSON string.

        **Example Request**

            GET /api/user/v1/skill_level/1/

        **Example Response**

            {
                "job": "Digital Product Manager",
                "skill_categories": [
                    {
                        "name": "Information Technology",
                        "id": 1,
                        "user_score": 0.4,
                        "edx_average_score": 0.7,
                        "skills_subcategories": [
                            {
                                "id": 1,
                                "name": "Databases",
                                "skills": [
                                    {"id": 2, "name": "Query Languages", "score": 1},
                                    {"id": 3, "name": "MongoDB", "score": 3},
                                ]
                            },
                            {
                                "id": 2,
                                "name": "IT Management",
                                "skills": [
                                    {"id": 1, "name": "Technology Roadmap", "score": 2},
                                ]
                            },
                            // here remaining job related skills subcategories
                        ]
                    },

                    // Here more 4 skill categories
                ]
            }
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
        # get top categories for the given job
        response = get_top_skill_categories_for_job(job_id)

        job_holder_usernames = get_job_holder_usernames(job_id)
        users = User.objects.filter(username__in=job_holder_usernames['usernames'])

        # Save all the user scores against every category to calculate average score
        users_category_score_map = defaultdict(list)

        # calculate average scores for each category
        for user in users:
            get_learner_skill_levels(
                user=user,
                top_categories=response,
                user_score_mapping=users_category_score_map,
                calculate_avg=True
            )

        # finally calculate score for the current user
        get_learner_skill_levels(
            user=request.user,
            top_categories=response,
            user_score_mapping=users_category_score_map,
        )
        return Response(response)
