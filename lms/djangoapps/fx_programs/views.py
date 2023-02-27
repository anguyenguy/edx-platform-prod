from common.djangoapps.edxmako.shortcuts import render_to_response
from django.http import HttpResponseServerError

from cms.djangoapps.fx_programs.models import FxPrograms


def index(request):
    try:
        programs = FxPrograms.objects.all()

        program_list = []

        for program in programs:
            metadata = program.metadata
            for course_id in program.id_course_list.split(","):
                if course_id:
                    course = metadata[course_id]
                    program_list.append({
                        'program_name': program.name,
                        "program_id": program.program_id,
                        'course_id': course['id'],
                        'course_name': course['display_name'],
                        'language': course['language'],
                        'course_image_url': course['course_image_url'],
                    })

        context = {
            'status': '200',
            'programs': program_list
        }

        print("..FUNiX Custom ..", context)
        return render_to_response('programs_list.html', context)
    except (ValueError, AttributeError, TypeError) as e:
        # Bắt lỗi nếu có lỗi định dạng, thuộc tính không tồn tại hoặc giá trị không hợp lệ
        return HttpResponseServerError('Error occurred while processing the data.', str(e))
