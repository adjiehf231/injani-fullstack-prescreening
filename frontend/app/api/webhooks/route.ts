/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5: Next.js 14 App Router External Webhook Handler (HMAC-SHA256 Protected)
 */

import { NextRequest } from 'next/server';
import { apiSuccess, apiError } from '@/lib/errors';
import { verifyWebhookHmac } from '@/lib/auth';

export async function POST(request: NextRequest) {
  const signature = request.headers.get('x-hub-signature-256');
  const secret = process.env.WEBHOOK_SECRET || 'injani-webhook-secret-token';

  if (!signature) {
    return apiError(401, 'MISSING_SIGNATURE', 'Missing required X-Hub-Signature-256 header.');
  }

  const rawBody = await request.text();
  const isValid = await verifyWebhookHmac(rawBody, signature, secret);

  if (!isValid) {
    return apiError(401, 'INVALID_SIGNATURE', 'HMAC signature verification failed. Untrusted webhook sender.');
  }

  try {
    const payload = JSON.parse(rawBody);
    // Process verified webhook event (e.g. WhatsApp message arrived or status update)
    return apiSuccess({ received: true, eventId: payload.id || crypto.randomUUID() }, 200);
  } catch {
    return apiError(400, 'INVALID_JSON', 'Webhook payload could not be parsed.');
  }
}
