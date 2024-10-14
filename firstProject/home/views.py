from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST', 'PATCH'])
def courses(request):
    courses = {
        'course_name': 'Python',
        'learn': ['flask', 'django']
    }
    if request.method == 'GET':
        name = request.GET.get('name')
        response = {'message': 'You hit GET request',
                    'courses': courses,
                     'name': name }
    elif request.method == 'POST':
        data = request.data
        response = {'message': 'You hit POST request',
                    'data': data }
    elif request.method == 'PATCH':
        data = request.data
        response = {'message': 'You hit Patch request',
                    'data': data }

    return Response(response)