# Business Estimator 🚀

A full-stack web application that helps entrepreneurs calculate total investment required to start their business. Uses Claude AI to provide intelligent, location-aware cost estimation with multi-agent architecture.

## Features

- **Multi-Business Support**: Cafe, Salon, Retail Shop, Fitness Studio, Co-working Space
- **Intelligent Cost Estimation**: Claude AI agents analyze market data and provide realistic cost breakdowns
- **Interactive Calculator**: User-friendly React interface for input and visualization
- **Cost Breakdown**: Detailed categorization (setup, inventory, staffing, licensing, etc.)
- **Business Plan Generation**: AI-powered recommendations and insights
- **Funding Analysis**: Breakdown of funding sources
- **Responsive Design**: Works on desktop and mobile

## Tech Stack

**Backend:**
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy ORM
- LangGraph (for multi-agent AI)
- Claude API

**Frontend:**
- React 18
- Vite
- Axios for API calls
- Tailwind CSS

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)

## Project Structure

```
business-estimator/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Entry point
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # DB setup
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── ai_agent.py     # LangGraph setup
│   │   ├── schemas.py      # Pydantic models
│   │   └── api/            # Route handlers
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── docker-compose.yml
├── nginx.conf
└── docs/
    ├── SETUP_GUIDE.md
    └── DEPLOYMENT_GUIDE.md
```

## Quick Start

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Local Development
See [SETUP_GUIDE.md](./docs/SETUP_GUIDE.md)

## Deployment

See [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger documentation.

## Environment Variables

Create `.env` files in both backend and frontend directories. See `.env.example` files for required variables.

**Key Backend Variables:**
- `CLAUDE_API_KEY`: Your Anthropic API key
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: dev, staging, or prod

**Key Frontend Variables:**
- `VITE_API_URL`: Backend API endpoint

## License

MIT
