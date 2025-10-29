import { api } from './api';

export interface Genre {
  id: number;
  title: string;
  description?: string | null;
}

export async function fetchGenres() {
  const res = await api.get(`/api/genres?limit=200`);
  return res.data as Genre[];
}
