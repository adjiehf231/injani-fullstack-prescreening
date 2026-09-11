'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function Navbar() {
  const pathname = usePathname();

  const navLinks = [
    { href: '/', label: 'Overview' },
    { href: '/dashboard', label: 'SLA Analytics' },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:h-16 justify-between py-2 sm:py-0 gap-2 sm:gap-4">
          {/* Top/Left Row: Brand & Assessment Tag */}
          <div className="flex items-center justify-between sm:justify-start gap-3 h-10 sm:h-auto">
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="w-8 h-8 rounded-md bg-slate-900 flex items-center justify-center text-white font-bold text-xs shadow-xs group-hover:bg-blue-600 transition-colors">
                IJ
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-semibold tracking-tight text-slate-900 leading-tight">
                  Injani Prescreening
                </span>
                <span className="text-[11px] font-normal text-slate-500">
                  Fullstack Engineering Assessment
                </span>
              </div>
            </Link>

            <span className="hidden md:inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600 border border-slate-200">
              Next.js 14 App Router
            </span>

            {/* Mobile GitHub link */}
            <div className="sm:hidden">
              <a
                href="https://github.com/adjiehf231/injani-fullstack-prescreening"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded hover:bg-slate-50"
              >
                Repo &nearr;
              </a>
            </div>
          </div>

          {/* Bottom/Center Row on mobile, Centered/Right on desktop */}
          <div className="flex items-center justify-between sm:justify-end gap-3 pb-1 sm:pb-0">
            <nav className="flex items-center gap-1" aria-label="Main Navigation">
              {navLinks.map((link) => {
                const isActive = pathname === link.href;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`px-3 py-1.5 text-xs sm:text-sm rounded-md transition-colors ${
                      isActive
                        ? 'bg-slate-100 text-slate-900 font-semibold'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </nav>

            {/* Desktop GitHub link */}
            <div className="hidden sm:flex items-center">
              <a
                href="https://github.com/adjiehf231/injani-fullstack-prescreening"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-md hover:bg-slate-50 hover:text-slate-900 transition-colors"
              >
                <span>Repository</span>
                <span aria-hidden="true">&nearr;</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
