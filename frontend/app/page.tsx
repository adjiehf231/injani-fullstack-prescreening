import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <div className="max-w-2xl bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6">
        <div className="inline-block px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-full uppercase tracking-wider">
          PT Injani Systems Prescreening
        </div>
        <h1 className="text-3xl font-bold text-slate-900">
          Fullstack Developer Prescreening Application
        </h1>
        <p className="text-slate-600 text-sm leading-relaxed">
          Next.js 14 App Router integration featuring React Server Components, SLA bottleneck analytics,
          cryptographically verified Edge JWT middleware, and robust API design.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
          <Link
            href="/dashboard"
            className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors shadow-sm"
          >
            Open SLA Analytics Dashboard &rarr;
          </Link>
          <a
            href="https://github.com/adjiehf231/injani-fullstack-prescreening"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-5 py-2.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
          >
            GitHub Repository
          </a>
        </div>
      </div>
    </main>
  );
}
