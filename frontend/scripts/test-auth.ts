/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5 Automated Cryptographic JWT & Webhook Authentication Tests
 */

import assert from 'node:assert/strict';
import { signJwtToken, verifyJwtToken, verifyWebhookHmac } from '../lib/auth';

const VALID_SECRET = 'super-secret-production-key-at-least-32-chars!!';
const ATTACKER_SECRET = 'untrusted-adversary-attacker-secret-key!!';

async function runAuthTests() {
  console.log('Running Frontend Cryptographic Auth Tests with strict assertions...');

  // 1. Valid Token Accepted
  const validToken = await signJwtToken(
    { sub: 'usr_adjie_101', email: 'adjie@injani.co.id', role: 'engineer' },
    VALID_SECRET,
    '1h'
  );
  const payload = await verifyJwtToken(validToken, VALID_SECRET);
  assert.equal(payload.userId, 'usr_adjie_101', 'User ID must match subject');
  assert.equal(payload.email, 'adjie@injani.co.id', 'Email claim must match');
  assert.equal(payload.role, 'engineer', 'Role claim must match');
  assert.ok(payload.exp > 0, 'Expiration timestamp must be present');
  console.log('  [PASS] 1. Valid token accepted with correct claims');

  // 2. Forged Signature Rejected (Signed with different secret)
  const forgedToken = await signJwtToken(
    { sub: 'usr_attacker', email: 'attacker@injani.co.id', role: 'admin' },
    ATTACKER_SECRET,
    '1h'
  );
  await assert.rejects(
    async () => {
      await verifyJwtToken(forgedToken, VALID_SECRET);
    },
    (err: Error) => {
      assert.ok(err.name === 'JWSSignatureVerificationFailed' || err.message.includes('signature'));
      return true;
    },
    'Forged token must be rejected with signature verification error'
  );
  console.log('  [PASS] 2. Forged signature rejected');

  // 3. Tampered Payload Rejected (Signature does not match modified payload)
  const [headerB64, , sigB64] = validToken.split('.');
  const forgedPayload = Buffer.from(
    JSON.stringify({ sub: 'usr_adjie_101', email: 'adjie@injani.co.id', role: 'superadmin' })
  ).toString('base64url');
  const tamperedToken = `${headerB64}.${forgedPayload}.${sigB64}`;

  await assert.rejects(
    async () => {
      await verifyJwtToken(tamperedToken, VALID_SECRET);
    },
    (err: Error) => {
      assert.ok(err.name === 'JWSSignatureVerificationFailed' || err.message.includes('signature'));
      return true;
    },
    'Token with tampered payload must be rejected'
  );
  console.log('  [PASS] 3. Tampered payload rejected');

  // 4. Expired Token Rejected
  const expiredToken = await signJwtToken(
    { sub: 'usr_expired', email: 'expired@injani.co.id', role: 'user' },
    VALID_SECRET,
    '-10s' // Expired 10 seconds ago
  );
  await assert.rejects(
    async () => {
      await verifyJwtToken(expiredToken, VALID_SECRET);
    },
    (err: Error) => {
      assert.ok(err.name === 'JWTExpired' || err.message.includes('expired'));
      return true;
    },
    'Expired token must be rejected'
  );
  console.log('  [PASS] 4. Expired token rejected');

  // 5. Malformed Token Rejected
  const malformedTokens = [
    'invalid.token.format',
    'not-even-a-jwt',
    'header.payload', // missing signature
    'header.payload.signature.extra',
  ];
  for (const badToken of malformedTokens) {
    await assert.rejects(
      async () => {
        await verifyJwtToken(badToken, VALID_SECRET);
      },
      'Malformed token string must be rejected'
    );
  }
  console.log('  [PASS] 5. Malformed tokens rejected');

  // 6. Missing / Empty Token Rejected
  await assert.rejects(
    async () => {
      await verifyJwtToken('', VALID_SECRET);
    },
    (err: Error) => {
      assert.equal(err.message, 'Token is required.');
      return true;
    },
    'Empty token string must be rejected'
  );
  console.log('  [PASS] 6. Empty token rejected');

  // 7. HMAC Webhook Valid Signature Accepted
  const webhookBody = JSON.stringify({ event: 'order.created', order_id: 'ord_test_9988' });
  const encoder = new TextEncoder();
  const keyData = encoder.encode(VALID_SECRET);
  const msgData = encoder.encode(webhookBody);
  const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  const validHexSig = Array.from(new Uint8Array(sigBuffer)).map((b) => b.toString(16).padStart(2, '0')).join('');

  const hmacValid = await verifyWebhookHmac(webhookBody, validHexSig, VALID_SECRET);
  assert.equal(hmacValid, true, 'HMAC signature for authentic body must be valid');
  console.log('  [PASS] 7. HMAC webhook signature verified successfully');

  // 8. HMAC Webhook Tampered Body Rejected
  const hmacTampered = await verifyWebhookHmac(webhookBody + 'tampered_data', validHexSig, VALID_SECRET);
  assert.equal(hmacTampered, false, 'HMAC signature for tampered body must be invalid');
  console.log('  [PASS] 8. Tampered HMAC webhook payload rejected');

  console.log('\nAll 8 Cryptographic Authentication Tests Passed Successfully!\n');
}

runAuthTests().catch((err) => {
  console.error('\n[FATAL] Auth test failure:', err);
  process.exit(1);
});
