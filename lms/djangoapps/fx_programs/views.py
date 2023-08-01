from common.djangoapps.edxmako.shortcuts import render_to_response
from django.http import HttpResponseServerError

from cms.djangoapps.fx_programs.models import FxPrograms


def index(request):
    try:
        programs = FxPrograms.objects.all()

        context = {
            'status': '200',
            'programs': programs
        }

        print("..FUNiX Custom ..", context)
        return render_to_response('programs_list.html', context)
    except (ValueError, AttributeError, TypeError) as e:
        # Bắt lỗi nếu có lỗi định dạng, thuộc tính không tồn tại hoặc giá trị không hợp lệ
        return HttpResponseServerError('Error occurred while processing the data.', str(e))
