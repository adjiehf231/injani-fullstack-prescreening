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
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="p-4 bg-white border rounded-xl shadow-sm">
        <p className="text-xs font-medium text-gray-500 uppercase">Active Backlog Queue</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">{metrics.activePending}</p>
        <span className="text-xs text-gray-400">Total steps awaiting approval</span>
      </div>

      <div className="p-4 bg-white border rounded-xl shadow-sm">
        <p className="text-xs font-medium text-gray-500 uppercase">Currently Overdue</p>
        <p className="text-2xl font-bold text-red-600 mt-1">{metrics.currentlyOverdue}</p>
        <span className="text-xs text-red-500 font-medium">Violating active SLA right now</span>
      </div>

      <div className="p-4 bg-white border rounded-xl shadow-sm">
        <p className="text-xs font-medium text-gray-500 uppercase">Overall Breach Rate</p>
        <p className="text-2xl font-bold text-amber-600 mt-1">{metrics.overallBreachRatePct}%</p>
        <span className="text-xs text-gray-400">Past 30 days historical</span>
      </div>

      <div className="p-4 bg-white border rounded-xl shadow-sm">
        <p className="text-xs font-medium text-gray-500 uppercase">Median Turnaround (P50)</p>
        <p className="text-2xl font-bold text-blue-600 mt-1">{metrics.medianTurnaroundMinutes}m</p>
        <span className="text-xs text-gray-400">1.9 hours end-to-end median</span>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// 2. Step Bottleneck Chart (P50 vs P90 vs SLA Baseline)
// What it reveals to a business analyst:
// - P50 reflects typical turnaround, while P90 reveals the severe "tail latency".
// - If P90 drastically exceeds target_sla, this specific step is where tasks stall.
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
  return (
    <div className="space-y-4">
      {steps.map((s) => {
        const isBreached = s.p90Minutes > s.targetSla;
        const maxScale = Math.max(...steps.map((x) => x.p90Minutes), 600);
        const p50Width = (s.p50Minutes / maxScale) * 100;
        const p90Width = (s.p90Minutes / maxScale) * 100;
        const slaPos = (s.targetSla / maxScale) * 100;

        return (
          <div key={s.stepType} className="space-y-1">
            <div className="flex justify-between text-xs font-medium">
              <span className="text-gray-800">{s.stepType}</span>
              <span className={isBreached ? 'text-red-600 font-semibold' : 'text-gray-500'}>
                P50: {s.p50Minutes}m | P90: {s.p90Minutes}m (SLA: {s.targetSla}m)
              </span>
            </div>

            {/* Custom bar chart with SLA threshold marker */}
            <div className="relative h-6 bg-gray-100 rounded-md overflow-hidden">
              {/* P90 tail latency bar */}
              <div
                className={`absolute top-0 bottom-0 left-0 ${isBreached ? 'bg-red-200' : 'bg-blue-200'}`}
                style={{ width: `${p90Width}%` }}
              />
              {/* P50 median bar */}
              <div
                className={`absolute top-0 bottom-0 left-0 ${isBreached ? 'bg-red-500' : 'bg-blue-500'}`}
                style={{ width: `${p50Width}%` }}
              />
              {/* SLA Target indicator line */}
              <div
                className="absolute top-0 bottom-0 w-0.5 bg-gray-800 z-10"
                style={{ left: `${slaPos}%` }}
                title={`Target SLA: ${s.targetSla}m`}
              />
            </div>
            <div className="text-[11px] text-gray-500 text-right">
              Breach Rate: <span className="font-medium text-gray-700">{s.breachRatePct}%</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 3. Department Backlog & Breach Table
// What it reveals to a business analyst:
// - Shows whether bottlenecks stem from departmental under-staffing or process complexity.
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
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-xs text-gray-600">
        <thead className="bg-gray-50 text-gray-500 uppercase border-b">
          <tr>
            <th className="py-2.5 px-3">Department</th>
            <th className="py-2.5 px-3 text-center">Active Queue</th>
            <th className="py-2.5 px-3 text-center">Overdue</th>
            <th className="py-2.5 px-3 text-right">Breach Rate</th>
          </tr>
        </thead>
        <tbody className="divide-y">
          {rankings.map((d) => (
            <tr key={d.department} className="hover:bg-gray-50">
              <td className="py-2.5 px-3 font-medium text-gray-900">{d.department}</td>
              <td className="py-2.5 px-3 text-center font-semibold">{d.activeQueue}</td>
              <td className="py-2.5 px-3 text-center">
                {d.overdueCount > 0 ? (
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-red-100 text-red-800">
                    {d.overdueCount} overdue
                  </span>
                ) : (
                  <span className="text-gray-400">0</span>
                )}
              </td>
              <td className="py-2.5 px-3 text-right font-medium text-gray-800">
                {d.breachRatePct}%
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
