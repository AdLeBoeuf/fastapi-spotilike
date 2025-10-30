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

export function getAuthToken(): string | null {
  if (inMemoryToken) return inMemoryToken;
  if (isBrowser) {
    try { return localStorage.getItem('token'); } catch { return null; }
  }
  return null;
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
    if (!res.ok) throw await buildError(res);
    const data = (await res.json()) as T;
    return { data };
  },
  async post<T = unknown>(url: string, body?: unknown): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'POST',
      headers: buildHeaders(),
      body: body != null ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw await buildError(res);
    const data = (await res.json()) as T;
    return { data };
  },
  async postForm<T = unknown>(url: string, form: Record<string, string>): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'POST',
      headers: buildHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' }),
      body: new URLSearchParams(form).toString(),
    });
    if (!res.ok) throw await buildError(res);
    const data = (await res.json()) as T;
    return { data };
  },
  async put<T = unknown>(url: string, body?: unknown): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'PUT',
      headers: buildHeaders(),
      body: body != null ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw await buildError(res);
    const data = (await res.json()) as T;
    return { data };
  },
  async delete<T = unknown>(url: string): Promise<{ data: T }> {
    const res = await fetch(`${API_BASE}${url}`, {
      method: 'DELETE',
      headers: buildHeaders(),
    });
    if (!res.ok) throw await buildError(res);
    const data = (await res.json()) as T;
    return { data };
  },
};

// Initialize from localStorage (browser only)
if (isBrowser) {
  try { setAuthToken(localStorage.getItem('token')); } catch {}
}

async function buildError(res: Response): Promise<Error> {
  try {
    const ct = res.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      const j = await res.json();
      const msg = j?.detail || j?.message || `${res.status} ${res.statusText}`;
      return new Error(msg);
    } else {
      const t = await res.text();
      return new Error(t || `${res.status} ${res.statusText}`);
    }
  } catch {
    return new Error(`${res.status} ${res.statusText}`);
  }
}
