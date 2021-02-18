from rest_framework.decorators import api_view
from .models import *
from django.forms.models import model_to_dict
from rest_framework.response import Response
from .serializers import *


@api_view(['GET', ])
def our_team_view(request):
    our_team_obj = OurTeamSerializer(instance=OurTeam.objects.all(), many=True)
    return Response({'data': our_team_obj.data, 'message': 'Successfully Get Our Team', 'status': 200}, status=200)


@api_view(['GET', ])
def vision_view(request):
    vision_obj = VisionSerializer(instance=Vision.objects.all(), many=True)
    return Response({'data': vision_obj.data, 'message': 'Successfully Get Vision', 'status': 200}, status=200)


@api_view(['GET', ])
def mission_view(request):
    mission_obj = MissionSerializer(instance=Mission.objects.all(), many=True)
    return Response({'data': mission_obj.data, 'message': 'Successfully Get Our Team', 'status': 200}, status=200)


@api_view(['GET', ])
def f_and_q_view(request):
    f_and_q_obj = FAndQSerializer(instance=FAndQ.objects.all(), many=True)
    return Response({'data': f_and_q_obj.data, 'message': 'Successfully Get Our Team', 'status': 200}, status=200)
