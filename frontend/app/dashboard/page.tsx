/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q2(b): SLA Analytics Dashboard Architecture - Next.js 14 React Server Component (RSC)
 * 
 * ARCHITECTURE HIGHLIGHTS:
 * 1. React Server Components (RSC): Analytical data is retrieved directly on the server,
 *    eliminating client waterfalls, reducing client JS bundle size to near zero, and keeping DB credentials secure.
 * 2. URL as State (searchParams): Department and date range filters are driven by query params.
 *    This enables browser history navigation, shareable URLs, and eliminates redundant client state stores.
 * 3. Suspense & Streaming: Analytical aggregations stream in via <Suspense>, showing skeletons during network I/O.
 * 4. Sample Data Integrity: Metrics shown represent simulated analytical outputs designed in
 *    database/queries_q2_analytics.sql and database/schema_q2_sla.sql.
 */

import React, { Suspense } from 'react';
import Link from 'next/link';
import { SLAMetricCards, StepBottleneckChart, DepartmentBreachTable } from './components/sla-charts';

interface DashboardPageProps {
  searchParams: Promise<{
    department?: string;
    dateRange?: string;
  }>;
}

// Simulated server-side analytical fetch (in production: direct PostgreSQL connection via pool/ORM)
async function getSLAAnalyticsData(department?: string, dateRange = '30d') {
  // Simulating the analytical query output designed in database/queries_q2_analytics.sql
  const stepMetrics = [
    { stepType: 'Dept Head Review', p50Minutes: 45, p90Minutes: 110, targetSla: 120, breachRatePct: 6.2 },
    { stepType: 'Finance Approval', p50Minutes: 180, p90Minutes: 420, targetSla: 240, breachRatePct: 28.5 },
    { stepType: 'Legal Review', p50Minutes: 210, p90Minutes: 510, targetSla: 300, breachRatePct: 32.1 },
    { stepType: 'Director Sign-off', p50Minutes: 60, p90Minutes: 140, targetSla: 180, breachRatePct: 4.8 },
  ];

  const departmentRankings = [
    { department: 'Finance & Accounting', activeQueue: 18, overdueCount: 5, breachRatePct: 28.5 },
    { department: 'Legal & Compliance', activeQueue: 11, overdueCount: 2, breachRatePct: 24.1 },
    { department: 'Operations', activeQueue: 8, overdueCount: 0, breachRatePct: 5.2 },
    { department: 'Human Resources', activeQueue: 5, overdueCount: 0, breachRatePct: 3.1 },
  ];

  return {
    kpis: {
      activePending: 42,
      currentlyOverdue: 7,
      overallBreachRatePct: 14.8,
      medianTurnaroundMinutes: 115,
    },
    stepMetrics,
    departmentRankings,
    selectedDepartment: department || 'All Departments',
    selectedRange: dateRange,
  };
}

