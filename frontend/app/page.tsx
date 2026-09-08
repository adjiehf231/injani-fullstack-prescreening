import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  const architecturalModules = [
    {
      title: 'SLA Analytics Dashboard (Q2)',
      tag: 'Next.js 14 RSC',
      description:
        'Multi-step workflow turnaround and SLA compliance monitoring. Employs React Server Components for zero client waterfall and URL-driven filter state.',
      href: '/dashboard',
      actionText: 'View Dashboard',
    },
    {
      title: 'Cryptographic Edge Security (Q5)',
      tag: 'Edge Middleware & jose',
      description:
        'Fail-closed HMAC-SHA256 signature verification at the edge, per-user sliding window rate limiting, and RFC 7807 compliant error envelopes.',
      href: '/api/orders',
      actionText: 'Inspect API Route',
    },
    {
      title: 'Async Cloud Tasks & Workers (Q3/Q6)',
      tag: 'FastAPI & AsyncIO',
      description:
        'Background task execution, Cloud Tasks worker endpoint with dead-letter queue handling, and idempotency locking.',
      href: 'https://github.com/adjiehf231/injani-fullstack-prescreening#part-b-q3-google-cloud-tasks-scheduled-workflows',
      actionText: 'View Architecture',
      external: true,
    },
    {
      title: 'PostgreSQL Relational Design (Q2/Q4)',
      tag: 'PostgreSQL 16',
      description:
        'Generated duration columns, monthly range table partitioning, and composite B-tree indexing for deterministic keyset pagination.',
      href: 'https://github.com/adjiehf231/injani-fullstack-prescreening#part-b-q4-postgresql-query-optimization--explain-analyze',
      actionText: 'View Query Plan',
      external: true,
    },
  ];

  const systemSpecs = [
    { label: 'Frontend Stack', value: 'Next.js 14 (App Router), TypeScript, Tailwind CSS, jose' },
    { label: 'Backend Stack', value: 'Python 3.12 / 3.13, FastAPI, Pydantic v2, pytest (26 passed)' },
    { label: 'Database', value: 'PostgreSQL 16 (Generated columns, Range partitions, Keyset indexes)' },
    { label: 'Cloud Architecture', value: 'Google Cloud Run, Cloud Tasks, Workload Identity Federation' },
    { label: 'Evaluation Target', value: 'PT Injani Systems — Programmer (NextJS & Python)' },
    { label: 'Candidate', value: 'Adjie Hari Fajar' },
  ];

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 space-y-12">
      {/* Hero Section */}
      <section className="space-y-4 max-w-3xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-800 border border-slate-200">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-600" aria-hidden="true" />
          <span>PT Injani Systems Prescreening Submission</span>
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
          Operations & SLA Analytics Platform
        </h1>

        <p className="text-base text-slate-600 leading-relaxed">
          A production-grade fullstack implementation demonstrating React Server Components,
          cryptographically verified Edge JWT middleware, SLA turnaround analytics, and Python async background processing.
        </p>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors shadow-xs"
          >
            <span>Open SLA Analytics Dashboard</span>
            <span className="ml-1.5" aria-hidden="true">&rarr;</span>
          </Link>

          <a
            href="https://github.com/adjiehf231/injani-fullstack-prescreening"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2.5 text-sm font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 hover:text-slate-900 rounded-lg transition-colors shadow-2xs"
          >
            GitHub Repository
          </a>
        </div>
      </section>

      {/* Architectural Modules Grid */}
      <section className="space-y-4">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <h2 className="text-lg font-semibold tracking-tight text-slate-900">
            Prescreening Implementation Modules
          </h2>
          <span className="text-xs text-slate-500">4 Core Pillars</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {architecturalModules.map((module) => (
            <article
              key={module.title}
              className="flex flex-col justify-between p-5 bg-white border border-slate-200 rounded-xl shadow-xs hover:border-slate-300 transition-colors"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
                    {module.tag}
                  </span>
                </div>
                <h3 className="text-base font-semibold text-slate-900">
                  {module.title}
                </h3>
                <p className="text-sm text-slate-600 leading-relaxed">
                  {module.description}
                </p>
              </div>

              <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between">
                {module.external ? (
                  <a
                    href={module.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-semibold text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  >
                    <span>{module.actionText}</span>
                    <span aria-hidden="true">&nearr;</span>
                  </a>
                ) : (
                  <Link
                    href={module.href}
                    className="text-xs font-semibold text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  >
                    <span>{module.actionText}</span>
                    <span aria-hidden="true">&rarr;</span>
                  </Link>
                )}
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* System Technical Specifications */}
      <section className="p-6 bg-white border border-slate-200 rounded-xl shadow-xs space-y-4">
        <h2 className="text-base font-semibold text-slate-900 border-b border-slate-100 pb-3">
          Technical Specifications & System Verification
        </h2>

        <dl className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-4 text-xs">
          {systemSpecs.map((spec) => (
            <div key={spec.label} className="space-y-1">
              <dt className="text-slate-500 font-medium">{spec.label}</dt>
              <dd className="text-slate-900 font-semibold">{spec.value}</dd>
            </div>
          ))}
        </dl>
      </section>
    </main>
  );
}
