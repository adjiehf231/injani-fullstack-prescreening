import React from 'react';

export default function DashboardLoading() {
  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6" aria-busy="true" aria-label="Loading SLA Analytics">
      {/* Header Skeleton */}
      <div className="space-y-2 border-b border-slate-200 pb-5">
        <div className="h-7 w-64 bg-slate-200 rounded" />
        <div className="h-4 w-96 bg-slate-100 rounded" />
      </div>

      {/* Filter Bar Skeleton */}
      <div className="h-16 bg-white border border-slate-200 rounded-lg p-4" />

      {/* Metric Cards Skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-24 bg-white border border-slate-200 rounded-lg p-4 space-y-2">
            <div className="h-3 w-20 bg-slate-100 rounded" />
            <div className="h-6 w-12 bg-slate-200 rounded" />
          </div>
        ))}
      </div>

      {/* Charts Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-64 bg-white border border-slate-200 rounded-lg p-5" />
        <div className="h-64 bg-white border border-slate-200 rounded-lg p-5" />
      </div>
    </main>
  );
}
