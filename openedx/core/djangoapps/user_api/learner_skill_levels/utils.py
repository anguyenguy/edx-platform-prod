from openedx.core.djangoapps.catalog.utils import (
    get_catalog_api_client,
    check_catalog_integration_and_get_user,
    get_catalog_api_base_url,

)
from openedx.core.lib.edx_api_utils import get_api_data


def get_top_skill_categories_for_job(job_id):
    """
        Retrieve top categories for the job with the given job_id.

        Arguments:
            job_id (int): id of the job about which we are retrieving information.

        Returns:
            dict with top 5 categories of specified job.
    """
    user, catalog_integration = check_catalog_integration_and_get_user(error_message_field='Skill Categories')
    if user:
        api_client = get_catalog_api_client(user)
        root_url = get_catalog_api_base_url()
        base_api_url = root_url.split('/api', 1)[0]
        resource = '/taxonomy/api/v1/job-top-subcategories'
        cache_key = f'{catalog_integration.CACHE_KEY}.job-categories.{job_id}'
        data = get_api_data(
            catalog_integration,
            resource=resource,
            resource_id=job_id,
            api_client=api_client,
            base_api_url=base_api_url,
            cache_key=cache_key if catalog_integration.is_cache_enabled else None,
        )
        if data:
            return data


def get_job_holder_usernames(job_id):
    """
        Retrieve usernames of users who have the same job as given job_id.

        Arguments:
            job_id (int): id of the job for which we are retrieving usernames.

        Returns:
            list with oldest 100 users' usernames that exist in our system.
    """
    user, catalog_integration = check_catalog_integration_and_get_user(error_message_field='Job Holder Usernames')
    if user:
        api_client = get_catalog_api_client(user)
        root_url = get_catalog_api_base_url()
        base_api_url = root_url.split('/api', 1)[0]
        resource = '/taxonomy/api/v1/job-holder-usernames'
        cache_key = f'{catalog_integration.CACHE_KEY}.job-holder-usernames.{job_id}'
        data = get_api_data(
            catalog_integration,
            resource=resource,
            resource_id=job_id,
            api_client=api_client,
            base_api_url=base_api_url,
            cache_key=cache_key if catalog_integration.is_cache_enabled else None,
        )
        if data:
            return data
