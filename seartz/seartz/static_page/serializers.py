from rest_framework import serializers
from .models import *


class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = "__all__"


class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = "__all__"


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = "__all__"


class FAndQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAndQ
        fields = "__all__"
