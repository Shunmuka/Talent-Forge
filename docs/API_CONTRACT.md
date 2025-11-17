# Talent Forge MVP - API Contract

## Base URL
- Development: `http://localhost:8000`
- Production: `[TBD]`

## Authentication
- **Status**: Stubbed for MVP (all endpoints currently open)
- **Future**: Google OAuth JWT tokens
- **Header**: `Authorization: Bearer <token>`

## Endpoints

### POST /api/analyze

Analyze resume against job description.

**Request Body (JSON):**
```json
{
  "resumeText": "string (optional if resumeFileId provided)",
  "resumeFileId": "string (optional, not yet implemented)",
  "jobDescription": "string (required, min 10 chars)"
}
```

**Request (Form Data - File Upload):**
- `resume_file`: File (PDF, DOCX, TXT)
- `job_description`: String

**Response:**
```json
{
  "score": 72,
  "gaps": [
    {
      "skill": "GraphQL",
      "reason": "Job requires GraphQL experience but resume doesn't mention it"
    }
  ],
  "evidence": [
    {
      "resumeText": "Led team of 5 engineers",
      "jdText": "Experience leading engineering teams"
    }
  ],
  "bullets": [
    "Led team of 5 engineers to deliver product",
    "Improved performance by 30%"
  ]
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request (missing/invalid input)
- `422`: Validation error
- `500`: Server error

**Constraints:**
- File size: Max 16MB
- Supported formats: PDF, DOCX, TXT
- Response time target: ≤5s

---

### POST /api/rewrite

Rewrite a resume bullet point.

**Request Body:**
```json
{
  "original": "string (required, min 5 chars)",
  "context": "string (optional, job description or resume context)"
}
```

**Response:**
```json
{
  "original": "Worked on software projects",
  "revised": "Led development of scalable software solutions, improving system performance by 30%",
  "rationale": "Added action verb 'Led', quantified impact with '30%', and used job-relevant terminology"
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad request
- `422`: Validation error
- `500`: Server error

---

### GET /healthz

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200`: Service is healthy

---

## Validation Rules

### Analyze Request
- `jobDescription`: Required, min 10 characters
- `resumeText` or `resumeFileId`: At least one required
- File: Max 16MB, must be PDF/DOCX/TXT

### Rewrite Request
- `original`: Required, min 5 characters
- `context`: Optional

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

- **Current**: None (MVP)
- **Future**: Rate limits on `/api/rewrite` (TBD)

## OpenAPI Spec

Full OpenAPI 3.0 specification: `openapi/talent-forge.v1.yaml`
