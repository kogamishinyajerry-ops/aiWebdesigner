# AI Designer API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.aidesigner.com
```

## Authentication

API uses JWT tokens for authentication.

```bash
Authorization: Bearer <token>
```

## Health Check

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "models": "loaded"
}
```

---

## Image Generation

### POST /api/v1/image/generate

Generate an image using AI model.

**Request:**
```json
{
  "prompt": "A modern hero banner with gradient colors",
  "style": "modern",
  "size": "hero_medium",
  "negative_prompt": "blurry, low quality",
  "guidance_scale": 7.5,
  "num_steps": 50,
  "seed": 12345
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | Yes | Image description |
| style | string | No | Style preset (modern, minimal, glassmorphism, etc.) |
| size | string | No | Size preset (hero_medium, icon, etc.) |
| guidance_scale | float | No | Guidance strength (default: 7.5) |
| num_steps | int | No | Number of inference steps (default: 50) |
| seed | int | No | Random seed for reproducibility |

**Response:**
```json
{
  "success": true,
  "image_url": "data:image/png;base64,...",
  "generation_id": "uuid",
  "generation_time": 2.5,
  "prompt": "...",
  "dimensions": {"width": 1280, "height": 720},
  "style": "modern",
  "seed": 12345,
  "request_id": "uuid"
}
```

### POST /api/v1/image/icons

Generate icon set.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| concept | string | Yes | Icon concept (navigation, social, etc.) |
| style | string | No | Icon style (outline, filled, etc.) |
| count | int | No | Number of icons (1-10) |
| size | string | No | Icon size preset |

### POST /api/v1/image/background

Generate background texture.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| style | string | No | Background style (gradient, pattern, etc.) |
| colors | string | No | Comma-separated colors |
| complexity | string | No | Complexity level (low, medium, high) |
| size | string | No | Size preset |

---

## SVG Generation

### POST /api/v1/svg/generate

Generate SVG from text description.

**Request:**
```json
{
  "description": "A minimalist logo with a circle",
  "style": "modern",
  "width": 512,
  "height": 512,
  "optimize": true
}
```

### POST /api/v1/svg/icon-set

Generate a set of icons.

---

## Code Generation

### POST /api/v1/code/generate

Generate code from design description.

**Request:**
```json
{
  "description": "A modern button component",
  "framework": "react",
  "language": "typescript",
  "with_tailwind": true,
  "component_name": "Button"
}
```

### POST /api/v1/code/component-library

Generate a component library.

### POST /api/v1/code/optimize

Optimize existing code.

---

## Aesthetic Engine

### POST /api/v1/aesthetic/colors/recommend

Get color palette recommendations.

### POST /api/v1/aesthetic/style/analyze

Analyze design style from description.

### POST /api/v1/aesthetic/score

Calculate aesthetic score for design.

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "error_code": "ERROR_CODE",
  "request_id": "uuid",
  "detail": "Detailed error information"
}
```

**Error Codes:**
| Code | Status | Description |
|-------|---------|-------------|
| VALIDATION_ERROR | 422 | Invalid request data |
| NOT_FOUND | 404 | Resource not found |
| CONFLICT_ERROR | 409 | Resource conflict |
| UNAUTHORIZED_ERROR | 401 | Unauthorized access |
| RATE_LIMIT_ERROR | 429 | Rate limit exceeded |

## Rate Limiting

| Endpoint | Limit |
|----------|--------|
| Image generation | 10 req/min |
| SVG generation | 30 req/min |
| Code generation | 20 req/min |
| Other | 100 req/min |

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```
