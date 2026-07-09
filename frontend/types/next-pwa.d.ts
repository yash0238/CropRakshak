/**
 * next-pwa ships no bundled TypeScript types.
 * Minimal declaration to satisfy strict type-checking.
 * See: https://github.com/shadowwalker/next-pwa
 */
declare module "next-pwa" {
  import type { NextConfig } from "next";

  interface RuntimeCachingEntry {
    urlPattern: RegExp | string;
    handler: string;
    options?: {
      cacheName?: string;
      expiration?: {
        maxEntries?: number;
        maxAgeSeconds?: number;
      };
      [key: string]: unknown;
    };
  }

  interface PWAOptions {
    dest?: string;
    disable?: boolean;
    register?: boolean;
    skipWaiting?: boolean;
    runtimeCaching?: RuntimeCachingEntry[];
    [key: string]: unknown;
  }

  export default function withPWA(
    options?: PWAOptions
  ): (nextConfig: NextConfig) => NextConfig;
}
