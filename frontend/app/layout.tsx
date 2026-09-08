import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';

export const metadata: Metadata = {
  title: 'Injani Systems - Operations & SLA Analytics Portal',
  description: 'PT Injani Systems Fullstack Developer Prescreening (Next.js 14 & Python FastAPI)',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 antialiased selection:bg-blue-100 selection:text-blue-900">
        <Navbar />
        <div className="flex-1">
          {children}
        </div>
        <footer className="border-t border-slate-200 bg-white py-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
            <p>
              PT Injani Systems &mdash; Programmer (NextJS & Python) Prescreening
            </p>
            <p className="flex items-center gap-1.5">
              <span>Candidate:</span>
              <strong className="font-semibold text-slate-800">Adjie Hari Fajar</strong>
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}

