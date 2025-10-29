import { api } from './api';

export interface Album {
  id: number;
  title: string;
  cover?: string | null;
  release_date?: string | null; // ISO date
  artist_id: number;
  artist_name?: string | null;
}

export async function fetchAlbums() {
  const res = await api.get(`/api/albums?limit=100`);
  return res.data as Album[];
}

export async function fetchAlbum(id: number) {
  const res = await api.get(`/api/albums/${id}`);
  return res.data as Album;
}

export async function fetchAlbumSongs(id: number) {
  const res = await api.get(`/api/albums/${id}/songs?limit=200`);
  return res.data as any[];
}
