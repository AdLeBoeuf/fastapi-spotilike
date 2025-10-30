import { api } from './api';

const AUTH_KEY = 'authUser';

export async function login(username: string, password: string) {
  const { data } = await api.post<{ ok: boolean; user: any }>(`/api/auth/login`, { username, password });
  try { localStorage.setItem(AUTH_KEY, JSON.stringify(data.user)); } catch {}
  return data.user;
}

export async function signup(username: string, email: string, password: string) {
  const { data } = await api.post<any>(`/api/users`, { username, email, password });
  try { localStorage.setItem(AUTH_KEY, JSON.stringify(data)); } catch {}
  return data;
}

export function logout() { try { localStorage.removeItem(AUTH_KEY); } catch {} }
export function isAuthenticated(): boolean { try { return !!localStorage.getItem(AUTH_KEY); } catch { return false; } }
