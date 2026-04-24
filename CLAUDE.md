# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TestHub is an AI-driven test management platform built with Django 4.2 (backend) + Vue 3 (frontend). It provides test case management, API testing, UI/APP automation testing, AI-powered requirement analysis, and test case generation capabilities.

## Common Commands

### Backend (Django)

```bash
# Activate the virtual environment (Windows)
.venv\Scripts\Activate.ps1
# Activate the virtual environment (macOS/Linux)
source .venv/bin/activate

# Start development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Management commands
python manage.py run_all_scheduled_tasks    # Run all scheduled tasks (API testing + UI automation)
python manage.py init_locator_strategies    # Initialize UI automation locator strategies
python manage.py download_webdrivers        # Download webdrivers for UI automation
python manage.py load_component_pack        # Load APP automation component pack
```

### Frontend (Vue 3 + Vite)

```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start dev server (port 3000, proxies /api/ and /ws/ to Django at :8000)
npm run build        # Production build
npm run lint         # ESLint with auto-fix
```

### Celery Worker

```bash
celery -A backend worker -l info           # Start Celery worker
celery -A backend beat -l info             # Start Celery beat scheduler
```

## Architecture

### Backend Structure (`apps/`)

Each Django app under `apps/` follows the standard pattern: `models.py`, `serializers.py`, `views.py`, `urls.py`. Key apps:

- **users**: Custom User model (`AUTH_USER_MODEL = 'users.User'`) extending AbstractUser, with UserProfile for settings (theme/language/timezone). JWT auth via SimpleJWT with token blacklist.
- **projects**: Project and team management
- **testcases**: Manual test case management with steps, attachments, comments
- **testsuites**: Test suite organization
- **executions**: Test plan execution and result tracking
- **reports**: Test report generation
- **reviews**: Test case review workflow with templates and assignments
- **versions**: Version/release management
- **requirement_analysis**: AI-powered document parsing (PDF/Word/TXT via pypdf/python-docx) and test case generation. `AIModelConfig` stores per-model API credentials. `services.py` handles orchestration, `advanced_analyzer.py` does the analysis.
- **assistant**: Dify AI chatbot integration
- **api_testing**: HTTP/WebSocket API testing. `variable_resolver.py` for env variable substitution, `custom_email_backend.py` for notification emails, `operation_logger.py` for audit logging.
- **ui_automation**: Dual-engine (Selenium + Playwright) UI automation. `selenium_engine.py` / `playwright_engine.py` for execution, `ai_agent.py` / `ai_base.py` for AI browser-use mode (browser-use + langchain-openai), `test_executor.py` for orchestration, `variable_resolver.py` for script variables, `pdf_generator.py` for report PDFs.
- **app_automation**: Android APP automation via Airtest. `utils/airtest_base.py` for device interaction, `utils/ocr_helper.py` for OCR-based element finding (easyocr + opencv), `runners/ui_flow_runner.py` for JSON-based UI flow execution, `executors/test_executor.py` for test orchestration, `managers/device_manager.py` for ADB device pool management, `consumers.py` for WebSocket real-time progress via Django Channels.
- **core**: Shared configuration, locator strategies, management commands
- **data_factory**: Test data generation tools. Each tool in `tools/` is a standalone module (json_tools, random_tools, encryption_tools, etc.). `tool_list.py` registers available tools.

### Frontend Structure (`frontend/src/`)

- **views/**: Page components organized by feature module (matches backend app names)
- **api/**: Axios-based API service layer (one file per module: `api-testing.js`, `ui_automation.js`, `app-automation.js`, `requirement-analysis.js`, `core.js`, `data-factory.js`)
- **stores/**: Pinia stores (`user.js` for auth/token state, `app.js` for global state)
- **router/**: Vue Router with static imports for all components, auth guards via `requiresAuth`/`requiresGuest` meta
- **locales/**: i18n via vue-i18n with `zh-cn` and `en` translations
- **layout/**: App shell/layout components
- **components/**: Shared components

### Key Cross-Cutting Patterns

- **Auth flow**: JWT double-token (access 60min + refresh 7d), auto-refresh on frontend, token blacklist on logout. Frontend stores tokens in Pinia user store, Axios interceptors handle refresh queuing.
- **Celery async tasks**: Celery auto-discovers `tasks.py` in each app. Used for scheduled API/UI/APP test execution. Requires Redis as broker.
- ** **WebSocket (Django Channels)**: Used by `app_automation` for real-time execution progress. Requires `channels_redis` backend. Consumer at `app_automation/consumers.py`, routing in `app_automation/routing.py`.
- **Variable resolution**: Both `api_testing/variable_resolver.py` and `ui_automation/variable_resolver.py` handle `{{variable}}` syntax substitution from environment configs.
- **Allure reports**: Both `api_testing` and `app_automation` generate Allure-format reports (via `allure-pytest`).
- **AI model config**: `requirement_analysis.AIModelConfig` is the central model for AI provider settings. UI automation AI mode additionally supports OpenAI/Anthropic/Gemini/DeepSeek/Groq via browser-use's own model resolution.

### API URL Routing

All endpoints under `/api/`, configured in `backend/urls.py`:
- `/api/auth/` and `/api/users/`: Auth (JWT token obtain/refresh/verify)
- `/api/projects/`, `/api/testcases/`, `/api/testsuites/`, `/api/executions/`, `/api/reports/`, `/api/reviews/`, `/api/versions/`
- `/api/assistant/`, `/api/requirement-analysis/`
- `/api/` (api_testing): No prefix — api_testing URLs mount directly
- `/api/ui-automation/`, `/api/app-automation/`
- `/api/core/`, `/api/data-factory/`
- `/api/docs/` (Swagger), `/api/redoc/` (ReDoc)

### Configuration

- `backend/settings.py`: Django settings — uses `python-decouple` for env vars
- `.env`: Environment variables (copy from `.env.example`). Key vars: `DB_*`, `REDIS_URL`, `SECRET_KEY`, `EMAIL_*`, `LANGUAGE_CODE`, `TIME_ZONE`
- `frontend/vite.config.js`: Dev server on port 3000, proxies `/api/`, `/media/`, `/ws/` to Django at `:8000`

## Database

MySQL 8.0+ with `utf8mb4` charset. Custom user model (`AUTH_USER_MODEL = 'users.User'`). All config via env vars: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

## Commit 规范

- 默认不自动提交代码
- 多个相关修改应合并为一个 commit
- commit message 格式：`<type>: <简短描述>`
- 提交前必须运行 lint 和测试
