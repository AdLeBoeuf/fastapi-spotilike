import { api } from './api';

export interface Song {
  id: number;
  title: string;
  duration?: number | null;
  artist_id?: number | null;
  artist_name?: string | null;
  album_id?: number | null;
  album_title?: string | null;
}

export async function fetchSongs(limit = 100) {
  const res = await api.get(`/api/songs?limit=${limit}`);
  return res.data as Song[];
}

export async function fetchSongsWithParams(params: Record<string, any>) {
  const search = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== null && v !== undefined && `${v}`.length > 0) search.append(k, String(v));
  }
  if (!search.has('limit')) search.set('limit', '100');
  const url = `/api/songs?${search.toString()}`;
  const res = await api.get(url);
  return res.data as Song[];
}
