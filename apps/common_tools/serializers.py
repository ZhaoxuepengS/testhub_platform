from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CommonToolCategory, CommonToolTag, CommonToolResource, CommonToolAccessLog

User = get_user_model()


class CommonToolCategorySerializer(serializers.ModelSerializer):
    resource_count = serializers.SerializerMethodField()

    class Meta:
        model = CommonToolCategory
        fields = ['id', 'name', 'code', 'icon', 'description', 'sort',
                  'is_enabled', 'resource_count', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_resource_count(self, obj):
        return obj.resources.filter(is_enabled=True).count()


class CommonToolTagSerializer(serializers.ModelSerializer):
    resource_count = serializers.SerializerMethodField()

    class Meta:
        model = CommonToolTag
        fields = ['id', 'name', 'color', 'resource_count', 'created_at']
        read_only_fields = ['created_at']

    def get_resource_count(self, obj):
        return obj.resources.filter(is_enabled=True).count()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name']


class CommonToolResourceListSerializer(serializers.ModelSerializer):
    """列表页用的轻量序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    tags_info = CommonToolTagSerializer(source='tags', many=True, read_only=True)

    class Meta:
        model = CommonToolResource
        fields = [
            'id', 'name', 'code', 'type', 'type_display', 'category', 'category_name',
            'tags_info', 'icon', 'short_desc', 'url', 'open_mode', 'env_type',
            'owner_name', 'sort', 'is_top', 'is_recommend', 'is_enabled',
            'visibility_type', 'access_count', 'updated_at',
        ]


class CommonToolResourceDetailSerializer(serializers.ModelSerializer):
    """详情页用的完整序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True, default='')
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    open_mode_display = serializers.CharField(source='get_open_mode_display', read_only=True)
    env_type_display = serializers.CharField(source='get_env_type_display', read_only=True, default='')
    visibility_type_display = serializers.CharField(source='get_visibility_type_display', read_only=True)
    tags_info = CommonToolTagSerializer(source='tags', many=True, read_only=True)
    created_by_info = SimpleUserSerializer(source='created_by', read_only=True)
    updated_by_info = SimpleUserSerializer(source='updated_by', read_only=True)

    class Meta:
        model = CommonToolResource
        fields = [
            'id', 'name', 'code', 'type', 'type_display', 'category', 'category_name',
            'tags_info', 'icon', 'short_desc', 'content', 'url', 'open_mode',
            'open_mode_display', 'env_type', 'env_type_display',
            'owner_name', 'owner_contact', 'sort', 'is_top', 'is_recommend',
            'is_enabled', 'visibility_type', 'visibility_type_display',
            'extra_json', 'access_count',
            'created_by', 'created_by_info', 'updated_by', 'updated_by_info',
            'created_at', 'updated_at',
        ]


class CommonToolResourceWriteSerializer(serializers.ModelSerializer):
    """创建/更新用的序列化器"""
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=CommonToolTag.objects.all(), many=True, write_only=True,
        required=False, source='tags'
    )

    class Meta:
        model = CommonToolResource
        fields = [
            'id', 'name', 'code', 'type', 'category', 'tag_ids',
            'icon', 'short_desc', 'content', 'url', 'open_mode', 'env_type',
            'owner_name', 'owner_contact', 'sort', 'is_top', 'is_recommend',
            'is_enabled', 'visibility_type', 'extra_json',
        ]

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().update(instance, validated_data)


class CommonToolAccessLogSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True, default='')

    class Meta:
        model = CommonToolAccessLog
        fields = ['id', 'resource', 'resource_name', 'user', 'username',
                  'ip_address', 'access_type', 'created_at']
        read_only_fields = ['created_at']
