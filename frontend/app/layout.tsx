import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Injani Systems - SLA Analytics & Order Gateway',
  description: 'Fullstack Prescreening Solution for PT Injani Systems',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-slate-50">{children}</body>
    </html>
  );
}
