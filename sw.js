/* Полиглот — офлайн-кэш (PWA).
   ВАЖНО: при каждом изменении index.html повышать VERSION,
   иначе телефоны продолжат показывать старую версию. */
const VERSION = "v12";
const CACHE = "polyglot-cache-" + VERSION;
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./icon-maskable-512.png"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) { return c.addAll(ASSETS); })
      .then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; })
        .map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(function (hit) {
      if (hit) return hit;
      return fetch(e.request).then(function (res) {
        try {
          var u = new URL(e.request.url);
          var cacheable = res.ok && (u.origin === location.origin
            || u.hostname.indexOf("jsdelivr.net") >= 0
            || u.hostname.indexOf("cdnjs.cloudflare.com") >= 0
            || u.hostname.indexOf("tessdata.projectnaptha.com") >= 0);
          if (cacheable) {
            var copy = res.clone();
            caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
          }
        } catch (err) {}
        return res;
      }).catch(function () {
        return caches.match("./index.html");
      });
    })
  );
});

