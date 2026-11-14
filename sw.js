const CACHE_NAME = 'p04-slides-pwa-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './slides/P04_image_processing_eda.html',
  './slides/assets/P04/icon-192.png',
  './slides/assets/P04/icon-512.png',
  './slides/assets/P04/01_opening_character.png',
  './slides/assets/P04/04_grayscale_vs_rgb.png',
  './slides/assets/P04/05_rgb_channels.png',
  './slides/assets/P04/06_resize_aspect_ratio.png',
  './slides/assets/P04/07_histogram_brightness_contrast.png',
  './slides/assets/P04/07b_brightness_contrast_box.png',
  './slides/assets/P04/08_canny_edge_density.png',
  './slides/assets/P04/09_exif_trap.png',
  './slides/assets/P04/human_vision_realistic.jpg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
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
