"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ArrowRight,
  Camera,
  CloudRain,
  Shield,
  MessageCircle,
  FileText,
  BarChart3,
  Sparkles,
  Cpu,
  Database,
  LineChart,
  Boxes,
  Layers,
  Check,
  Globe,
} from "lucide-react";
import { COPY, LANGS, type Locale, type Item } from "@/lib/landing-i18n";
import { ThemeToggle } from "@/components/ThemeToggle";
import {
  Reveal,
  StaggerGroup,
  StaggerItem,
  CountUp,
  motion,
} from "@/components/motion";

const FEATURE_META = [
  { icon: Camera, color: "text-green-600", bg: "bg-green-50 dark:bg-green-900/20" },
  { icon: Shield, color: "text-orange-600", bg: "bg-orange-50 dark:bg-orange-900/20" },
  { icon: CloudRain, color: "text-blue-600", bg: "bg-blue-50 dark:bg-blue-900/20" },
  { icon: MessageCircle, color: "text-purple-600", bg: "bg-purple-50 dark:bg-purple-900/20" },
  { icon: FileText, color: "text-indigo-600", bg: "bg-indigo-50 dark:bg-indigo-900/20" },
  { icon: BarChart3, color: "text-teal-600", bg: "bg-teal-50 dark:bg-teal-900/20" },
];

const TECH_META = [Sparkles, Boxes, Cpu, Database, LineChart, Layers];

const STAT_VALUES = ["500K", "22.58×", "3", "5"];

const SOLUTION_STATUS: ("Live" | "Roadmap")[] = ["Live", "Live", "Live", "Roadmap"];

