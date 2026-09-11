/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q2(c): SLA Analytics Dashboard Visualizations & Business Insights Components
 */

import React from 'react';

// ---------------------------------------------------------------------------
// 1. KPI Overview Cards
// ---------------------------------------------------------------------------
export function SLAMetricCards({
  metrics,
}: {
  metrics: {
    activePending: number;
    currentlyOverdue: number;
    overallBreachRatePct: number;
    medianTurnaroundMinutes: number;
  };
}) {
  const cards = [
    {
      label: 'Active backlog',
      value: metrics.activePending,
      suffix: '',
      detail: 'Awaiting completion across steps',
      badge: null,
    },
    {
      label: 'Currently overdue',
      value: metrics.currentlyOverdue,
      suffix: '',
      detail: 'Violating target SLA window',
      badge: metrics.currentlyOverdue > 0 ? { text: 'Attention', type: 'warning' as const } : { text: 'Clear', type: 'neutral' as const },
    },
    {
      label: 'Overall breach rate',
      value: metrics.overallBreachRatePct,
      suffix: '%',
      detail: 'Historical completion window',
      badge: null,
    },
    {
      label: 'Median turnaround',
      value: metrics.medianTurnaroundMinutes,
      suffix: 'm',
      detail: 'P50 end-to-end processing time',
      badge: null,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">
      {cards.map((c) => (
        <div
          key={c.label}
          className="p-4 bg-white border border-slate-200 rounded-lg space-y-1.5"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-500">
              {c.label}
            </span>
            {c.badge && (
              <span
                className={`text-[10px] font-medium px-1.5 py-0.5 rounded border ${
                  c.badge.type === 'warning'
                    ? 'bg-rose-50 text-rose-700 border-rose-200'
                    : 'bg-slate-100 text-slate-600 border-slate-200'
                }`}
              >
                {c.badge.text}
              </span>
            )}
          </div>

          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-semibold tracking-tight text-slate-900 tabular-nums">
              {c.value}
            </span>
            {c.suffix && (
              <span className="text-sm font-medium text-slate-500">
                {c.suffix}
              </span>
            )}
          </div>

          <p className="text-xs text-slate-500">
            {c.detail}
          </p>
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 2. Step Bottleneck Chart (P50 vs P90 vs SLA Baseline)
// ---------------------------------------------------------------------------
export function StepBottleneckChart({
  steps,
}: {
  steps: Array<{
    stepType: string;
    p50Minutes: number;
    p90Minutes: number;
    targetSla: number;
    breachRatePct: number;
    totalCount: number;
  }>;
}) {
  if (steps.length === 0) {
    return (
      <div className="p-8 text-center bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-500">
        No step turnaround records match the selected filters.
      </div>
    );
  }

  // Calculation moved outside .map() loop for performance and clarity
  const calculatedMax = Math.max(...steps.map((x) => Math.max(x.p90Minutes, x.targetSla)), 300);
  const maxScale = Math.ceil(calculatedMax / 60) * 60; // Round up to nearest hour boundary

  return (
    <div className="space-y-4">
      {/* Legend */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-md text-xs text-slate-600">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-xs bg-slate-800" aria-hidden="true" />
            <span>Median (P50)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-xs bg-blue-200" aria-hidden="true" />
            <span>Tail (P90)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-0.5 h-2.5 bg-rose-600" aria-hidden="true" />
            <span>SLA Target</span>
          </div>
        </div>
        <span className="text-[11px] text-slate-400">Scale: 0 &ndash; {maxScale}m</span>
      </div>

      {/* Step Rows */}
      <div className="space-y-4">
        {steps.map((s) => {
          const isBreached = s.p90Minutes > s.targetSla;
          const p50Width = maxScale > 0 ? Math.min((s.p50Minutes / maxScale) * 100, 100) : 0;
          const p90Width = maxScale > 0 ? Math.min((s.p90Minutes / maxScale) * 100, 100) : 0;
          const slaPos = maxScale > 0 ? Math.min((s.targetSla / maxScale) * 100, 100) : 0;

          return (
            <div key={s.stepType} className="space-y-1.5">
              {/* Responsive title and metrics layout: wraps gracefully on mobile without crushing */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-900">{s.stepType}</span>
                  {s.totalCount > 0 && (
                    <span className="text-[11px] text-slate-400 font-mono">({s.totalCount} runs)</span>
                  )}
                </div>

                <div className="flex flex-wrap items-center gap-2 text-slate-600">
                  <span className="tabular-nums font-mono text-[11px]">
                    P50: <strong>{s.p50Minutes}m</strong> | P90: <strong>{s.p90Minutes}m</strong> | SLA: {s.targetSla}m
                  </span>
                  <span
                    className={`text-[10px] font-medium px-1.5 py-0.2 rounded border ${
                      isBreached
                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                        : 'bg-slate-100 text-slate-700 border-slate-200'
                    }`}
                  >
                    {isBreached ? `Breach ${s.breachRatePct}%` : 'Within SLA'}
                  </span>
                </div>
              </div>

              {/* Progress bar with SLA marker */}
              <div
                className="relative h-5 bg-slate-100 rounded overflow-hidden border border-slate-200"
                role="progressbar"
                aria-valuenow={s.p90Minutes}
                aria-valuemin={0}
                aria-valuemax={maxScale}
                aria-label={`${s.stepType} turnaround percentiles`}
              >
                {/* P90 tail duration bar */}
                <div
                  className={`absolute top-0 bottom-0 left-0 transition-all ${
                    isBreached ? 'bg-rose-100' : 'bg-blue-200'
                  }`}
                  style={{ width: `${p90Width}%` }}
                />

                {/* P50 median bar */}
                <div
                  className={`absolute top-0 bottom-0 left-0 transition-all ${
                    isBreached ? 'bg-rose-400' : 'bg-slate-800'
                  }`}
                  style={{ width: `${p50Width}%` }}
                />

                {/* SLA target vertical line */}
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-rose-600 z-10"
                  style={{ left: `${slaPos}%` }}
                  title={`Target SLA: ${s.targetSla}m`}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// 3. Department Backlog & Breach Table
// ---------------------------------------------------------------------------
export function DepartmentBreachTable({
  rankings,
}: {
  rankings: Array<{
    department: string;
    activeQueue: number;
    overdueCount: number;
    breachRatePct: number;
    totalCount: number;
  }>;
}) {
  if (rankings.length === 0) {
    return (
      <div className="p-8 text-center bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-500">
        No department records match the selected filters.
      </div>
    );
  }

  const totalQueue = rankings.reduce((acc, r) => acc + r.activeQueue, 0);
  const totalOverdue = rankings.reduce((acc, r) => acc + r.overdueCount, 0);

  return (
    <div className="overflow-x-auto border border-slate-200 rounded-lg">
      <table className="w-full text-left text-sm text-slate-700 divide-y divide-slate-200">
        <caption className="sr-only">
          Department workflow backlog queues, overdue counts, and SLA breach rates
        </caption>
        <thead className="bg-slate-50 text-xs text-slate-600 font-semibold uppercase tracking-wider">
          <tr>
            <th scope="col" className="py-2.5 px-3">Department</th>
            <th scope="col" className="py-2.5 px-3 text-center">Active Queue</th>
            <th scope="col" className="py-2.5 px-3 text-center">Overdue</th>
            <th scope="col" className="py-2.5 px-3.5 text-right">Breach Rate</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 bg-white">
          {rankings.map((d) => (
            <tr key={d.department} className="hover:bg-slate-50/70 transition-colors">
              <td className="py-2.5 px-3 font-medium text-slate-900">
                {d.department}
              </td>
              <td className="py-2.5 px-3 text-center font-mono tabular-nums text-slate-800">
                {d.activeQueue}
              </td>
              <td className="py-2.5 px-3 text-center">
                {d.overdueCount > 0 ? (
                  <span className="inline-block px-1.5 py-0.5 rounded text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200 tabular-nums">
                    {d.overdueCount} overdue
                  </span>
                ) : (
                  <span className="text-slate-400 font-mono tabular-nums">0</span>
                )}
              </td>
              <td className="py-2.5 px-3.5 text-right font-mono tabular-nums text-slate-900">
                {d.breachRatePct}%
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot className="bg-slate-50 text-xs font-semibold text-slate-900 border-t border-slate-200">
          <tr>
            <td className="py-2.5 px-3">Summary Total</td>
            <td className="py-2.5 px-3 text-center font-mono tabular-nums">{totalQueue}</td>
            <td className="py-2.5 px-3 text-center font-mono tabular-nums">
              {totalOverdue > 0 ? (
                <span className="text-rose-700 font-bold">{totalOverdue} overdue</span>
              ) : (
                '0'
              )}
            </td>
            <td className="py-2.5 px-3.5 text-right font-mono text-slate-500">
              &mdash;
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  );
}
