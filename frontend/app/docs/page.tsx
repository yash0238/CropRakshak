import Link from "next/link";
import { ArrowLeft, BookOpen, Code2, Rocket } from "lucide-react";

export const metadata = { title: "Documentation - KrisiSar AI" };

const docs = [
  {
    icon: BookOpen,
    title: "Architecture",
    description: "System design, multi-agent AI, data pipeline, and GPU acceleration.",
    file: "docs/ARCHITECTURE.md",
  },
  {
    icon: Code2,
    title: "Project Overview",
    description: "Features, tech stack, and how the data pipeline fits together.",
    file: "README.md",
  },
  {
    icon: Rocket,
    title: "Live API",
    description: "Interactive FastAPI docs (Swagger UI) at /docs on the backend.",
    file: "backend: /docs",
  },
];

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12 max-w-3xl">
        <Link
          href="/"
          className="inline-flex items-center text-green-600 hover:text-green-700 mb-8"
        >
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to home
        </Link>

        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Documentation
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          Full documentation lives in the <code>/docs</code> folder of the
          repository.
        </p>

        <div className="space-y-4">
          {docs.map((doc) => {
            const Icon = doc.icon;
            return (
              <div key={doc.title} className="feature-card flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-green-50 dark:bg-green-900/20 flex items-center justify-center shrink-0">
                  <Icon className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    {doc.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    {doc.description}
                  </p>
                  <code className="text-sm text-green-600">{doc.file}</code>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
