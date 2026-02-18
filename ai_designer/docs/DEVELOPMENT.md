# AI Designer - Development Guide

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Setup

1. **Clone repository**
```bash
git clone https://github.com/kogamishinyajerry-ops/aiWebdesigner.git
cd aiWebdesigner
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
```

3. **Frontend setup**
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
```

4. **Database setup**
```bash
# Run migrations
cd backend
alembic upgrade head

# Run seed data
python scripts/seed_data.py
```

5. **Start services**
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Or use Docker:
```bash
docker-compose up
```

## Project Structure

```
ai_designer/
├── backend/                 # FastAPI backend
│   ├── api/               # API routes
│   ├── core/              # Configuration
│   ├── crud/              # Database operations
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # AI services
│   ├── middleware/        # Custom middleware
│   └── tests/             # Backend tests
│
├── frontend/              # Next.js frontend
│   ├── app/              # App router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities
│   ├── hooks/            # Custom hooks
│   ├── tests/            # Frontend tests
│   └── styles/           # Global styles
│
├── docs/                 # Documentation
├── .github/             # GitHub workflows
└── docker-compose.yml    # Docker orchestration
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=.
```

### Frontend Tests
```bash
cd frontend
npm test
```

### E2E Tests
```bash
cd frontend
npm run test:e2e
```

## Development Workflow

1. Create feature branch
```bash
git checkout -b feature/your-feature
```

2. Make changes and commit
```bash
git add .
git commit -m "feat: description"
```

3. Run tests
```bash
# Backend
pytest

# Frontend
npm test
```

4. Push and create PR
```bash
git push origin feature/your-feature
```

## Code Style

### Backend (Python)
- Use Black for formatting
- Use Ruff for linting
- Use Type Hints
- Follow PEP 8

```bash
black backend/
ruff check backend/
mypy backend/
```

### Frontend (TypeScript)
- Use ESLint
- Use Prettier
- Follow Airbnb style guide

```bash
npm run lint
npm run format
```

## Architecture

### Backend Services

- **Image Generation Service**: SDXL/FLUX for image generation
- **SVG Generation Service**: Text-to-SVG with Gemini
- **Code Generation Service**: Design-to-Code with AI
- **Aesthetic Engine**: Style analysis and color recommendations

### Frontend Architecture

- **Next.js 14**: App Router with SSR/SSG
- **State Management**: Zustand for global state
- **Styling**: Tailwind CSS + Radix UI
- **API Communication**: Axios with interceptors

## Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_api_key
DEBUG=True
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### Common Issues

**Database connection error**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env

**AI model loading error**
- Verify GPU availability
- Check model paths in config
- Ensure enough GPU memory

**Redis connection error**
- Check Redis is running
- Verify REDIS_URL in .env

## Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

## Contributing

1. Follow the code style guidelines
2. Write tests for new features
3. Update documentation
4. Create pull requests

## License

MIT License
