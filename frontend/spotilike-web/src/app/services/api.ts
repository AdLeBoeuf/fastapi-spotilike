export const API_BASE = 'http://127.0.0.1:8000';

const isBrowser = typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
let inMemoryToken: string | null = null;

export function setAuthToken(token: string | null) {
  inMemoryToken = token;
  if (isBrowser) {
    try {
      if (token) localStorage.setItem('token', token);
      else localStorage.removeItem('token');
    } catch {}
  }
}

function buildHeaders(init?: HeadersInit): HeadersInit {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init as any || {}),
  };
  if (inMemoryToken) headers['Authorization'] = `Bearer ${inMemoryToken}`;
  return headers;
}

export const api = {
  async get<T = unknown>(url: string): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, { headers: buildHeaders() });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = (await res.json()) as T;
    return { data };
  },
  async post<T = unknown>(url: string, body?: unknown): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'POST',
      headers: buildHeaders(),
      body: body != null ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = (await res.json()) as T;
    return { data };
  },
  async put<T = unknown>(url: string, body?: unknown): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'PUT',
      headers: buildHeaders(),
      body: body != null ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = (await res.json()) as T;
    return { data };
  },
  async delete<T = unknown>(url: string): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'DELETE',
      headers: buildHeaders(),
    });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = (await res.json()) as T;
    return { data };
  },
};

// Initialize from localStorage (browser only)
if (isBrowser) {
  try { setAuthToken(localStorage.getItem('token')); } catch {}
}
