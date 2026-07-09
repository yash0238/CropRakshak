import type { NextConfig } from "next";
import withPWA from "next-pwa";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  images: {
    domains: [
      "localhost",
      "supabase.co",
      "firebasestorage.googleapis.com",
      "openweathermap.org",
    ],
    formats: ["image/avif", "image/webp"],
  },
  experimental: {
    optimizePackageImports: ["lucide-react", "recharts"],
  },
  // i18n configuration for next-intl
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-Frame-Options",
            value: "DENY",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
        ],
      },
    ];
  },
};

// PWA configuration.
// PWA is now OPT-IN: it stays off everywhere (dev + production) unless you
// explicitly set NEXT_PUBLIC_ENABLE_PWA=true. This avoids the service-worker
// caching surprises during development and demos. Turn it on later once the
// app is stable if you want installable/offline behaviour.
const enablePWA = process.env.NEXT_PUBLIC_ENABLE_PWA === "true";

const pwaConfig = withPWA({
  dest: "public",
  disable: !enablePWA,
  register: true,
  skipWaiting: true,
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/api\.open-meteo\.com\/.*/i,
      handler: "NetworkFirst",
      options: {
        cacheName: "weather-cache",
        expiration: {
          maxEntries: 32,
          maxAgeSeconds: 3600, // 1 hour
        },
      },
    },
    {
      urlPattern: /^https:\/\/.*\.supabase\.co\/.*/i,
      handler: "NetworkFirst",
      options: {
        cacheName: "supabase-cache",
        expiration: {
          maxEntries: 64,
          maxAgeSeconds: 86400, // 24 hours
        },
      },
    },
  ],
});

export default pwaConfig(nextConfig);
