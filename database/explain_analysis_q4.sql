-- ============================================================================
-- PT Injani Systems - Fullstack Developer Prescreening
-- Q4: PostgreSQL Query Diagnostics: EXPLAIN (ANALYZE, BUFFERS) & Rewrites
-- ============================================================================

-- ============================================================================
-- 1. DIAGNOSTIC QUERY
-- ============================================================================
-- Run EXPLAIN with ANALYZE and BUFFERS to get actual execution metrics:
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)
SELECT id, user_id, amount, currency, status, created_at
FROM transactions_unoptimized
WHERE user_id = 45892
  AND status = 'SETTLED'
  AND created_at >= '2026-08-01 00:00:00+00' 
  AND created_at < '2026-09-01 00:00:00+00'
ORDER BY created_at DESC
LIMIT 50;

/*
WHAT A SENIOR ENGINEER LOOKS FOR IN THE EXPLAIN (ANALYZE, BUFFERS) OUTPUT:
-------------------------------------------------------------------------------
1. Access Method (Seq Scan vs. Index Scan vs. Bitmap Index Scan):
   - Symptom: "Seq Scan on transactions ... Rows Removed by Filter: 9,998,500"
   - Meaning: Missing index or planner decided table scan is cheaper because of outdated statistics.
   - Target: "Index Scan" or "Index Only Scan using idx_transactions_user_status_created".

2. Buffer Usage (Shared Hit vs. Shared Read vs. Written):
   - Symptom: "Buffers: shared hit=120 read=85400"
   - Meaning: 85,400 8KB blocks (~683 MB) had to be fetched from physical disk/SSD into RAM,
     causing massive I/O latency (4+ seconds).
   - Target: "Buffers: shared hit=4 read=0" (all index pages cached in PostgreSQL buffer pool).

3. Estimated Rows vs. Actual Rows (Planner Statistics Accuracy):
   - Symptom: "rows=1 width=48 (actual rows=1250 loops=1)"
   - Meaning: 1000x discrepancy. Autovacuum / ANALYZE statistics are stale; default_statistics_target
     might be too low, misleading the planner into choosing a nested loop or sequential scan.
   - Fix: ANALYZE transactions; or ALTER TABLE transactions ALTER COLUMN status SET STATISTICS 500;

4. Sort Method and Memory Footprint:
   - Symptom: "Sort Method: external merge Disk: 4800kB"
   - Meaning: Sorting `ORDER BY created_at DESC` exceeded `work_mem`, spilling temporary sort files
     to disk, destroying latency.
   - Target: Zero sorting step because the B-tree index `(..., created_at DESC)` already returns tuples
     in the exact requested order!
*/


-- ============================================================================
-- 2. QUERY REWRITE: KEYSET (CURSOR-BASED) PAGINATION VS OFFSET
-- ============================================================================

-- Anti-pattern (Page 100 with OFFSET):
-- PostgreSQL must scan 5,000 rows and discard the first 4,950 rows!
-- SELECT id, amount, created_at FROM transactions 
-- WHERE user_id = 45892 AND status = 'SETTLED'
-- ORDER BY created_at DESC, id DESC
-- LIMIT 50 OFFSET 4950;

-- Optimized Senior Rewrite: Keyset / Cursor Pagination
-- Uses an indexed B-tree seek from the cursor and avoids the growing scan-and-discard cost of deep OFFSET pagination.
-- B-tree seek is approximately O(log n), followed by reading k rows for the requested page:
SELECT id, user_id, amount, currency, status, created_at
FROM transactions_unoptimized
WHERE user_id = :user_id
  AND status = 'SETTLED'
  -- Compound tuple comparison uses the B-tree directly:
  AND (created_at, id) < (:last_seen_created_at, :last_seen_id)
ORDER BY created_at DESC, id DESC
LIMIT 50;


-- ============================================================================
-- 3. SCHEMA REWRITE: COVERING INDEX (INDEX-ONLY SCAN ELIGIBILITY)
-- ============================================================================
-- With the aligned covering index:
-- CREATE INDEX idx_transactions_user_status_created_id 
-- ON transactions (user_id, status, created_at DESC, id DESC) 
-- INCLUDE (amount, currency);
--
-- Planner Mechanics:
-- 1. If the table's Visibility Map (VM) confirms all tuples in referenced 8KB pages 
--    are "all-visible" (maintained by autovacuum), PostgreSQL fulfills this via 
--    Index Only Scan with zero heap table page accesses.
-- 2. If recent updates/inserts leave pages dirty, PostgreSQL falls back to fetching 
--    unconfirmed tuples from heap pages (reflected in EXPLAIN as "Heap Fetches: N").
-- 3. The compound tuple predicate `(created_at, id) < (:last_ts, :last_id)` maps 
--    directly to the pre-sorted B-tree leaf order, avoiding any sort node.