export default async function SLADashboardPage({ searchParams }: DashboardPageProps) {
  const params = await searchParams;
  const currentDept = params.department || 'All Departments';
  const currentRange = params.dateRange || '30d';
  const data = await getSLAAnalyticsData(params.department, currentRange);

  const departments = [
    'All Departments',
    'Finance & Accounting',
    'Legal & Compliance',
    'Operations',
    'Human Resources',
  ];

  const dateRanges = [
    { label: '7 Days', value: '7d' },
    { label: '30 Days', value: '30d' },
    { label: '90 Days', value: '90d' },
  ];

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Breadcrumb & Header */}
      <div className="space-y-3">
        <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs text-slate-500">
          <Link href="/" className="hover:text-slate-900 transition-colors">Overview</Link>
          <span aria-hidden="true">/</span>
          <span className="font-semibold text-slate-800" aria-current="page">SLA Analytics</span>
        </nav>

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-5">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                SLA &amp; Process Bottleneck Analytics
              </h1>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                Sample Analytical Data
              </span>
            </div>
            <p className="text-sm text-slate-600">
              Multi-step workflow turnaround and SLA compliance monitoring across approval departments.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-500">
            <span className="inline-block w-2 h-2 rounded-full bg-emerald-500" aria-hidden="true" />
            <span>React Server Component &bull; Direct DB Query Architecture</span>
          </div>
        </div>
      </div>

      {/* Interactive Filter Bar */}
      <section className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          {/* Department Filter */}
          <div className="flex flex-wrap items-center gap-1.5">
            <span className="font-semibold text-slate-700 mr-1">Department:</span>
            {departments.map((dept) => {
              const isSelected = currentDept === dept;
              const href = dept === 'All Departments'
                ? `/dashboard?dateRange=${currentRange}`
                : `/dashboard?department=${encodeURIComponent(dept)}&dateRange=${currentRange}`;

              return (
                <Link
                  key={dept}
                  href={href}
                  className={`px-2.5 py-1 rounded-md text-xs transition-colors ${
                    isSelected
                      ? 'bg-blue-600 text-white font-semibold shadow-2xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {dept}
                </Link>
              );
            })}
          </div>

          {/* Date Range Filter */}
          <div className="flex items-center gap-1.5">
            <span className="font-semibold text-slate-700 mr-1">Range:</span>
            {dateRanges.map((r) => {
              const isSelected = currentRange === r.value;
              const href = currentDept === 'All Departments'
                ? `/dashboard?dateRange=${r.value}`
                : `/dashboard?department=${encodeURIComponent(currentDept)}&dateRange=${r.value}`;

              return (
                <Link
                  key={r.value}
                  href={href}
                  className={`px-2.5 py-1 rounded-md text-xs transition-colors ${
                    isSelected
                      ? 'bg-slate-900 text-white font-semibold'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {r.label}
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* KPI Overview Cards */}
      <Suspense fallback={<div className="h-28 bg-slate-100 animate-pulse rounded-xl" />}>
        <SLAMetricCards metrics={data.kpis} />
      </Suspense>

      {/* Primary Analytical Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Section 1: Step Duration vs SLA Target */}
        <section className="p-6 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-base font-semibold text-slate-900">
                Step Turnaround vs SLA Target
              </h2>
              <p className="text-xs text-slate-500">
                P50 Median and P90 Tail Latency (Minutes)
              </p>
            </div>
            <span className="text-[11px] font-medium text-slate-400">
              Q2 Metric Visualization
            </span>
          </div>

          <StepBottleneckChart steps={data.stepMetrics} />
        </section>

        {/* Section 2: Department Overdue Backlog & Breach Table */}
        <section className="p-6 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div>
              <h2 className="text-base font-semibold text-slate-900">
                Department Backlog &amp; Breach Severity
              </h2>
              <p className="text-xs text-slate-500">
                Active approval queues and overdue counts
              </p>
            </div>
            <span className="text-[11px] font-medium text-slate-400">
              PostgreSQL Aggregation
            </span>
          </div>

          <DepartmentBreachTable rankings={data.departmentRankings} />
        </section>
      </div>

      {/* Architectural Context Drawer */}
      <section className="p-5 bg-white border border-slate-200 rounded-xl shadow-xs text-xs text-slate-600 space-y-3">
        <h3 className="font-semibold text-slate-900 text-sm">
          Technical Architecture Context (Q2 Implementation)
        </h3>
        <ul className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <li className="space-y-1">
            <strong className="text-slate-800 block">1. React Server Components (RSC)</strong>
            <span>
              All analytical calculations execute on the server. Zero client JavaScript waterfalls and no exposed database credentials.
            </span>
          </li>
          <li className="space-y-1">
            <strong className="text-slate-800 block">2. URL as State (searchParams)</strong>
            <span>
              Filters are driven by URL search params, enabling bookmarking, browser back/forward history, and shareable reports without external state stores.
            </span>
          </li>
          <li className="space-y-1">
            <strong className="text-slate-800 block">3. Relational PostgreSQL Backing</strong>
            <span>
              Backed by generated columns (<code>duration_seconds</code>) and composite indexes detailed in <code>database/queries_q2_analytics.sql</code>.
            </span>
          </li>
        </ul>
      </section>
    </main>
  );
}
