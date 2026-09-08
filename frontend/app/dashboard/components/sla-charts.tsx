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
      title: 'Active Backlog Queue',
      value: metrics.activePending,
      suffix: '',
      subtitle: 'Steps currently awaiting review',
      status: 'neutral',
      icon: (
        <svg className="w-4 h-4 text-slate-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
        </svg>
      ),
    },
    {
      title: 'Currently Overdue',
      value: metrics.currentlyOverdue,
      suffix: '',
      subtitle: 'Exceeding target SLA window',
      status: metrics.currentlyOverdue > 0 ? 'warning' : 'neutral',
      icon: (
        <svg className="w-4 h-4 text-rose-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      ),
    },
    {
      title: 'Overall Breach Rate',
      value: metrics.overallBreachRatePct,
      suffix: '%',
      subtitle: 'Past 30 days historical window',
      status: 'neutral',
      icon: (
        <svg className="w-4 h-4 text-amber-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
      ),
    },
    {
      title: 'Median Turnaround (P50)',
      value: metrics.medianTurnaroundMinutes,
      suffix: 'm',
      subtitle: 'End-to-end turnaround (~1.9h)',
      status: 'neutral',
      icon: (
        <svg className="w-4 h-4 text-blue-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="10" />
          <polyline points="12 6 12 12 16 14" />
        </svg>
      ),
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c) => (
        <div
          key={c.title}
          className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs space-y-2 hover:border-slate-300 transition-colors"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              {c.title}
            </span>
            {c.icon}
          </div>

          <div className="flex items-baseline gap-1">
            <span
              className={`text-2xl font-bold tracking-tight ${
                c.status === 'warning' ? 'text-rose-600' : 'text-slate-900'
              }`}
            >
              {c.value}
            </span>
            {c.suffix && (
              <span className="text-sm font-semibold text-slate-500">
                {c.suffix}
              </span>
            )}
          </div>

          <p className="text-xs text-slate-500 leading-tight">
            {c.subtitle}
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
  }>;
}) {
  const maxScale = 600; // 10 hours reference scale

  return (
    <div className="space-y-5">
      {/* Visual Legend */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-xs bg-blue-600" aria-hidden="true" />
            <span>P50 Median</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3 h-3 rounded-xs bg-blue-200" aria-hidden="true" />
            <span>P90 Tail Latency</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-0.5 h-3 bg-slate-900" aria-hidden="true" />
            <span>Target SLA</span>
          </div>
        </div>
        <span className="text-[11px] text-slate-500">Scale: 0 &ndash; {maxScale} mins</span>
      </div>

      {/* Step Bars */}
      <div className="space-y-4">
        {steps.map((s) => {
          const isBreached = s.p90Minutes > s.targetSla;
          const p50Width = Math.min((s.p50Minutes / maxScale) * 100, 100);
          const p90Width = Math.min((s.p90Minutes / maxScale) * 100, 100);
          const slaPos = Math.min((s.targetSla / maxScale) * 100, 100);

          return (
            <div key={s.stepType} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="font-semibold text-slate-900">{s.stepType}</span>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-slate-600">
                    P50: <strong>{s.p50Minutes}m</strong> | P90: <strong>{s.p90Minutes}m</strong>
                  </span>
                  <span
                    className={`px-1.5 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wide border ${
                      isBreached
                        ? 'bg-rose-50 text-rose-700 border-rose-200'
                        : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    }`}
                  >
                    {isBreached ? 'Breached' : 'Within SLA'}
                  </span>
                </div>
              </div>

              {/* Progress Bar Container */}
              <div
                className="relative h-6 bg-slate-100 rounded-md overflow-hidden border border-slate-200"
                role="progressbar"
                aria-valuenow={s.p90Minutes}
                aria-valuemin={0}
                aria-valuemax={maxScale}
                aria-label={`${s.stepType} P90 duration`}
              >
                {/* P90 bar */}
                <div
                  className={`absolute top-0 bottom-0 left-0 transition-all ${
                    isBreached ? 'bg-rose-200' : 'bg-blue-200'
                  }`}
                  style={{ width: `${p90Width}%` }}
                />

                {/* P50 bar */}
                <div
                  className={`absolute top-0 bottom-0 left-0 transition-all ${
                    isBreached ? 'bg-rose-500' : 'bg-blue-600'
                  }`}
                  style={{ width: `${p50Width}%` }}
                />

                {/* Target SLA Line */}
                <div
                  className="absolute top-0 bottom-0 w-0.5 bg-slate-900 z-10"
                  style={{ left: `${slaPos}%` }}
                  title={`Target SLA: ${s.targetSla} minutes`}
                />
              </div>

              <div className="flex justify-between items-center text-[11px] text-slate-500">
                <span>Target SLA: {s.targetSla}m</span>
                <span>
                  Breach Frequency: <strong className="text-slate-800">{s.breachRatePct}%</strong>
                </span>
              </div>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-slate-500 bg-slate-50 p-3 rounded-lg border border-slate-200 leading-relaxed">
        <strong>Analyst Note:</strong> Steps where P90 drastically outpaces target SLA (e.g., Finance and Legal)
        represent long-tail approval bottlenecks requiring escalation automation or additional reviewer capacity.
      </p>
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
  }>;
}) {
  const totalQueue = rankings.reduce((acc, r) => acc + r.activeQueue, 0);
  const totalOverdue = rankings.reduce((acc, r) => acc + r.overdueCount, 0);

  return (
    <div className="space-y-3">
      <div className="overflow-x-auto border border-slate-200 rounded-lg">
        <table className="w-full text-left text-xs text-slate-700 divide-y divide-slate-200">
          <thead className="bg-slate-50 text-slate-600 font-semibold uppercase tracking-wider">
            <tr>
              <th scope="col" className="py-3 px-3.5">Department</th>
              <th scope="col" className="py-3 px-3 text-center">Active Queue</th>
              <th scope="col" className="py-3 px-3 text-center">Overdue</th>
              <th scope="col" className="py-3 px-3.5 text-right">Breach Rate</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {rankings.map((d) => (
              <tr key={d.department} className="hover:bg-slate-50/80 transition-colors">
                <td className="py-2.5 px-3.5 font-medium text-slate-900">
                  {d.department}
                </td>
                <td className="py-2.5 px-3 text-center font-mono font-semibold text-slate-800">
                  {d.activeQueue}
                </td>
                <td className="py-2.5 px-3 text-center">
                  {d.overdueCount > 0 ? (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-50 text-rose-700 border border-rose-200">
                      {d.overdueCount} overdue
                    </span>
                  ) : (
                    <span className="text-slate-400 font-mono">0</span>
                  )}
                </td>
                <td className="py-2.5 px-3.5 text-right font-mono font-medium text-slate-900">
                  {d.breachRatePct}%
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot className="bg-slate-50 font-semibold text-slate-900 border-t border-slate-200">
            <tr>
              <td className="py-2.5 px-3.5">Summary Total</td>
              <td className="py-2.5 px-3 text-center font-mono">{totalQueue}</td>
              <td className="py-2.5 px-3 text-center font-mono">
                {totalOverdue > 0 ? (
                  <span className="text-rose-600 font-bold">{totalOverdue} overdue</span>
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

      <p className="text-[11px] text-slate-500 text-right">
        Sorted by overdue approval severity &bull; Query generated by <code>queries_q2_analytics.sql</code>
      </p>
    </div>
  );
}
