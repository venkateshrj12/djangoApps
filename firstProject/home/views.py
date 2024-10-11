from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST', 'PATCH'])
def courses(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'django']
    }
    if request.method == 'GET':
        response = {'message': 'You hit GET request',
                    'courses': courses }
    elif request.method == 'POST':
        response = {'message': 'You hit POST request',
                    'courses': courses }
    elif request.method == 'PATCH':
        response = {'message': 'You hit Patch request',
                    'courses': courses }

    return Response(response)