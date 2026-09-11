/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q2: SLA Analytics Dashboard - Next.js 14 React Server Component (RSC)
 * 
 * ARCHITECTURE OVERVIEW:
 * 1. React Server Component: Runs directly on the server to compute analytical aggregations,
 *    eliminating client waterfalls and keeping client JS minimal.
 * 2. URL as State (searchParams): Department, step type, and date range filters are driven by
 *    standard GET query params via a native HTML form. This provides shareable URLs,
 *    browser history navigation, and zero client state overhead.
 * 3. Deterministic Assessment Dataset: Aggregations are calculated dynamically from a structured
 *    sample workflow dataset (frontend/lib/sla-data.ts) matching the PostgreSQL schema
 *    defined in database/schema_q2_sla.sql and queries_q2_analytics.sql.
 */

import React, { Suspense } from 'react';
import Link from 'next/link';
import {
  getFilteredSLAAnalytics,
  DEPARTMENTS,
  STEP_TYPES,
  DATE_RANGES,
} from '@/lib/sla-data';
import {
  SLAMetricCards,
  StepBottleneckChart,
  DepartmentBreachTable,
} from './components/sla-charts';

interface DashboardPageProps {
  searchParams: Promise<{
    department?: string;
    stepType?: string;
    dateRange?: string;
  }>;
}

export default async function SLADashboardPage({ searchParams }: DashboardPageProps) {
  const params = await searchParams;
  const currentDept = params.department || 'All Departments';
  const currentStep = params.stepType || 'All Steps';
  const currentRange = params.dateRange || '30d';

  const data = getFilteredSLAAnalytics({
    department: currentDept,
    stepType: currentStep,
    dateRange: currentRange,
  });

  const isFiltered = currentDept !== 'All Departments' || currentStep !== 'All Steps' || currentRange !== '30d';

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header & Truthful Context */}
      <div className="space-y-2 border-b border-slate-200 pb-5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-slate-900">
              SLA &amp; Process Bottleneck Analytics
            </h1>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
              Sample Data
            </span>
          </div>

          <span className="text-xs text-slate-500 font-mono">
            Next.js 14 Server Component
          </span>
        </div>

        <p className="text-sm text-slate-600">
          Sample multi-step workflow turnaround and SLA compliance analysis.
        </p>
      </div>

      {/* URL-driven Filter Form */}
      <section aria-label="Dashboard Filters" className="p-4 bg-white border border-slate-200 rounded-lg">
        <form method="get" action="/dashboard" className="flex flex-wrap items-end gap-3 text-xs">
          {/* Department Select */}
          <div className="flex flex-col gap-1 min-w-[160px]">
            <label htmlFor="filter-department" className="font-medium text-slate-700">
              Department
            </label>
            <select
              id="filter-department"
              name="department"
              defaultValue={currentDept}
              className="h-9 px-2.5 bg-white border border-slate-300 rounded text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900"
            >
              {DEPARTMENTS.map((dept) => (
                <option key={dept} value={dept}>
                  {dept}
                </option>
              ))}
            </select>
          </div>

          {/* Step Type Select */}
          <div className="flex flex-col gap-1 min-w-[160px]">
            <label htmlFor="filter-stepType" className="font-medium text-slate-700">
              Step Type
            </label>
            <select
              id="filter-stepType"
              name="stepType"
              defaultValue={currentStep}
              className="h-9 px-2.5 bg-white border border-slate-300 rounded text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900"
            >
              {STEP_TYPES.map((step) => (
                <option key={step} value={step}>
                  {step}
                </option>
              ))}
            </select>
          </div>

          {/* Period Select */}
          <div className="flex flex-col gap-1 min-w-[130px]">
            <label htmlFor="filter-dateRange" className="font-medium text-slate-700">
              Period
            </label>
            <select
              id="filter-dateRange"
              name="dateRange"
              defaultValue={currentRange}
              className="h-9 px-2.5 bg-white border border-slate-300 rounded text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900"
            >
              {DATE_RANGES.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-2 pt-1 sm:pt-0">
            <button
              type="submit"
              className="h-9 px-3.5 bg-slate-900 hover:bg-slate-800 text-white font-medium rounded text-xs transition-colors"
            >
              Apply Filters
            </button>

            {isFiltered && (
              <Link
                href="/dashboard"
                className="h-9 px-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded text-xs flex items-center transition-colors"
              >
                Reset
              </Link>
            )}
          </div>

          <div className="ml-auto hidden sm:flex items-center text-xs text-slate-500 font-mono">
            <span>{data.totalRecordCount} matching records</span>
          </div>
        </form>
      </section>

      {/* Empty State vs Analytical Data */}
      {data.totalRecordCount === 0 ? (
        <div className="p-12 text-center bg-white border border-slate-200 rounded-lg space-y-3">
          <p className="text-base font-semibold text-slate-900">
            No sample workflow records match these filters.
          </p>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Try selecting another department, step type, or expanding the historical period window.
          </p>
          <div className="pt-2">
            <Link
              href="/dashboard"
              className="inline-flex items-center px-3.5 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded transition-colors"
            >
              Reset to All Records
            </Link>
          </div>
        </div>
      ) : (
        <>
          {/* KPI Cards */}
          <Suspense fallback={<div className="h-24 bg-slate-100 animate-pulse rounded-lg" />}>
            <SLAMetricCards metrics={data.kpis} />
          </Suspense>

          {/* Primary Visualizations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Step Bottlenecks Chart */}
            <section className="p-5 bg-white border border-slate-200 rounded-lg space-y-3">
              <div className="border-b border-slate-100 pb-2.5">
                <h2 className="text-sm font-semibold text-slate-900">
                  Step Turnaround vs SLA Target
                </h2>
                <p className="text-xs text-slate-500">
                  P50 Median and P90 Tail Latency in minutes
                </p>
              </div>

              <StepBottleneckChart steps={data.stepMetrics} />
            </section>

            {/* Department Backlog Table */}
            <section className="p-5 bg-white border border-slate-200 rounded-lg space-y-3">
              <div className="border-b border-slate-100 pb-2.5">
                <h2 className="text-sm font-semibold text-slate-900">
                  Department Backlog &amp; Breach Summary
                </h2>
                <p className="text-xs text-slate-500">
                  Active approval queues and overdue status
                </p>
              </div>

              <DepartmentBreachTable rankings={data.departmentRankings} />
            </section>
          </div>
        </>
      )}

      {/* Technical Architecture Reference */}
      <section className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-600 space-y-2">
        <h3 className="font-semibold text-slate-800">
          Architecture Reference (Q2 Prescreening Question)
        </h3>
        <p className="leading-relaxed">
          This dashboard runs as a React Server Component where data aggregation occurs entirely on the server.
          Filter states are retained via standard HTTP query parameters, eliminating client-side global state dependencies
          while preserving complete browser back/forward history navigation. Query models match the PostgreSQL schema in{' '}
          <code className="text-slate-800">database/schema_q2_sla.sql</code> and{' '}
          <code className="text-slate-800">database/queries_q2_analytics.sql</code>.
        </p>
      </section>
    </main>
  );
}
