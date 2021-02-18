from rest_framework import serializers
from .models import *
from PLR_APIs.logs import *
import sys


class AllFoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllFolders
        fields = '__all__'

    def create(self, validated_data):
        try:
            if 'parent_id' in validated_data and validated_data['parent_id'] != '':
                folder_path = upper_tree_folder(validated_data['parent_id']) + f"{validated_data['parent_id'].folder_name}/{validated_data['folder_name']}"
            else:
                folder_path = f"/{validated_data['folder_name']}"
            if validated_data['user'].is_company:
                upload_dir = os.path.join(f"media/plr/{str(validated_data['user'].username)}/Documents{folder_path}")
            else:
                upload_dir = os.path.join(f"media/plr/{validated_data['user'].company_sub_user_id.username}/{validated_data['user'].username}/Documents{folder_path}")
            os.makedirs(upload_dir)
            return AllFolders.objects.create(**validated_data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logger.error(str((e, exc_type, f_name, exc_tb.tb_lineno)))
            raise serializers.ValidationError(str((e, exc_type, f_name, exc_tb.tb_lineno)))


class DMSSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScanFile
        fields = '__all__'


class FileTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileTag
        fields = '__all__'
