/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q5(b): Sliding-Window Rate Limiter without a Dedicated Redis Instance
 * 
 * In single-instance Node.js runtimes, an in-memory Map with timestamp arrays 
 * provides accurate sliding-window rate limiting with zero external dependencies.
 * An active interval prunes expired entries to prevent memory leaks.
 */

interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

interface RateLimitRecord {
  timestamps: number[];
}

export class MemoryRateLimiter {
  private cache = new Map<string, RateLimitRecord>();
  private sweepInterval: NodeJS.Timeout | null = null;

  constructor(private config: RateLimitConfig = { maxRequests: 20, windowMs: 60_000 }) {
    // Background garbage collection sweep every 2 minutes
    this.sweepInterval = setInterval(() => this.sweep(), 120_000);
    if (this.sweepInterval.unref) {
      this.sweepInterval.unref();
    }
  }

  public check(identifier: string): { success: boolean; limit: number; remaining: number; resetMs: number } {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    let record = this.cache.get(identifier);
    if (!record) {
      record = { timestamps: [] };
      this.cache.set(identifier, record);
    }

    // Filter out timestamps outside the sliding window
    record.timestamps = record.timestamps.filter((ts) => ts > windowStart);

    if (record.timestamps.length >= this.config.maxRequests) {
      const oldestInWindow = record.timestamps[0];
      const resetMs = Math.max(0, this.config.windowMs - (now - oldestInWindow));
      return {
        success: false,
        limit: this.config.maxRequests,
        remaining: 0,
        resetMs,
      };
    }

    record.timestamps.push(now);
    return {
      success: true,
      limit: this.config.maxRequests,
      remaining: this.config.maxRequests - record.timestamps.length,
      resetMs: this.config.windowMs,
    };
  }

  private sweep() {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;
    for (const [key, record] of this.cache.entries()) {
      record.timestamps = record.timestamps.filter((ts) => ts > windowStart);
      if (record.timestamps.length === 0) {
        this.cache.delete(key);
      }
    }
  }
}

// Export singleton instance
export const globalRateLimiter = new MemoryRateLimiter({
  maxRequests: 30,
  windowMs: 60_000, // 30 requests per minute
});
