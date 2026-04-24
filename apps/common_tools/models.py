from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonToolCategory(models.Model):
    """工具分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='分类编码')
    icon = models.CharField(max_length=50, blank=True, default='', verbose_name='图标')
    description = models.TextField(blank=True, default='', verbose_name='描述')
    sort = models.IntegerField(default=0, verbose_name='排序')
    is_enabled = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'common_tool_categories'
        verbose_name = '工具分类'
        verbose_name_plural = '工具分类'
        ordering = ['sort', '-created_at']

    def __str__(self):
        return self.name


class CommonToolTag(models.Model):
    """工具标签"""
    name = models.CharField(max_length=50, verbose_name='标签名称')
    color = models.CharField(max_length=20, blank=True, default='', verbose_name='标签颜色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'common_tool_tags'
        verbose_name = '工具标签'
        verbose_name_plural = '工具标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class CommonToolResource(models.Model):
    """工具资源"""
    TYPE_CHOICES = [
        ('tool_link', '工具链接'),
        ('website', '网站地址'),
        ('doc_link', '文档链接'),
        ('mock_platform', 'Mock平台'),
        ('env_address', '环境地址'),
        ('memo', '备忘信息'),
        ('faq', 'FAQ'),
        ('other', '其他'),
    ]

    OPEN_MODE_CHOICES = [
        ('_blank', '新窗口打开'),
        ('_self', '当前窗口打开'),
        ('internal', '站内查看'),
    ]

    ENV_TYPE_CHOICES = [
        ('dev', '开发环境'),
        ('test', '测试环境'),
        ('staging', '预发环境'),
        ('prod', '生产环境'),
        ('', '不涉及'),
    ]

    VISIBILITY_CHOICES = [
        ('public', '所有人可见'),
        ('team', '团队可见'),
        ('private', '仅自己可见'),
    ]

    name = models.CharField(max_length=200, verbose_name='资源名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='资源编码')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='资源类型')
    category = models.ForeignKey(
        CommonToolCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='resources', verbose_name='分类'
    )
    tags = models.ManyToManyField(
        CommonToolTag, blank=True, related_name='resources', verbose_name='标签'
    )
    icon = models.CharField(max_length=100, blank=True, default='', verbose_name='图标')
    short_desc = models.CharField(max_length=500, blank=True, default='', verbose_name='简介')
    content = models.TextField(blank=True, default='', verbose_name='使用说明/内容')
    url = models.URLField(max_length=500, blank=True, default='', verbose_name='访问地址')
    open_mode = models.CharField(
        max_length=20, choices=OPEN_MODE_CHOICES, default='_blank', verbose_name='打开方式'
    )
    env_type = models.CharField(
        max_length=20, choices=ENV_TYPE_CHOICES, blank=True, default='', verbose_name='环境类型'
    )
    owner_name = models.CharField(max_length=100, blank=True, default='', verbose_name='负责人')
    owner_contact = models.CharField(max_length=200, blank=True, default='', verbose_name='联系方式')
    sort = models.IntegerField(default=0, verbose_name='排序')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    is_enabled = models.BooleanField(default=True, verbose_name='是否启用')
    visibility_type = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default='public', verbose_name='可见范围'
    )
    extra_json = models.JSONField(default=dict, blank=True, verbose_name='扩展信息')
    access_count = models.IntegerField(default=0, verbose_name='访问次数')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_common_tools', verbose_name='创建者'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='updated_common_tools', verbose_name='更新者'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'common_tool_resources'
        verbose_name = '工具资源'
        verbose_name_plural = '工具资源'
        ordering = ['-is_top', 'sort', '-updated_at']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['category']),
            models.Index(fields=['is_enabled']),
            models.Index(fields=['is_recommend']),
        ]

    def __str__(self):
        return self.name


class CommonToolAccessLog(models.Model):
    """访问记录"""
    resource = models.ForeignKey(
        CommonToolResource, on_delete=models.CASCADE,
        related_name='access_logs', verbose_name='资源'
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='访问用户'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    access_type = models.CharField(
        max_length=20, default='view', verbose_name='访问类型',
        help_text='view=查看, click=点击链接'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='访问时间')

    class Meta:
        db_table = 'common_tool_access_logs'
        verbose_name = '访问记录'
        verbose_name_plural = '访问记录'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['resource', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.resource.name} - {self.user} - {self.created_at}'
