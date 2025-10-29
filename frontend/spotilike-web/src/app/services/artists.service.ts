import { api } from './api';

export interface Artist {
  id: number;
  name: string;
  avatar?: string | null;
  bio?: string | null;
}

export async function fetchArtists(): Promise<Artist[]> {
  const res = await api.get(`/api/artists?limit=50`);
  return res.data as Artist[];
}

export async function fetchArtist(id: number): Promise<Artist> {
  const res = await api.get(`/api/artists/${id}`);
  return res.data as Artist;
}

export async function fetchArtistSongs(id: number) {
  const res = await api.get(`/api/artists/${id}/songs?limit=100`);
  return res.data as any[];
}

