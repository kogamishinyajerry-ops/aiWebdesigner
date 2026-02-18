# Testing Guide

## Overview

This guide covers the testing setup and best practices for the AI Designer project.

## Test Structure

```
ai_designer/
├── frontend/
│   └── tests/
│       ├── setup.ts              # Vitest setup
│       ├── components/           # Unit tests
│       │   ├── button.test.tsx
│       │   ├── card.test.tsx
│       │   ├── badge.test.tsx
│       │   └── ...
│       └── e2e/                  # E2E tests
│           ├── home.spec.ts
│           ├── dashboard.spec.ts
│           └── generator.spec.ts
└── backend/
    └── tests/
        ├── conftest.py            # Pytest fixtures
        ├── test_crud.py           # CRUD tests
        ├── test_middleware.py     # Middleware tests
        ├── test_redis.py          # Redis tests
        ├── test_image_api.py      # Image API tests
        ├── test_svg_api.py        # SVG API tests
        ├── test_code_api.py       # Code API tests
        ├── test_aesthetic_api.py  # Aesthetic API tests
        └── test_services.py       # Service tests
```

## Frontend Testing

### Unit Tests

Run unit tests:
```bash
cd frontend
npm test
```

Run with coverage:
```bash
npm run test:coverage
```

Run with UI:
```bash
npm run test:ui
```

### E2E Tests

Run E2E tests:
```bash
npm run test:e2e
```

Run E2E with UI:
```bash
npm run test:e2e:ui
```

Debug E2E:
```bash
npm run test:e2e:debug
```

### Test Configuration

**vitest.config.ts**
- Environment: jsdom
- Coverage provider: v8
- Setup file: `tests/setup.ts`

**playwright.config.ts**
- Browsers: Chromium, Firefox, WebKit
- Mobile: Pixel 5, iPhone 12
- Dev server: npm run dev

## Backend Testing

### Run Tests

Run all tests:
```bash
cd backend
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_crud.py
```

Run with markers:
```bash
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
pytest -m slow           # Slow tests only
```

### Test Configuration

**pytest.ini**
- Test directory: `tests/`
- Async mode: auto
- Coverage: HTML + terminal
- Markers: unit, integration, slow, asyncio

### Fixtures

Available fixtures in `conftest.py`:

- `db_session`: Async database session
- `client`: HTTP test client
- `test_user_data`: Sample user data
- `test_project_data`: Sample project data

### Example Test

```python
import pytest
from httpx import AsyncClient

@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "password": "Test123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

## CI/CD

### GitHub Actions

**Lint Workflow** (.github/workflows/lint.yml)
- Runs on: push, pull_request
- Lints: Frontend (ESLint), Backend (Ruff)
- Type checks: Frontend (tsc), Backend (mypy)

**Test Workflow** (.github/workflows/test.yml)
- Runs on: push, pull_request
- Tests: Unit tests, E2E tests, API tests
- Coverage: Generated and uploaded
- Matrix: Multiple Node/Python versions

## Best Practices

### Frontend

1. **Unit Tests**
   - Test component rendering
   - Test user interactions
   - Test props and state
   - Mock external dependencies

2. **E2E Tests**
   - Test user flows
   - Test critical paths
   - Use page object pattern
   - Avoid flaky tests

3. **Coverage Goals**
   - Aim for 80%+ coverage
   - Focus on business logic
   - Don't test trivial code

### Backend

1. **Unit Tests**
   - Test in isolation
   - Use test fixtures
   - Mock external services
   - Test happy and error paths

2. **Integration Tests**
   - Test API endpoints
   - Test database operations
   - Test middleware
   - Use test database

3. **Async Tests**
   - Mark with `@pytest.mark.asyncio`
   - Use async fixtures
   - Handle cleanup properly
   - Test concurrent operations

## Test Commands Reference

### Frontend

| Command | Description |
|---------|-------------|
| `npm test` | Run unit tests |
| `npm run test:ui` | Run tests with UI |
| `npm run test:coverage` | Run with coverage |
| `npm run test:e2e` | Run E2E tests |
| `npm run test:e2e:ui` | Run E2E with UI |
| `npm run test:e2e:debug` | Debug E2E tests |
| `npm run test:all` | Run all tests |

### Backend

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -m unit` | Unit tests only |
| `pytest -m integration` | Integration tests only |
| `pytest --cov` | With coverage |
| `pytest --cov-report=html` | HTML coverage report |
| `pytest tests/test_file.py` | Specific file |
| `pytest -k test_name` | Test by name |

## Troubleshooting

### Common Issues

1. **Tests Timeout**
   - Increase timeout in pytest.ini
   - Check for hanging async operations

2. **Database Errors**
   - Ensure test database exists
   - Check connection string

3. **Redis Errors**
   - Ensure Redis is running
   - Check Redis connection settings

4. **E2E Flaky Tests**
   - Increase wait timeouts
   - Use explicit waits instead of implicit
   - Check for race conditions

## Resources

- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Library](https://testing-library.com/)
