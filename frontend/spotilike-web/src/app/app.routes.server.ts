import { RenderMode, ServerRoute } from '@angular/ssr';

// Prerender only static routes; use Server mode for dynamic parameter routes
export const serverRoutes: ServerRoute[] = [
  { path: '', renderMode: RenderMode.Prerender },
  { path: 'login', renderMode: RenderMode.Prerender },
  { path: 'signup', renderMode: RenderMode.Prerender },
  { path: 'artists', renderMode: RenderMode.Prerender },
  { path: 'albums', renderMode: RenderMode.Prerender },
  { path: 'songs', renderMode: RenderMode.Prerender },

  // Parameterized routes cannot be prerendered without getPrerenderParams
  { path: 'artists/:id', renderMode: RenderMode.Server },
  { path: 'albums/:id', renderMode: RenderMode.Server },

  // Fallback
  { path: '**', renderMode: RenderMode.Server },
];
