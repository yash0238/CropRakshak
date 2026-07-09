import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import type { ReactNode } from "react";

interface FeatureShellProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function FeatureShell({ title, description, children }: FeatureShellProps) {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12 max-w-4xl">
        <Link
          href="/dashboard"
          className="inline-flex items-center text-green-600 hover:text-green-700 mb-8"
        >
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to dashboard
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {title}
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
        This feature connects to the KrisiSar AI backend.
      </p>
      <p className="text-sm text-gray-500 dark:text-gray-400">{note}</p>
    </div>
  );
}
