import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import type { ReactNode } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";

interface FeatureShellProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function FeatureShell({ title, description, children }: FeatureShellProps) {
  return (
    <div className="min-h-screen bg-gradient-hero">
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <div className="flex items-center justify-between mb-8">
          <Link
            href="/dashboard"
            className="inline-flex items-center text-green-600 hover:text-green-700 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to dashboard
          </Link>
          <ThemeToggle />
        </div>

        <div className="mb-8 animate-slide-up">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            <span className="text-gradient-brand">{title}</span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">{description}</p>
        </div>

        {children}
      </div>
    </div>
  );
}

export function ComingSoon({ note }: { note: string }) {
  return (
    <div className="feature-card border-2 border-dashed border-gray-300 dark:border-gray-700 text-center py-12">
      <p className="text-gray-600 dark:text-gray-300 mb-2">
        This feature connects to the Krishivaani backend.
      </p>
      <p className="text-sm text-gray-500 dark:text-gray-400">{note}</p>
    </div>
  );
}
