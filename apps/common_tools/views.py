from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from .models import CommonToolCategory, CommonToolTag, CommonToolResource, CommonToolAccessLog
from .serializers import (
    CommonToolCategorySerializer,
    CommonToolTagSerializer,
    CommonToolResourceListSerializer,
    CommonToolResourceDetailSerializer,
    CommonToolResourceWriteSerializer,
    CommonToolAccessLogSerializer,
)


class CommonToolCategoryViewSet(viewsets.ModelViewSet):
    queryset = CommonToolCategory.objects.all()
    serializer_class = CommonToolCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['sort', 'created_at']
    ordering = ['sort', '-created_at']


class CommonToolTagViewSet(viewsets.ModelViewSet):
    queryset = CommonToolTag.objects.all()
    serializer_class = CommonToolTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering = ['name']


class CommonToolResourceViewSet(viewsets.ModelViewSet):
    queryset = CommonToolResource.objects.none()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'is_enabled', 'is_recommend', 'is_top', 'env_type', 'visibility_type']
    search_fields = ['name', 'short_desc', 'content', 'owner_name']
    ordering_fields = ['name', 'sort', 'access_count', 'updated_at', 'created_at']
    ordering = ['-is_top', 'sort', '-updated_at']

    def get_queryset(self):
        qs = CommonToolResource.objects.select_related('category', 'created_by', 'updated_by').prefetch_related('tags')
        user = self.request.user
        # 前台接口只返回启用的资源
        action = getattr(self, 'action', None)
        if action in ['list', 'retrieve', 'dashboard', 'access']:
            qs = qs.filter(is_enabled=True)
            # 可见范围过滤
            if not user.is_superuser:
                qs = qs.filter(
                    Q(visibility_type='public') |
                    Q(visibility_type='team') |
                    Q(visibility_type='private', created_by=user)
                )
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CommonToolResourceListSerializer
        if self.action == 'retrieve':
            return CommonToolResourceDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CommonToolResourceWriteSerializer
        return CommonToolResourceDetailSerializer

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """首页聚合数据"""
        base_qs = self.get_queryset()

        # 推荐工具
        recommend = base_qs.filter(is_recommend=True)[:6]
        # 热门工具（按访问次数）
        hot = base_qs.order_by('-access_count')[:6]
        # 最近更新
        recent = base_qs.order_by('-updated_at')[:6]
        # FAQ入口
        faq = base_qs.filter(type='faq')[:4]
        # 分类导航
        categories = CommonToolCategory.objects.filter(
            is_enabled=True
        ).annotate(
            resource_count=Count('resources', filter=Q(resources__is_enabled=True))
        ).order_by('sort')[:10]

        return Response({
            'recommend': CommonToolResourceListSerializer(recommend, many=True).data,
            'hot': CommonToolResourceListSerializer(hot, many=True).data,
            'recent': CommonToolResourceListSerializer(recent, many=True).data,
            'faq': CommonToolResourceListSerializer(faq, many=True).data,
            'categories': CommonToolCategorySerializer(categories, many=True).data,
            'total_count': base_qs.count(),
            'type_count': {
                t['type']: t['count']
                for t in base_qs.values('type').annotate(count=Count('id'))
            },
        })

    @action(detail=True, methods=['post'], url_path='access')
    def access(self, request, pk=None):
        """记录访问"""
        resource = self.get_object()
        access_type = request.data.get('access_type', 'view')

        # 更新访问计数
        CommonToolResource.objects.filter(pk=resource.pk).update(
            access_count=resource.access_count + 1
        )

        # 记录日志
        CommonToolAccessLog.objects.create(
            resource=resource,
            user=request.user,
            ip_address=self._get_client_ip(request),
            access_type=access_type,
        )

        return Response({'message': '记录成功', 'access_count': resource.access_count + 1})

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """统计数据"""
        total = CommonToolResource.objects.count()
        enabled = CommonToolResource.objects.filter(is_enabled=True).count()
        by_type = {
            t['type']: t['count']
            for t in CommonToolResource.objects.values('type').annotate(count=Count('id'))
        }
        top_accessed = CommonToolResource.objects.filter(
            is_enabled=True
        ).order_by('-access_count')[:10]

        return Response({
            'total': total,
            'enabled': enabled,
            'by_type': by_type,
            'top_accessed': CommonToolResourceListSerializer(top_accessed, many=True).data,
        })

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class CommonToolAccessLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommonToolAccessLog.objects.select_related('resource', 'user')
    serializer_class = CommonToolAccessLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['resource', 'user', 'access_type']
    ordering = ['-created_at']
