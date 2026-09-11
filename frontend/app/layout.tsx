import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';

export const metadata: Metadata = {
  title: 'Injani Prescreening - Operations & SLA Analytics',
  description: 'Fullstack Prescreening Solution for PT Injani Systems (Next.js 14 & Python FastAPI)',
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
        <footer className="border-t border-slate-200 bg-white py-4 text-center">
          <p className="text-xs text-slate-500">
            Technical assessment &bull; <span className="font-medium text-slate-700">Adjie Hari Fajar</span> (NextJS &amp; Python)
          </p>
        </footer>
      </body>
    </html>
  );
}
