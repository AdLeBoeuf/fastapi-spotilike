import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { fetchArtist, fetchArtistSongs, Artist } from '../services/artists.service';

@Component({
  selector: 'app-artist-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
  <section class="container" *ngIf="artist">
    <a routerLink="/artists">← Back to artists</a>
    <header class="header">
      <img *ngIf="artist.avatar" [src]="artist.avatar" width="96" height="96" style="object-fit:cover;border-radius:50%;" />
      <div>
        <h1>{{ artist.name }}</h1>
        <p class="muted" *ngIf="artist.bio">{{ artist.bio }}</p>
      </div>
    </header>
    <h3>Songs</h3>
    <ul *ngIf="songs?.length; else empty">
      <li *ngFor="let s of songs">
        <strong>{{ s.title || 'Untitled' }}</strong>
        <small class="muted"> • durée: {{ s.duration || 'n/a' }}</small>
        <span *ngIf="s.album_id">
          • album:
          <a [routerLink]="['/albums', s.album_id]">{{ s.album_title || ('#' + s.album_id) }}</a>
        </span>
      </li>
    </ul>
    <ng-template #empty><p>No songs for this artist.</p></ng-template>
  </section>
  <section class="container" *ngIf="!artist && !error">
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
export class ArtistDetailComponent implements OnInit {
  artist: Artist | null = null;
  songs: any[] = [];
  error = '';

  constructor(private route: ActivatedRoute) {}

  async ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error = 'Invalid artist id';
      return;
    }
    try {
      this.artist = await fetchArtist(id);
      this.songs = await fetchArtistSongs(id);
    } catch (e: any) {
      this.error = e?.message || 'Failed to load artist';
    }
  }
}
