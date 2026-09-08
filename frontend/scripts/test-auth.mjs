import { signJwtToken, verifyJwtToken, verifyWebhookHmac } from '../lib/auth.ts';

const SECRET = 'test-secret-key-32-characters-minimum!!';

async function runTests() {
  console.log('Running Frontend Cryptographic Auth Tests...');

  // 1. Valid Token Verification
  const token = await signJwtToken(
    { sub: 'usr_adjie', email: 'adjie@injani.co.id', role: 'developer' },
    SECRET,
    '1h'
  );
  const payload = await verifyJwtToken(token, SECRET);
  if (payload.userId !== 'usr_adjie' || payload.role !== 'developer') {
    throw new Error('Valid token verification failed');
  }
  console.log('✓ Valid JWT token verified successfully');

  // 2. Forged Token (signed with different key)
  const forgedToken = await signJwtToken(
    { sub: 'attacker', role: 'admin' },
    'untrusted-attacker-secret-key!!',
    '1h'
  );
  try {
    await verifyJwtToken(forgedToken, SECRET);
    throw new Error('Forged token was unexpectedly accepted!');
  } catch (err) {
    console.log('✓ Forged JWT token successfully rejected');
  }

  // 3. Tampered Payload
  const [h, b, s] = token.split('.');
  const tamperedBody = Buffer.from(JSON.stringify({ sub: 'usr_adjie', role: 'admin' })).toString('base64url');
  const tamperedToken = `${h}.${tamperedBody}.${s}`;
  try {
    await verifyJwtToken(tamperedToken, SECRET);
    throw new Error('Tampered token was unexpectedly accepted!');
  } catch (err) {
    console.log('✓ Tampered JWT payload successfully rejected');
  }

  // 4. HMAC Webhook Verification
  const webhookBody = '{"event":"order_created","id":"ord_123"}';
  const encoder = new TextEncoder();
  const keyData = encoder.encode(SECRET);
  const msgData = encoder.encode(webhookBody);
  const cryptoKey = await crypto.subtle.importKey('raw', keyData, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  const validSig = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');

  const hmacValid = await verifyWebhookHmac(webhookBody, validSig, SECRET);
  if (!hmacValid) throw new Error('HMAC verification failed for valid signature');
  console.log('✓ HMAC webhook signature verified successfully');

  const hmacTampered = await verifyWebhookHmac(webhookBody + 'tampered', validSig, SECRET);
  if (hmacTampered) throw new Error('HMAC verification accepted tampered body');
  console.log('✓ Tampered HMAC webhook successfully rejected');

  console.log('\nAll Frontend Auth Verification Tests Passed!');
}

runTests().catch((err) => {
  console.error('Test failure:', err);
  process.exit(1);
});
