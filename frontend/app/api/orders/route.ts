/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5: Next.js 14 App Router API Route (Orders Submission with Rate Limiting & Error Handling)
 */

import { NextRequest } from 'next/server';
import { apiSuccess, apiError } from '@/lib/errors';
import { globalRateLimiter } from '@/lib/rate-limit';

interface CreateOrderBody {
  items: Array<{
    itemName: string;
    quantity: number;
    unit?: string;
  }>;
  deliveryAddress: string;
}

export async function POST(request: NextRequest) {
  const userId = request.headers.get('x-user-id') || 'anonymous_user';
  const clientIp = request.headers.get('x-forwarded-for')?.split(',')[0] || '127.0.0.1';

  // 1. Rate Limiting enforcement (Q5b)
  const rateLimitResult = globalRateLimiter.check(`orders:${userId}:${clientIp}`);
  if (!rateLimitResult.success) {
    return apiError(
      429,
      'RATE_LIMIT_EXCEEDED',
      `Rate limit exceeded. Try again in ${Math.ceil(rateLimitResult.resetMs / 1000)} seconds.`,
      undefined,
      { 'Retry-After': String(Math.ceil(rateLimitResult.resetMs / 1000)) }
    );
  }

  // 2. Body parsing and schema validation (Q5c)
  let body: CreateOrderBody;
  try {
    body = await request.json();
  } catch {
    return apiError(400, 'MALFORMED_JSON', 'Request payload could not be parsed as valid JSON.');
  }

  const validationErrors = [];
  if (!body.items || !Array.isArray(body.items) || body.items.length === 0) {
    validationErrors.push({
      field: 'items',
      message: 'Order items list must contain at least one item.',
      code: 'REQUIRED_FIELD',
    });
  } else {
    body.items.forEach((item, index) => {
      if (!item.itemName || item.itemName.trim() === '') {
        validationErrors.push({
          field: `items[${index}].itemName`,
          message: 'Item name is required.',
          code: 'INVALID_VALUE',
        });
      }
      if (!item.quantity || item.quantity <= 0) {
        validationErrors.push({
          field: `items[${index}].quantity`,
          message: 'Quantity must be a positive number.',
          code: 'INVALID_VALUE',
        });
      }
    });
  }

  if (!body.deliveryAddress || body.deliveryAddress.trim().length < 5) {
    validationErrors.push({
      field: 'deliveryAddress',
      message: 'Delivery address must be at least 5 characters.',
      code: 'INVALID_LENGTH',
    });
  }

  if (validationErrors.length > 0) {
    return apiError(422, 'VALIDATION_ERROR', 'The request payload failed structural validation.', validationErrors);
  }

  // 3. Idempotency Key extraction
  const idempotencyKey = request.headers.get('Idempotency-Key');

  // 4. Forward to Python FastAPI backend or execute business logic
  try {
    const backendUrl = process.env.BACKEND_API_URL || 'http://localhost:8000';
    const backendRes = await fetch(`${backendUrl}/api/v1/orders/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(idempotencyKey ? { 'Idempotency-Key': idempotencyKey } : {}),
      },
      body: JSON.stringify({
        customer_id: userId,
        items: body.items.map((i) => ({ item_name: i.itemName, quantity: i.quantity })),
        delivery_address: body.deliveryAddress,
      }),
    });

    const backendData = await backendRes.json();
    return apiSuccess(backendData.data || backendData, 202);
  } catch {
    // Graceful error handling without leaking server internals
    return apiError(
      503,
      'SERVICE_UNAVAILABLE',
      'The upstream order processing service is temporarily unreachable.'
    );
  }
}
