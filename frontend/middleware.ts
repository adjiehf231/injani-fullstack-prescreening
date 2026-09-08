/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(a): Next.js 14 App Router Middleware - Edge Authentication & Gating
 * 
 * ARCHITECTURAL DESIGN:
 * 1. Edge Middleware:
 *    - Validates token presence, cryptographic signature, and expiration via `jose.jwtVerify`.
 *    - Bypasses public endpoints (e.g. /api/auth/login, /api/healthz) and webhook callers (/api/webhooks/*).
 *    - Injects verified claims (x-user-id, x-user-role, x-user-dept) into request headers.
 *    - Fails closed: Rejects invalid or forged tokens immediately with 401 Unauthorized.
 * 2. Route Handler:
 *    - Enforces domain authorization where required.
 *    - Object-level ownership validation is a production consideration.
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // 1. Skip non-API routes and static assets
  if (!pathname.startsWith('/api')) {
    return NextResponse.next();
  }

  // 2. Webhook callers use HMAC signatures in route handlers, bypass JWT check
  if (pathname.startsWith('/api/webhooks')) {
    return NextResponse.next();
  }

  // 3. Public API routes (login, register, health check)
  const publicRoutes = ['/api/auth/login', '/api/healthz'];
  if (publicRoutes.includes(pathname)) {
    return NextResponse.next();
  }

  // 4. Extract JWT from Authorization header or HTTP-only session cookie
  const authHeader = request.headers.get('Authorization');
  let token: string | null = null;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.substring(7);
  } else {
    token = request.cookies.get('injani_session')?.value || null;
  }

  if (!token) {
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'UNAUTHORIZED',
          message: 'Authentication required. Bearer token missing.',
          traceId: crypto.randomUUID(),
        },
      },
      { status: 401 }
    );
  }

  const jwtSecret = process.env.JWT_SECRET;
  if (!jwtSecret) {
    // Fails closed if server configuration is missing
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'SERVER_CONFIGURATION_ERROR',
          message: 'Server authentication secret is not configured.',
          traceId: crypto.randomUUID(),
        },
      },
      { status: 500 }
    );
  }

  try {
    const secret = new TextEncoder().encode(jwtSecret);
    const { payload } = await jwtVerify(token, secret, {
      algorithms: ['HS256'],
    });

    // Forward verified claims downstream via request headers
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set('x-user-id', String(payload.sub || payload.userId || ''));
    requestHeaders.set('x-user-role', String(payload.role || 'user'));
    requestHeaders.set('x-user-dept', String(payload.departmentId || ''));

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  } catch (err: unknown) {
    const isExpired =
      err && typeof err === 'object' && 'code' in err && err.code === 'ERR_JWT_EXPIRED';

    return NextResponse.json(
      {
        success: false,
        error: {
          code: isExpired ? 'TOKEN_EXPIRED' : 'INVALID_TOKEN',
          message: isExpired
            ? 'Session has expired. Please refresh your credentials.'
            : 'Supplied credentials failed cryptographic verification.',
          traceId: crypto.randomUUID(),
        },
      },
      { status: 401 }
    );
  }
}

export const config = {
  matcher: ['/api/:path*'],
};
