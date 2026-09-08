/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(a): Cryptographically Verified JWT & Webhook HMAC Authentication Utilities
 */

import { jwtVerify, SignJWT } from 'jose';

export interface UserSessionPayload {
  userId: string;
  email: string;
  role: string;
  departmentId?: string;
  exp: number;
}

/**
 * Validates a JWT bearer token using genuine cryptographic HMAC-SHA256 signature verification via `jose`.
 * Rejects forged tokens, tampered payloads, expired tokens, and malformed structures.
 */
export async function verifyJwtToken(token: string, secretKey: string): Promise<UserSessionPayload> {
  if (!token || typeof token !== 'string' || token.trim() === '') {
    throw new Error('Token is required.');
  }

  if (!secretKey) {
    throw new Error('Secret key is required for token verification.');
  }

  const secret = new TextEncoder().encode(secretKey);
  
  // Real cryptographic signature and claims verification
  const { payload } = await jwtVerify(token, secret, {
    algorithms: ['HS256'],
  });

  return {
    userId: String(payload.sub || payload.userId || ''),
    email: String(payload.email || ''),
    role: String(payload.role || 'user'),
    departmentId: payload.departmentId ? String(payload.departmentId) : undefined,
    exp: typeof payload.exp === 'number' ? payload.exp : 0,
  };
}

/**
 * Utility helper to generate genuine signed JWTs for testing and local authentication flows.
 */
export async function signJwtToken(
  claims: { sub: string; email: string; role: string; departmentId?: string },
  secretKey: string,
  expiresIn = '1h'
): Promise<string> {
  const secret = new TextEncoder().encode(secretKey);
  return new SignJWT(claims)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(expiresIn)
    .sign(secret);
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

  // Constant-time comparison to prevent timing attacks
  if (computedHex.length !== cleanSig.length) return false;
  let mismatch = 0;
  for (let i = 0; i < computedHex.length; i++) {
    mismatch |= computedHex.charCodeAt(i) ^ cleanSig.charCodeAt(i);
  }
  return mismatch === 0;
}
