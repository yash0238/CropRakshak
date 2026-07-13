"use client";

import Link from "next/link";
import {
  Camera,
  CloudRain,
  Shield,
  MessageCircle,
  FileText,
  BarChart3,
  Mic,
  ArrowRight,
  type LucideIcon,
} from "lucide-react";
import { StaggerGroup, StaggerItem } from "@/components/motion";

interface Tile {
  href: string;
  icon: LucideIcon;
  color: string;
  bg: string;
  bar: string;
  glow: string;
  title: string;
  description: string;
}

const tiles: Tile[] = [
  {
    href: "/dashboard/diagnosis",
    icon: Camera,
    color: "text-green-600",
    bg: "bg-green-50 dark:bg-green-900/20",
    bar: "from-green-500 to-emerald-500",
    glow: "rgba(22,163,74,0.4)",
    title: "Crop Diagnosis",
    description: "Upload a crop photo for instant AI disease detection.",
  },
  {
    href: "/dashboard/risk-score",
    icon: Shield,
    color: "text-orange-600",
    bg: "bg-orange-50 dark:bg-orange-900/20",
    bar: "from-orange-500 to-amber-500",
    glow: "rgba(234,88,12,0.4)",
    title: "Farm Risk Score",
    description: "Real-time risk assessment from 0 to 100.",
  },
  {
    href: "/dashboard/weather",
    icon: CloudRain,
    color: "text-blue-600",
    bg: "bg-blue-50 dark:bg-blue-900/20",
    bar: "from-sky-500 to-blue-500",
    glow: "rgba(37,99,235,0.4)",
    title: "Weather Intelligence",
    description: "7-day forecast and irrigation recommendations.",
  },
  {
    href: "/dashboard/chat",
    icon: MessageCircle,
    color: "text-purple-600",
    bg: "bg-purple-50 dark:bg-purple-900/20",
    bar: "from-purple-500 to-fuchsia-500",
    glow: "rgba(147,51,234,0.4)",
    title: "Ask Krishivaani",
    description: "Multilingual AI assistant for any farming question.",
  },
  {
    href: "/dashboard/voice",
    icon: Mic,
    color: "text-rose-600",
    bg: "bg-rose-50 dark:bg-rose-900/20",
    bar: "from-rose-500 to-pink-500",
    glow: "rgba(225,29,72,0.4)",
    title: "Voice Assistant",
    description: "Speak your question in 5 languages and hear the answer aloud.",
  },
  {
    href: "/dashboard/schemes",
    icon: FileText,
    color: "text-indigo-600",
    bg: "bg-indigo-50 dark:bg-indigo-900/20",
    bar: "from-indigo-500 to-violet-500",
    glow: "rgba(79,70,229,0.4)",
    title: "Government Schemes",
    description: "Find schemes you are eligible for.",
  },
  {
    href: "/dashboard/analytics",
    icon: BarChart3,
    color: "text-teal-600",
    bg: "bg-teal-50 dark:bg-teal-900/20",
    bar: "from-teal-500 to-emerald-500",
    glow: "rgba(13,148,136,0.4)",
    title: "Analytics",
    description: "Disease trends and data-driven insights.",
  },
];

export function DashboardTiles() {
  return (
    <StaggerGroup className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {tiles.map((tile) => {
        const Icon = tile.icon;
        return (
          <StaggerItem key={tile.href}>
            <Link
              href={tile.href}
              style={{ "--glow-color": tile.glow } as React.CSSProperties}
              className="group glow-hover relative block h-full overflow-hidden rounded-2xl border border-border bg-card p-6 shadow-sm transition-all duration-300 hover:-translate-y-1.5"
            >
              {/* top accent bar */}
              <span
                className={`absolute inset-x-0 top-0 h-1.5 origin-left scale-x-0 bg-gradient-to-r ${tile.bar} transition-transform duration-300 group-hover:scale-x-100`}
              />
              <div
                className={`w-14 h-14 rounded-xl ${tile.bg} flex items-center justify-center mb-4 transition-transform duration-300 group-hover:scale-110 group-hover:-rotate-6`}
              >
                <Icon className={`w-7 h-7 ${tile.color}`} />
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white flex items-center gap-2">
                {tile.title}
                <ArrowRight className="w-4 h-4 -translate-x-1 opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:opacity-100 text-brand-600" />
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                {tile.description}
              </p>
            </Link>
          </StaggerItem>
        );
      })}
    </StaggerGroup>
  );
}
