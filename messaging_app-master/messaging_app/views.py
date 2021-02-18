from django.shortcuts import render
from django.contrib.sessions.models import Session
from adduser.models import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.forms.models import model_to_dict
# Create your views here.


def home_view(request):
    sessions = Session.objects.filter()
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        if request.user.id != int(data.get('_auth_user_id', None)):
            uid_list.append(data.get('_auth_user_id', None))
    return render(request, 'messages.html', {'user': User.objects.get(username=request.user),
                                             'online_user': User.objects.filter(id__in=uid_list)})


@api_view(['GET', 'POST'])
def chat_user_details_view(request, id=None):
    if id is not None:
        json_user_data = model_to_dict(User.objects.get(id=id))
        json_user_data.pop('password')
        return JsonResponse(json_user_data, safe=False, status=200)


def chat(request):
    return render(request, 'chat.html')


def room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })
