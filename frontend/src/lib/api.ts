/** API client for Talent Forge backend. */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface AnalyzeRequest {
  resumeText?: string;
  resumeFileId?: string;
  jobDescription: string;
}

export interface AnalyzeResponse {
  score: number;
  gaps: Array<{ skill: string; reason: string }>;
  evidence: Array<{ resumeText: string; jdText: string }>;
  bullets: string[];
}

export interface RewriteRequest {
  original: string;
  context?: string;
}

export interface RewriteResponse {
  original: string;
  revised: string;
  rationale: string;
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

export async function analyze(
  request: AnalyzeRequest
): Promise<AnalyzeResponse> {
  return fetchAPI<AnalyzeResponse>("/api/analyze", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function analyzeWithFile(
  formData: FormData
): Promise<AnalyzeResponse> {
  const url = `${API_BASE_URL}/api/analyze`;
  const response = await fetch(url, {
    method: "POST",
    body: formData,
    // Don't set Content-Type header - browser will set it automatically with boundary for FormData
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

export async function rewrite(
  request: RewriteRequest
): Promise<RewriteResponse> {
  return fetchAPI<RewriteResponse>("/api/rewrite", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