export default function HomePage() {
  const [locale, setLocale] = useState<Locale>("en");

  // Restore the visitor's previously chosen language.
  useEffect(() => {
    const saved = localStorage.getItem("krisisar-lang") as Locale | null;
    if (saved && LANGS.some((l) => l.code === saved)) setLocale(saved);
  }, []);

  function changeLang(code: Locale) {
    setLocale(code);
    localStorage.setItem("krisisar-lang", code);
  }

  const t = COPY[locale];

  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-white">
      {/* ── Sticky header ── */}
      <header className="sticky top-0 z-50 backdrop-blur-md bg-white/80 dark:bg-gray-950/80 border-b border-gray-200/70 dark:border-gray-800">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <span className="font-bold text-lg flex items-center gap-2">
            <span className="text-2xl">🌾</span> KrisiSar AI
          </span>

          <div className="flex items-center gap-3">
            <LanguageSelector locale={locale} onChange={changeLang} />
            <ThemeToggle />
            <Link
              href="/dashboard"
              className="hidden sm:inline-flex items-center rounded-full bg-gradient-brand text-white px-5 py-2 text-sm font-semibold shadow-md transition-transform hover:scale-105"
            >
              {t.getStarted}
            </Link>
          </div>
        </div>
      </header>

      {/* ── Hero ── */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-green-50 via-white to-white dark:from-green-950/30 dark:via-gray-950 dark:to-gray-950" />
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-green-400/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-32 -left-24 w-96 h-96 bg-emerald-400/10 rounded-full blur-3xl" />

        <div className="relative container mx-auto px-4 pt-16 pb-20 text-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/30 px-4 py-1.5 text-sm font-medium text-green-700 dark:text-green-300 mb-6">
            <Sparkles className="w-4 h-4" /> {t.eyebrow}
          </span>

          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-5">
            🌾 KrisiSar AI
          </h1>
          <p className="text-2xl md:text-3xl font-semibold text-green-600 dark:text-green-400 mb-4">
            {t.tagline}
          </p>
          <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto mb-8">
            {t.subtitle}
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10">
            <Link
              href="/dashboard"
              className="farmer-button bg-green-600 text-white hover:bg-green-700 inline-flex items-center justify-center"
            >
              {t.getStarted} <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link
              href="/demo"
              className="farmer-button bg-white dark:bg-gray-900 text-green-600 border-2 border-green-600 hover:bg-green-50 dark:hover:bg-gray-800 inline-flex items-center justify-center"
            >
              {t.watchDemo}
            </Link>
          </div>

          {/* Clickable language pills */}
          <div className="flex flex-wrap gap-2 justify-center mb-14">
            {LANGS.map((l) => {
              const active = l.code === locale;
              return (
                <button
                  key={l.code}
                  onClick={() => changeLang(l.code)}
                  aria-pressed={active}
                  className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${
                    active
                      ? "bg-green-600 text-white border-green-600 shadow-md scale-105"
                      : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700 hover:border-green-400 hover:text-green-600"
                  }`}
                >
                  {l.flag} {l.label}
                </button>
              );
            })}
          </div>

          {/* Stats band */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {STAT_VALUES.map((value, i) => (
              <div
                key={i}
                className="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-5 shadow-sm"
              >
                <div className="text-3xl font-extrabold text-green-600 dark:text-green-400">
                  {value}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  {t.statLabels[i]}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-14">
          {t.featuresHeading}
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {t.features.map((f: Item, i: number) => {
            const meta = FEATURE_META[i];
            const Icon = meta.icon;
            return (
              <div
                key={i}
                className="group rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all"
              >
                <div
                  className={`w-14 h-14 rounded-xl ${meta.bg} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
                >
                  <Icon className={`w-7 h-7 ${meta.color}`} />
                </div>
                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{f.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── Problem ── */}
      <section className="bg-red-50/60 dark:bg-red-950/20 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-red-700 dark:text-red-400">
            {t.problemHeading}
          </h2>
          <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-5">
            {t.problems.map((p: Item, i: number) => (
              <div
                key={i}
                className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-sm border-l-4 border-red-400"
              >
                <h3 className="font-bold text-lg mb-2 text-red-600 dark:text-red-400">
                  ❌ {p.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Solution ── */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-green-700 dark:text-green-400">
            {t.solutionHeading}
          </h2>
          <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-5">
            {t.solutions.map((s: Item, i: number) => {
              const isLive = SOLUTION_STATUS[i] === "Live";
              return (
                <div
                  key={i}
                  className="bg-green-50 dark:bg-green-900/20 rounded-xl p-6 shadow-sm border-l-4 border-green-500"
                >
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <h3 className="font-bold text-lg text-green-700 dark:text-green-400">
                      {isLive ? "✅ " : ""}
                      {s.title}
                    </h3>
                    <span
                      className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                        isLive
                          ? "bg-green-600 text-white"
                          : "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300"
                      }`}
                    >
                      {isLive ? t.live : t.comingSoon}
                    </span>
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">{s.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── Technology ── */}
      <section className="bg-gray-50 dark:bg-gray-900 py-20">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-14">
            {t.techHeading}
          </h2>
          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {t.tech.map((tech: Item, i: number) => {
              const Icon = TECH_META[i];
              return (
                <div
                  key={i}
                  className="rounded-2xl bg-white dark:bg-gray-950 p-6 shadow-sm border border-gray-200 dark:border-gray-800 hover:border-green-400 transition-colors"
                >
                  <div className="w-11 h-11 rounded-lg bg-green-50 dark:bg-green-900/30 flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-green-600 dark:text-green-400" />
                  </div>
                  <h3 className="font-bold text-lg mb-1">{tech.title}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    {tech.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-green-600 to-emerald-700 px-6 py-16 text-center text-white shadow-xl">
            <div className="absolute -top-16 -right-10 w-64 h-64 bg-white/10 rounded-full blur-2xl" />
            <h2 className="relative text-3xl md:text-5xl font-bold mb-4">
              {t.ctaHeading}
            </h2>
            <p className="relative text-lg text-green-50 mb-8 max-w-2xl mx-auto">
              {t.ctaSubtitle}
            </p>
            <Link
              href="/signup"
              className="relative farmer-button bg-white text-green-700 hover:bg-green-50 inline-flex items-center"
            >
              {t.ctaButton} <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="bg-gray-950 text-white py-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-lg mb-3 flex items-center justify-center gap-2">
            <span>🌾</span> {t.footerTagline}
          </p>
          <p className="text-gray-400 text-sm">{t.footerPowered}</p>
          <div className="mt-6 flex gap-6 justify-center text-sm">
            <Link href="/docs" className="hover:text-green-400 inline-flex items-center gap-1">
              <FileText className="w-4 h-4" /> {t.docs}
            </Link>
            <Link
              href="https://github.com/Ritik-Gupta8/KrisiSar-AI"
              className="hover:text-green-400"
            >
              GitHub
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}

/** Compact language dropdown for the header. */
function LanguageSelector({
  locale,
  onChange,
}: {
  locale: Locale;
  onChange: (l: Locale) => void;
}) {
  const [open, setOpen] = useState(false);
  const current = LANGS.find((l) => l.code === locale) ?? LANGS[0];

  return (
    <div className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className="inline-flex items-center gap-1.5 rounded-full border border-gray-200 dark:border-gray-700 px-3 py-2 text-sm font-medium hover:border-green-400 transition-colors"
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <Globe className="w-4 h-4" />
        <span>{current.flag}</span>
        <span>{current.label}</span>
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <ul
            role="listbox"
            className="absolute right-0 mt-2 z-50 w-40 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 shadow-lg overflow-hidden"
          >
            {LANGS.map((l) => {
              const active = l.code === locale;
              return (
                <li key={l.code}>
                  <button
                    onClick={() => {
                      onChange(l.code);
                      setOpen(false);
                    }}
                    className={`w-full flex items-center justify-between px-4 py-2.5 text-sm hover:bg-green-50 dark:hover:bg-green-900/20 ${
                      active ? "text-green-600 font-semibold" : ""
                    }`}
                  >
                    <span>
                      {l.flag} {l.label}
                    </span>
                    {active && <Check className="w-4 h-4" />}
                  </button>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
}
