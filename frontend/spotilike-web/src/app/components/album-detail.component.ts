import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { fetchAlbum, fetchAlbumSongs, Album } from '../services/albums.service';

@Component({
  selector: 'app-album-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <section class="container" *ngIf="album">
    <a routerLink="/albums">← Back to albums</a>
    <header class="header">
      <img *ngIf="album.cover" [src]="album.cover" width="128" height="128" style="object-fit:cover;border-radius:12px;" />
      <div>
    <h1>{{ album.title }}</h1>
  <p class="muted">Release: {{ album.release_date || 'n/a' }} • Artiste: <a [routerLink]="['/artists', album.artist_id]">{{ album.artist_name || ('#' + album.artist_id) }}</a></p>
      </div>
    </header>
    <h3>Songs</h3>
    <ul *ngIf="songs?.length; else empty">
      <li *ngFor="let s of songs">
        <strong>{{ s.title || 'Untitled' }}</strong>
        <small class="muted"> • duration: {{ s.duration || 'n/a' }}</small>
      </li>
    </ul>
    <ng-template #empty><p>No songs in this album.</p></ng-template>
  </section>
  <section class="container" *ngIf="!album && !error">
    <p>Loading...</p>
  </section>
  <section class="container" *ngIf="error">
    <p class="error">{{ error }}</p>
  </section>
  `,
  styles: [`
    .container { max-width: 720px; margin: 24px auto; padding: 0 16px; }
    .header { display: flex; align-items: center; gap: 16px; margin: 12px 0 20px; }
    ul { list-style: none; padding: 0; }
    li { padding: 8px 0; border-bottom: 1px solid #eee; }
    .muted { color: #666; }
    .error { color: #b00020; }
  `]
})
export class AlbumDetailComponent implements OnInit {
  album: Album | null = null;
  songs: any[] = [];
  error = '';

  constructor(private route: ActivatedRoute) {}

  async ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error = 'Invalid album id';
      return;
    }
    try {
      this.album = await fetchAlbum(id);
      this.songs = await fetchAlbumSongs(id);
    } catch (e: any) {
      this.error = e?.message || 'Failed to load album';
    }
  }
}
