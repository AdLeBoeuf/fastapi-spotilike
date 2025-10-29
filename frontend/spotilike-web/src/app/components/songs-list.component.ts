import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { fetchSongs, fetchSongsWithParams, Song } from '../services/songs.service';
import { fetchArtists, Artist } from '../services/artists.service';
import { fetchAlbums, Album } from '../services/albums.service';
import { fetchGenres, Genre } from '../services/genres.service';

@Component({
  selector: 'app-songs-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  template: `
  <section class="container">
    <h1>Songs</h1>
    <div class="filters">
      <input type="text" placeholder="Search title..." [(ngModel)]="q" (keyup.enter)="load()" />
      <select [(ngModel)]="artistId" (change)="load()">
        <option [ngValue]="null">All artists</option>
        <option *ngFor="let a of artists" [ngValue]="a.id">{{ a.name }}</option>
      </select>
      <select [(ngModel)]="albumId" (change)="load()">
        <option [ngValue]="null">All albums</option>
        <option *ngFor="let a of albums" [ngValue]="a.id">{{ a.title }}</option>
      </select>
      <select [(ngModel)]="genreId" (change)="load()">
        <option [ngValue]="null">All genres</option>
        <option *ngFor="let g of genres" [ngValue]="g.id">{{ g.title }}</option>
      </select>
      <button (click)="clearFilters()" [disabled]="loading">Clear</button>
    </div>
    <div *ngIf="error" class="error">{{error}}</div>
    <ul *ngIf="songs?.length; else empty">
      <li *ngFor="let s of songs">
        <div class="meta">
          <strong>{{ s.title }}</strong>
          <small class="muted"> • duration: {{ s.duration || 'n/a' }}</small>
          <div class="muted">
            artist:
            <a *ngIf="s.artist_id" [routerLink]="['/artists', s.artist_id]">{{ s.artist_name || ('#' + s.artist_id) }}</a>
            <span *ngIf="!s.artist_id">n/a</span>
            • album:
            <a *ngIf="s.album_id" [routerLink]="['/albums', s.album_id]">{{ s.album_title || ('#' + s.album_id) }}</a>
            <span *ngIf="!s.album_id">n/a</span>
          </div>
        </div>
      </li>
    </ul>
    <ng-template #empty>
      <p>No songs yet.</p>
    </ng-template>
  </section>
  `,
  styles: [`
    .container { max-width: 720px; margin: 24px auto; padding: 0 16px; }
    .filters { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px; }
    .filters input, .filters select { padding: 6px 8px; }
    ul { list-style: none; padding: 0; }
    li { display: flex; align-items: center; gap: 10px; padding: 10px 0; border-bottom: 1px solid #eee; }
    .muted { color: #666; }
    .error { color: #b00020; }
  `]
})
export class SongsListComponent implements OnInit {
  songs: Song[] = [];
  artists: Artist[] = [];
  albums: Album[] = [];
  genres: Genre[] = [];
  loading = false;
  error = '';
  q: string = '';
  artistId: number | null = null;
  albumId: number | null = null;
  genreId: number | null = null;

  async ngOnInit() {
    // Preload filter data
    try {
      [this.artists, this.albums, this.genres] = await Promise.all([
        fetchArtists(),
        fetchAlbums(),
        fetchGenres(),
      ]);
    } catch {}
    await this.load();
  }

  async load() {
    this.loading = true;
    this.error = '';
    try {
  const params: Record<string, any> = {};
  if (this.q?.trim()) params['q'] = this.q.trim();
  if (this.artistId != null) params['artist_id'] = this.artistId;
  if (this.albumId != null) params['album_id'] = this.albumId;
  if (this.genreId != null) params['genre_id'] = this.genreId;
  this.songs = await fetchSongsWithParams(params);
    } catch (e: any) {
      this.error = e?.message || 'Failed to load songs';
    } finally {
      this.loading = false;
    }
  }

  clearFilters() {
    this.q = '';
    this.artistId = null;
    this.albumId = null;
    this.genreId = null;
    this.load();
  }
}
