import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { DashboardTiles } from "@/components/DashboardTiles";
import { ThemeToggle } from "@/components/ThemeToggle";

export const metadata = {
  title: "Dashboard - Krishivaani",
  description: "Your farm decision intelligence dashboard",
};

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-hero">
      <div className="container mx-auto px-4 py-12">
        <div className="flex items-center justify-between mb-8">
          <Link
            href="/"
            className="inline-flex items-center text-green-600 hover:text-green-700 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> Back to home
          </Link>
          <ThemeToggle />
        </div>

        <div className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <span className="text-gradient-brand">Dashboard</span>
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Choose a tool to get started with smarter farm decisions.
          </p>
        </div>

        <DashboardTiles />
      </div>
    </div>
  );
}
