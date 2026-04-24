"""初始化常用工具示例数据"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.common_tools.models import CommonToolCategory, CommonToolTag, CommonToolResource

User = get_user_model()


class Command(BaseCommand):
    help = '初始化常用工具示例数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化常用工具数据...')

        # 创建分类
        categories_data = [
            {'name': '测试工具', 'code': 'test_tools', 'icon': 'SetUp', 'sort': 1},
            {'name': '项目管理', 'code': 'project_mgmt', 'icon': 'FolderOpened', 'sort': 2},
            {'name': '文档中心', 'code': 'docs', 'icon': 'Document', 'sort': 3},
            {'name': 'Mock服务', 'code': 'mock', 'icon': 'Connection', 'sort': 4},
            {'name': '测试环境', 'code': 'env', 'icon': 'Monitor', 'sort': 5},
            {'name': '备忘信息', 'code': 'memo', 'icon': 'Memo', 'sort': 6},
            {'name': 'FAQ', 'code': 'faq', 'icon': 'QuestionFilled', 'sort': 7},
        ]
        category_map = {}
        for item in categories_data:
            obj, created = CommonToolCategory.objects.get_or_create(
                code=item['code'],
                defaults=item
            )
            category_map[item['code']] = obj
            self.stdout.write(f'  {"创建" if created else "跳过"}分类: {obj.name}')

        # 创建标签
        tags_data = [
            {'name': '自动化', 'color': '#409EFF'},
            {'name': '接口测试', 'color': '#67C23A'},
            {'name': 'UI测试', 'color': '#E6A23C'},
            {'name': '持续集成', 'color': '#F56C6C'},
            {'name': '文档', 'color': '#909399'},
            {'name': '环境', 'color': '#409EFF'},
            {'name': '常用', 'color': '#67C23A'},
        ]
        tag_map = {}
        for item in tags_data:
            obj, created = CommonToolTag.objects.get_or_create(
                name=item['name'],
                defaults=item
            )
            tag_map[item['name']] = obj
            self.stdout.write(f'  {"创建" if created else "跳过"}标签: {obj.name}')

        # 创建资源
        resources_data = [
            {
                'name': 'Jenkins', 'code': 'jenkins', 'type': 'tool_link',
                'category_code': 'test_tools',
                'tag_names': ['持续集成', '自动化'],
                'icon': 'SetUp', 'short_desc': '持续集成/持续部署服务器，自动化构建和测试',
                'content': 'Jenkins 是开源的自动化服务器，用于自动化构建、测试和部署。\n\n常用功能：\n- 自动触发构建\n- 测试报告集成\n- 构建流水线\n- 参数化构建',
                'url': 'http://jenkins.example.com', 'is_recommend': True, 'is_top': True,
            },
            {
                'name': 'Allure', 'code': 'allure', 'type': 'tool_link',
                'category_code': 'test_tools',
                'tag_names': ['自动化', '常用'],
                'icon': 'DataAnalysis', 'short_desc': '灵活的轻量级多语言测试报告工具',
                'content': 'Allure Framework 是一个灵活的轻量级多语言测试报告工具。\n\n安装方式：\n1. 下载 Allure 命令行工具\n2. 需要 Java 17+ 运行环境\n3. 测试代码中集成 allure-pytest 等适配器',
                'url': 'https://docs.qameta.io/allure-report/', 'is_recommend': True,
            },
            {
                'name': 'GitLab', 'code': 'gitlab', 'type': 'tool_link',
                'category_code': 'project_mgmt',
                'tag_names': ['持续集成', '常用'],
                'icon': 'Link', 'short_desc': '代码仓库和CI/CD平台',
                'content': 'GitLab 是一体化的 DevOps 平台，提供代码仓库、CI/CD、代码审查等功能。\n\n常用操作：\n- 创建 Merge Request\n- 查看 CI 流水线\n- 代码审查',
                'url': 'http://gitlab.example.com', 'is_recommend': True, 'is_top': True,
            },
            {
                'name': 'ONES文档', 'code': 'ones_doc', 'type': 'doc_link',
                'category_code': 'docs',
                'tag_names': ['文档'],
                'icon': 'Document', 'short_desc': '项目管理和需求文档平台',
                'content': 'ONES 是企业级研发管理平台，用于需求管理、项目跟踪、文档协作。\n\n常用入口：\n- 需求看板\n- 缺陷跟踪\n- 测试计划\n- 项目文档',
                'url': 'https://ones.example.com', 'is_recommend': True,
            },
            {
                'name': 'Mock平台', 'code': 'mock_platform', 'type': 'mock_platform',
                'category_code': 'mock',
                'tag_names': ['接口测试', '常用'],
                'icon': 'Connection', 'short_desc': '接口Mock服务，支持自定义响应数据',
                'content': 'Mock平台用于模拟后端接口响应，方便前端和测试人员独立开发调试。\n\n功能特性：\n- 自定义接口响应数据\n- 支持动态模板\n- 支持正则匹配\n- 批量导入接口',
                'url': 'http://mock.example.com', 'is_recommend': True,
            },
            {
                'name': '开发环境', 'code': 'env_dev', 'type': 'env_address',
                'category_code': 'env',
                'tag_names': ['环境'],
                'icon': 'Monitor', 'short_desc': '开发环境地址集合',
                'content': '开发环境信息：\n\n| 服务 | 地址 |\n|------|------|\n| 前端 | http://dev-frontend.example.com |\n| 后端API | http://dev-api.example.com:8000 |\n| 数据库 | dev-mysql.example.com:3306 |',
                'url': 'http://dev-frontend.example.com', 'env_type': 'dev',
            },
            {
                'name': '测试环境', 'code': 'env_test', 'type': 'env_address',
                'category_code': 'env',
                'tag_names': ['环境'],
                'icon': 'Monitor', 'short_desc': '测试环境地址集合',
                'content': '测试环境信息：\n\n| 服务 | 地址 |\n|------|------|\n| 前端 | http://test-frontend.example.com |\n| 后端API | http://test-api.example.com:8000 |\n| 数据库 | test-mysql.example.com:3306 |',
                'url': 'http://test-frontend.example.com', 'env_type': 'test', 'is_top': True,
            },
            {
                'name': '常用测试账号', 'code': 'test_accounts', 'type': 'memo',
                'category_code': 'memo',
                'tag_names': ['常用'],
                'icon': 'Key', 'short_desc': '各环境常用测试账号备忘',
                'content': '## 测试账号备忘\n\n### 管理员账号\n- 用户名: admin / 密码: admin123\n\n### 普通用户\n- 用户名: testuser / 密码: test123\n\n注意：生产环境请勿使用测试账号！',
                'url': '', 'open_mode': 'internal',
            },
            {
                'name': 'FAQ：如何配置Jenkins构建', 'code': 'faq_jenkins', 'type': 'faq',
                'category_code': 'faq',
                'tag_names': ['持续集成'],
                'icon': 'QuestionFilled', 'short_desc': 'Jenkins构建配置常见问题解答',
                'content': '## 如何配置Jenkins构建？\n\n### 1. 创建构建任务\n在Jenkins首页点击"新建Item"，输入任务名称，选择"自由风格的软件项目"。\n\n### 2. 配置源码管理\n在"源码管理"中选择Git，填入仓库地址和凭证。\n\n### 3. 配置构建触发器\n选择"轮询SCM"或"Webhook触发"。\n\n### 4. 配置构建步骤\n添加执行Shell或Python脚本。\n\n### 5. 配置构建后操作\n配置测试报告、邮件通知等。',
                'url': '', 'open_mode': 'internal',
            },
        ]

        admin_user = User.objects.filter(is_superuser=True).first()

        for item in resources_data:
            category_code = item.pop('category_code', None)
            tag_names = item.pop('tag_names', [])

            category = category_map.get(category_code) if category_code else None
            item['category'] = category
            item.setdefault('created_by', admin_user)

            obj, created = CommonToolResource.objects.get_or_create(
                code=item['code'],
                defaults=item
            )

            if created:
                # 添加标签
                for tag_name in tag_names:
                    tag = tag_map.get(tag_name)
                    if tag:
                        obj.tags.add(tag)

            self.stdout.write(f'  {"创建" if created else "跳过"}资源: {obj.name}')

        self.stdout.write(self.style.SUCCESS('\n常用工具数据初始化完成！'))
