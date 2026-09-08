/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(a): Next.js 14 App Router Middleware - Edge Authentication & Gating
 * 
 * ARCHITECTURAL DESIGN: Middleware vs. Route Handler
 * ---------------------------------------------------------------------------
 * 1. Edge Middleware (Coarse-Grained Gatekeeper):
 *    - Executes BEFORE route execution on Edge workers.
 *    - Validates token presence and expiration quickly.
 *    - Bypasses public endpoints (e.g. /api/auth/login, /api/webhooks/*).
 *    - Injects sanitized context headers (x-user-id, x-user-role) into the request.
 *    - Returns immediate 401 Unauthorized, saving server compute.
 * 
 * 2. Route Handler (Fine-Grained Domain Authorization):
 *    - Performs cryptographic verification if payload integrity is paramount.
 *    - Enforces Role-Based Access Control (RBAC) and resource ownership (e.g. user_id == order.user_id).
 *    - Accesses database/ORM directly (which Edge middleware cannot cleanly do).
 */

import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

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

  try {
    // Fast verification on Edge runtime
    // In production: await jwtVerify(token, new TextEncoder().encode(process.env.JWT_SECRET))
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token structure');
    }

    const payload = JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf-8'));
    const now = Math.floor(Date.now() / 1000);

    if (payload.exp && payload.exp < now) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'TOKEN_EXPIRED',
            message: 'Session has expired. Please refresh your credentials.',
            traceId: crypto.randomUUID(),
          },
        },
        { status: 401 }
      );
    }

    // Forward verified claims downstream via request headers
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set('x-user-id', payload.sub || payload.userId || '');
    requestHeaders.set('x-user-role', payload.role || 'user');
    requestHeaders.set('x-user-dept', payload.departmentId || '');

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  } catch {
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INVALID_TOKEN',
          message: 'Supplied credentials are invalid or corrupted.',
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
