from openedx.core.djangoapps.catalog.utils import (
    get_catalog_api_client,
    check_catalog_integration_and_get_user,
    get_catalog_api_base_url,

)
from openedx.core.lib.edx_api_utils import get_api_data


def get_top_skill_categories_for_job(job_id):
    """
        Retrieve information about the course with the given course key.

        Arguments:
            course_key_str: key for the course about which we are retrieving information.

        Returns:
            dict with details about specified course.
        """
    user, catalog_integration = check_catalog_integration_and_get_user(error_message_field='Skill Categories')
    if user:
        api_client = get_catalog_api_client(user)
        base_api_url = get_catalog_api_base_url()
        root_url = base_api_url.split('/api', 1)[0]
        cache_key = f'{catalog_integration.CACHE_KEY}.skill-categories.{job_id}'
        data = get_api_data(
            catalog_integration,
            '/taxonomy/api/v1/job-top-subcategories',
            resource_id=job_id,
            api_client=api_client,
            base_api_url=root_url,
            cache_key=cache_key if catalog_integration.is_cache_enabled else None,
            long_term_cache=True,
            many=False,
        )
        if data:
            return data
