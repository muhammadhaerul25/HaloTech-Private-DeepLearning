const CACHE_NAME = 'dl-course-pwa-v16';
const PRECACHE_ASSETS = [
  './',
  './index.html',
  './sessions.json',
  './manifest.webmanifest',
  './materials/P01/P01_understanding_images_processing_eda.html',
  './materials/P01/assets/P01/icon-192.png',
  './materials/P01/assets/P01/icon-512.png',
  './materials/P02/p02_teori_neural_network.html',
  './materials/P03/P03_arsitektur_neural_network.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isDynamic = url.pathname.endsWith('.html') ||
                    url.pathname.endsWith('.json') ||
                    url.pathname === '/' ||
                    /^\/p0?[1-8]$/i.test(url.pathname);

  if (isDynamic) {
    // Network-first for portal, session manifest, and slide HTML so new P02-P08 updates show immediately
    event.respondWith(
      fetch(event.request)
        .then((resp) => {
          if (resp && resp.status === 200 && resp.type === 'basic') {
            const copy = resp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return resp;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Stale-while-revalidate for static assets (images, icons, etc.)
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const fetched = fetch(event.request)
        .then((resp) => {
          if (resp && resp.status === 200 && resp.type === 'basic') {
            const copy = resp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return resp;
        })
        .catch(() => cached);
      return cached || fetched;
    })
  );
});
