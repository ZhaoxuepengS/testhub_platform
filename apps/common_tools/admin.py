from django.contrib import admin
from .models import CommonToolCategory, CommonToolTag, CommonToolResource, CommonToolAccessLog


@admin.register(CommonToolCategory)
class CommonToolCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'icon', 'sort', 'is_enabled', 'created_at']
    list_filter = ['is_enabled']
    search_fields = ['name', 'code']
    ordering = ['sort']


@admin.register(CommonToolTag)
class CommonToolTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name']


@admin.register(CommonToolResource)
class CommonToolResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'type', 'category', 'is_top', 'is_recommend',
                    'is_enabled', 'access_count', 'owner_name', 'updated_at']
    list_filter = ['type', 'is_enabled', 'is_top', 'is_recommend', 'env_type', 'visibility_type']
    search_fields = ['name', 'code', 'short_desc', 'content', 'owner_name']
    filter_horizontal = ['tags']
    ordering = ['-is_top', 'sort', '-updated_at']
    readonly_fields = ['access_count', 'created_at', 'updated_at']


@admin.register(CommonToolAccessLog)
class CommonToolAccessLogAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'access_type', 'ip_address', 'created_at']
    list_filter = ['access_type', 'created_at']
    search_fields = ['resource__name', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
