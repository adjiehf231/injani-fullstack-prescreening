'use client';

import React from 'react';
import Link from 'next/link';

export default function DashboardError({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center space-y-4">
      <div className="max-w-md mx-auto p-6 bg-white border border-slate-200 rounded-lg space-y-3">
        <h1 className="text-base font-semibold text-slate-900">
          Unable to load SLA analytics.
        </h1>
        <p className="text-xs text-slate-600">
          Please try again or reset the filter parameters.
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            onClick={() => reset()}
            className="px-3.5 py-1.5 text-xs font-medium text-white bg-slate-900 hover:bg-slate-800 rounded transition-colors"
          >
            Retry
          </button>
          <Link
            href="/dashboard"
            className="px-3.5 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded transition-colors"
          >
            Reset Filters
          </Link>
        </div>
      </div>
    </main>
  );
}
