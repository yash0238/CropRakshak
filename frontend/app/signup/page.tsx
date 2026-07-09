"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowLeft, Loader2, CheckCircle2, AlertTriangle } from "lucide-react";
import { supabase, isSupabaseConfigured } from "@/lib/supabase";

type Status =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "confirm" } // signed up, email confirmation required
  | { kind: "done" } // signed up + session active
  | { kind: "error"; message: string };

export default function SignupPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<Status>({ kind: "idle" });

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!supabase) {
      setStatus({
        kind: "error",
        message:
          "Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY to frontend/.env.local.",
      });
      return;
    }
    if (password.length < 6) {
      setStatus({ kind: "error", message: "Password must be at least 6 characters." });
      return;
    }

    setStatus({ kind: "loading" });
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: { data: { name } },
      });

      if (error) {
        setStatus({ kind: "error", message: error.message });
        return;
      }
      // If a session exists, email confirmation is off -> logged in immediately.
      // Otherwise Supabase sent a confirmation email.
      setStatus(data.session ? { kind: "done" } : { kind: "confirm" });
    } catch (err) {
      setStatus({
        kind: "error",
        message: err instanceof Error ? err.message : "Something went wrong.",
      });
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-12 max-w-md">
        <Link
          href="/"
          className="inline-flex items-center text-green-600 hover:text-green-700 mb-8"
        >
          <ArrowLeft className="w-4 h-4 mr-2" /> Back to home
        </Link>

        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Create your account
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mb-8">
          Start making smarter farm decisions today.
        </p>

        {status.kind === "done" && (
          <div className="feature-card text-center py-10">
            <CheckCircle2 className="w-12 h-12 text-green-600 mx-auto mb-3" />
            <p className="text-green-600 font-semibold mb-2">Account created!</p>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              You&apos;re signed in.
            </p>
            <Link
              href="/dashboard"
              className="text-green-600 hover:text-green-700 font-medium"
            >
              Continue to dashboard →
            </Link>
          </div>
        )}

        {status.kind === "confirm" && (
          <div className="feature-card text-center py-10">
            <CheckCircle2 className="w-12 h-12 text-green-600 mx-auto mb-3" />
            <p className="text-green-600 font-semibold mb-2">Almost there!</p>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              We sent a confirmation link to <strong>{email}</strong>. Click it to
              activate your account, then sign in.
            </p>
            <Link
              href="/dashboard"
              className="text-green-600 hover:text-green-700 font-medium"
            >
              Skip to dashboard →
            </Link>
          </div>
        )}

        {(status.kind === "idle" ||
          status.kind === "loading" ||
          status.kind === "error") && (
          <form onSubmit={handleSubmit} className="feature-card space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 py-2"
              />
              <p className="text-xs text-gray-500 mt-1">At least 6 characters.</p>
            </div>

            {!isSupabaseConfigured && (
              <p className="text-xs text-yellow-600">
                Supabase keys not detected — signup will run in demo mode only.
              </p>
            )}

            {status.kind === "error" && (
              <div
                role="alert"
                className="flex items-start gap-2 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 p-3 text-sm"
              >
                <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                <span>{status.message}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={status.kind === "loading"}
              className="w-full rounded-full bg-green-600 text-white py-3 font-semibold hover:bg-green-700 disabled:opacity-50 inline-flex items-center justify-center gap-2"
            >
              {status.kind === "loading" ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" /> Creating account...
                </>
              ) : (
                "Sign up"
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
