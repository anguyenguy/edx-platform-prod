"""
APIs for learner skill levels.
"""
from lms.djangoapps.grades.models import PersistentCourseGrade  # lint-amnesty, pylint: disable=unused-import
from openedx.core.djangoapps.catalog.utils import get_course_data

from .constants import LEVEL_TYPE_SCORE_MAPPING


def _calculate_user_skill_score(all_skills):
    """
    Calculates user skill score to see where the user falls in a certain job category.
    """
    sum_of_skills = sum(all_skills.values())
    skills_count = len(all_skills)
    # sum of skills score in the category/ 3*no. of skills in category
    if skills_count:
        return round(sum_of_skills / (3 * skills_count), 1)
    return 0.0


def _generate_skill_score_mapping(course_run_ids):
    """
    Generates a skill to score mapping for all the skill user has learner so far in passed courses.
    """
    learner_skill_score = {}
    for course_run_id in course_run_ids:
        course_data = get_course_data(course_run_id, ['skill_names', 'level_type'])
        skill_names = course_data['skill_names']
        level_type = course_data['level_type'].capitalize()

        # if a level_type is None for a course, we should skip that course.
        score = LEVEL_TYPE_SCORE_MAPPING[level_type] if level_type else None
        if score:
            for skill in skill_names:
                if skill in learner_skill_score:
                    # assign scores b/w 1-3 based on level type
                    # assign the larger score if skill is repeated in 2 courses
                    learner_skill_score[skill] = max(score, learner_skill_score[skill])
                else:
                    learner_skill_score.update({skill: score})
    return learner_skill_score


def get_learner_skill_levels(user, top_categories, user_score_mapping, calculate_avg=False):
    """
    Evaluates learner's skill levels in the given job categories.

    Params:
        user (CourseKey): The identifier for the course.
        top_categories (List, string): A list of fields (as strings) of job categories and their skills.
        user_score_mapping (Dict, List): A dictionary of lists to save every user's score against each category.
        calculate_avg (Boolean): A flag to check if we are using this method to calculate avg or current user's score.
    Returns:
        None
    """
    # get course_run_ids of all courses the user has passed
    course_run_ids = list(
        PersistentCourseGrade.objects.filter(
            user_id=user.id
        ).exclude(passed_timestamp__isnull=True).values_list('course_id', flat=True)
    )

    # generates something like {'Python': 1, 'Technology Roadmap': 2}
    learner_skill_score = _generate_skill_score_mapping(course_run_ids)

    # assign score for each skill user has learned via any passed course
    for skill_category in top_categories['skill_categories']:
        category_skills = skill_category['skills']
        skills_with_scores = []
        if category_skills:
            # assign score only if the learner has learned that skill
            skills_with_scores = [
                dict(skill, **{'score': learner_skill_score[skill['name']]})
                for skill in category_skills
                if skill['name'] in learner_skill_score
            ]
            if not calculate_avg:
                # response should only be modified when we are calculating current users' levels
                skill_category['skills'] = skills_with_scores
        category_skills_scores = {item['name']: item['score'] for item in skills_with_scores}

        # iterate over sub-categories and their skills
        sub_categories = skill_category['skills_subcategories']
        if sub_categories:
            subcategories_skills_scores = {}
            for sub_category in sub_categories:
                subcategory_skills = sub_category['skills']
                if subcategory_skills:
                    skills_with_scores = [
                        dict(skill, **{'score': learner_skill_score[skill['name']]})
                        for skill in subcategory_skills
                        if skill['name'] in learner_skill_score
                    ]
                    if not calculate_avg:
                        sub_category['skills'] = skills_with_scores
                subcategory_skills_score = {item['name']: item['score'] for item in skills_with_scores}
                # append the new scores of current sub-category with previous sub-categories
                subcategories_skills_scores = {**subcategories_skills_scores, **subcategory_skills_score}

        # calculate user_score
        all_skills = {**category_skills_scores, **subcategories_skills_scores}
        user_score = _calculate_user_skill_score(all_skills)

        if calculate_avg:
            user_score_mapping[skill_category['name']].append(user_score)
        else:
            skill_category['user_score'] = user_score
            # calculate the sum of all user scores against the current job category in loop
            sum_score = sum(user_score_mapping[skill_category['name']], 0.0)
            average_score = sum_score/len(user_score_mapping[skill_category['name']])
            skill_category['edx_average_score'] = average_score

