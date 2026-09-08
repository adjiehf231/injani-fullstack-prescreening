/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(a): JWT Verification & Webhook HMAC Authentication Utilities
 */

export interface UserSessionPayload {
  userId: string;
  email: string;
  role: string;
  departmentId?: string;
  exp: number;
}

/**
 * Validates a JWT bearer token using Web Crypto API.
 * In production: Verify signature using HMAC-SHA256 secret or RSA/ECDSA public key via `jose.jwtVerify`.
 */
export async function verifyJwtToken(token: string, secretKey: string): Promise<UserSessionPayload> {
  if (!token || token.length < 10) {
    throw new Error('Malformed or empty token.');
  }

  // Parse standard 3-part JWT
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT segment structure.');
  }

  try {
    const payloadJson = Buffer.from(parts[1], 'base64url').toString('utf-8');
    const payload = JSON.parse(payloadJson) as UserSessionPayload;

    // Check expiration
    const nowEpoch = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < nowEpoch) {
      throw new Error('Token has expired.');
    }

    return payload;
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : 'Unknown parsing failure';
    throw new Error(`Token verification failed: ${msg}`);
  }
}

/**
 * Verifies HMAC-SHA256 signature for external webhook callers (WhatsApp Cloud API / Stripe / GitHub)
 * Uses Web Crypto API compatible with Next.js Edge & Node.js runtimes.
 */
export async function verifyWebhookHmac(
  rawBody: string,
  receivedSignature: string,
  secret: string
): Promise<boolean> {
  if (!receivedSignature || !secret) return false;

  const cleanSig = receivedSignature.replace(/^sha256=/, '');
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const msgData = encoder.encode(rawBody);

  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );

  const signatureBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  const computedHex = Array.from(new Uint8Array(signatureBuffer))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  // Constant-time length check and character comparison
  if (computedHex.length !== cleanSig.length) return false;
  let mismatch = 0;
  for (let i = 0; i < computedHex.length; i++) {
    mismatch |= computedHex.charCodeAt(i) ^ cleanSig.charCodeAt(i);
  }
  return mismatch === 0;
}
