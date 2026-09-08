/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(c): Consistent, Typed API Error and Response Envelopes
 */

import { NextResponse } from 'next/server';

export interface ErrorDetail {
  field?: string;
  message: string;
  code?: string;
}

export interface ApiErrorPayload {
  code: string;
  message: string;
  details?: ErrorDetail[];
  traceId: string;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: ApiErrorPayload;
}

export function apiSuccess<T>(data: T, status = 200, headers?: HeadersInit): NextResponse<ApiResponse<T>> {
  return NextResponse.json(
    {
      success: true,
      data,
    },
    { status, headers }
  );
}

export function apiError(
  status: number,
  code: string,
  message: string,
  details?: ErrorDetail[],
  headers?: HeadersInit
): NextResponse<ApiResponse<never>> {
  const traceId = crypto.randomUUID();
  return NextResponse.json(
    {
      success: false,
      error: {
        code,
        message,
        details,
        traceId,
      },
    },
    { status, headers }
  );
}
