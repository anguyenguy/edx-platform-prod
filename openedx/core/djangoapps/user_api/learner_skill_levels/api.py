"""
APIs for learner skill levels.
"""
from copy import deepcopy

from lms.djangoapps.grades.models import PersistentCourseGrade  # lint-amnesty, pylint: disable=unused-import
from openedx.core.djangoapps.catalog.utils import get_course_data
from .utils import get_top_skill_categories_for_job

LEVEL_TYPE_SCORE_MAPPING = {
    'INTRODUCTORY': 1,
    'INTERMEDIATE': 2,
    'ADVANCED': 3
}


def get_learner_skill_levels(user, job_id):
    """
    Retrieves course run details for a given course run key.

    Params:
        course_key (CourseKey): The identifier for the course.
        fields_list (List, string): A list of fields (as strings) of values we want returned.
    Returns:
        dict containing response from the Discovery API that includes the fields specified in `fields_list`
    """
    import pdb;pdb.set_trace()
    response = get_top_skill_categories_for_job(job_id)

    # get course_run_ids of all courses the user has passed
    """
    course_run_ids = list(
        PersistentCourseGrade.objects.filter(
            user_id=user.id
        ).exclude(passed_timestamp__isnull=True).values_list('course_id', flat=True)
    )

    # generate user-skill-score mapping
    learner_skill_score = {}
    for course_run_id in course_run_ids:
        course_data = get_course_data(course_run_id, ['skill_names', 'level_type'])
        skill_names = course_data['skill_names']
        score = LEVEL_TYPE_SCORE_MAPPING[course_data['level_type']]
        for skill in skill_names:
            if skill in learner_skill_score:
                # assign larger score if skill repeated in 2 courses
                learner_skill_score[skill] = max(score, learner_skill_score[skill])
            else:
                learner_skill_score.update({skill: score})
    """
    learner_skill_score = {'DEF': 3, 'Python': 1}
    # assign scores b/w 1-3 based on level type
    response_copy = deepcopy(response)
    skill_categories = response['skill_categories']
    skill_categories_copy = response_copy['skill_categories']

    for skill_category, skill_category_copy in zip(skill_categories, skill_categories_copy):
        category_skills = skill_category['skills']
        category_skills_copy = skill_category_copy['skills']
        if category_skills:
            for index, skill in enumerate(category_skills):
                if skill['name'] in learner_skill_score:
                    category_skills_copy[index]['score'] = learner_skill_score[skill['name']]
                else:
                    category_skills_copy.remove(skill)

        # iterate over skill sub-categories and their skills
        sub_categories = skill_category['skills_subcategories']
        sub_categories_copy = skill_category_copy['skills_subcategories']
        if sub_categories:
            for sub_category, sub_category_copy in zip(sub_categories, sub_categories_copy):
                subcategory_skills = sub_category['skills']
                subcategory_skills_copy = sub_category_copy['skills']
                for index, skill in enumerate(subcategory_skills):
                    if skill['name'] in learner_skill_score:
                        subcategory_skills_copy[index]['score'] = learner_skill_score[skill['name']]
                    else:
                        subcategory_skills_copy.remove(skill)
    return [response, response_copy]

