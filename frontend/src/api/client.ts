import type {
  RecommendRequest,
  ScreenRequest,
  ScreenResponse,
} from '../types/models';

export interface HealthResponse {
  status: string;
}

const BASE_URL = 'https://silver-space-meme-g5r5j4945v4fppvq-8000.app.github.dev';

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch('/health');
  if (!res.ok) {
    throw new Error('Network error');
  }
  return res.json();
}

export async function postScreen(req: ScreenRequest): Promise<ScreenResponse> {
  const res = await fetch(`${BASE_URL}/screen`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error('Network error');
  }
  return res.json();
}

export async function postRecommend(
  req: RecommendRequest,
): Promise<ScreenResponse> {
  const res = await fetch(`${BASE_URL}/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) {
    throw new Error('Network error');
  }
  return res.json();
}
