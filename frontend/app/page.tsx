import React from 'react';
import Link from 'next/link';

export default function HomePage() {
  const implementationSections = [
    {
      title: 'SLA Analytics',
      description: 'Workflow turnaround, bottlenecks, and SLA analysis.',
      tag: 'Next.js 14 RSC',
      href: '/dashboard',
      actionText: 'Open Dashboard',
      isInternal: true,
    },
    {
      title: 'Security & API',
      description: 'Verified JWT handling, request validation, rate limiting, and idempotency controls.',
      tag: 'Edge Middleware & jose',
      href: 'https://github.com/adjiehf231/injani-fullstack-prescreening/blob/main/frontend/app/api/orders/route.ts',
      actionText: 'View API Implementation',
      isInternal: false,
    },
    {
      title: 'Async Processing',
      description: 'Python async processing and Cloud Tasks reference architecture.',
      tag: 'FastAPI & AsyncIO',
      href: 'https://github.com/adjiehf231/injani-fullstack-prescreening#part-b-q3-google-cloud-tasks-scheduled-workflows',
      actionText: 'View Worker Architecture',
      isInternal: false,
    },
    {
      title: 'PostgreSQL',
      description: 'Schema design, indexing, and keyset pagination.',
      tag: 'PostgreSQL 16',
      href: 'https://github.com/adjiehf231/injani-fullstack-prescreening#part-b-q4-postgresql-query-optimization--explain-analyze',
      actionText: 'View Query Design',
      isInternal: false,
    },
  ];

  const technicalSpecs = [
    { area: 'Frontend', stack: 'Next.js 14 (App Router) · TypeScript · Tailwind CSS' },
    { area: 'Backend', stack: 'Python 3.12 / 3.13 · FastAPI · Pydantic v2' },
    { area: 'Database', stack: 'PostgreSQL 16 (Generated columns, Partitioning, Keyset)' },
    { area: 'Security', stack: 'JWT (jose) · HMAC webhook · Fail-closed secrets' },
    { area: 'Testing', stack: 'pytest (26 passed) · TypeScript · ESLint · Auth test suite' },
  ];

  return (
    <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 space-y-12">
      {/* Hero Section */}
      <section className="space-y-4">
        <div className="inline-block px-2.5 py-1 text-xs font-medium text-slate-600 bg-slate-100 border border-slate-200 rounded">
          Fullstack Prescreening
        </div>

        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-slate-900 leading-tight">
          Operations &amp; SLA Analytics
        </h1>

        <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl">
          A reference implementation demonstrating Next.js, Python APIs,
          PostgreSQL, authentication, and async processing.
        </p>

        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-slate-900 hover:bg-slate-800 rounded-md transition-colors"
          >
            Open SLA Analytics Dashboard &rarr;
          </Link>

          <a
            href="https://github.com/adjiehf231/injani-fullstack-prescreening"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 rounded-md transition-colors"
          >
            GitHub Repository &nearr;
          </a>
        </div>
      </section>

      {/* Implementation Section */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold tracking-tight text-slate-900 border-b border-slate-200 pb-2">
          Implementation
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {implementationSections.map((item) => (
            <article
              key={item.title}
              className="p-4 bg-white border border-slate-200 rounded-lg flex flex-col justify-between hover:border-slate-300 transition-colors"
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-slate-900">
                    {item.title}
                  </h3>
                  <span className="text-[11px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                    {item.tag}
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {item.description}
                </p>
              </div>

              <div className="pt-3 mt-3 border-t border-slate-100">
                {item.isInternal ? (
                  <Link
                    href={item.href}
                    className="text-xs font-medium text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  >
                    <span>{item.actionText}</span>
                    <span aria-hidden="true">&rarr;</span>
                  </Link>
                ) : (
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-medium text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                  >
                    <span>{item.actionText}</span>
                    <span aria-hidden="true">&nearr;</span>
                  </a>
                )}
              </div>
            </article>
          ))}
        </div>
      </section>

      {/* Technical Overview Section */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold tracking-tight text-slate-900 border-b border-slate-200 pb-2">
          Technical Overview
        </h2>

        <div className="bg-white border border-slate-200 rounded-lg divide-y divide-slate-100">
          {technicalSpecs.map((spec) => (
            <div
              key={spec.area}
              className="grid grid-cols-1 sm:grid-cols-4 p-3.5 text-xs gap-1 sm:gap-4"
            >
              <dt className="font-semibold text-slate-800">{spec.area}</dt>
              <dd className="sm:col-span-3 text-slate-600">{spec.stack}</dd>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
