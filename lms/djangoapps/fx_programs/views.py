from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core import serializers
from django.template import loader
from django.shortcuts import render

from common.djangoapps.edxmako.shortcuts import render_to_response
import numpy as np
import requests
import json

from .models import FxPrograms


def index(request):
    program_list = FxPrograms.objects.all()
    if not program_list:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized_programs = serializers.serialize('json', program_list)
    response_dict = {
        'status': 200,
        'programs': json.loads(serialized_programs),
    }

    return render(request, 'programs_list.html', response_dict)


class FxProgramsView(APIView):
    """
    **Use Case**

        Get subjects of programs.

    **Example Request**

        GET /api/fx_programs/v1/fx_programs

    **Response Values**
        {
            "status": 200,
            "programs": [
                "course_01_id":{
                    "image": {
                        "raw": "url example",
                        "small": "url example",
                        "large": "url example"
                    },
                    "name": "Name of course example",
                    "number": "ID of course example",
                    "blocks_url": "url example"
                },
                "course_02_id":{
                    "image": {
                        "raw": "url example",
                        "small": "url example",
                        "large": "url example"
                    },
                    "name": "Name of course 2 example",
                    "number": "ID of course 2 example",
                    "blocks_url": "url example"
                },
            ]
        }

    """
    def get(self, request):  # lint-amnesty, pylint: disable=missing-function-docstring
        try:
            program_list = FxPrograms.objects.all()
            serialized_programs = serializers.serialize('json', np.array(program_list))
            print("..FUNiX Custom ..", serialized_programs)
            response_dict = {
                'status': 200,
                'programs': eval(serialized_programs),
            }
            # response_dict[programs] = programs

            return Response(data=response_dict, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

