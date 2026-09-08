-- ============================================================================
-- PT Injani Systems - Fullstack Developer Prescreening
-- Q4: PostgreSQL Query Performance & Schema Optimization (10M Rows Table)
-- ============================================================================

-- Base 10-Million Row Transactions Table (Unoptimized Baseline Schema)
CREATE TABLE transactions_unoptimized (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',
    status VARCHAR(32) NOT NULL,           -- 'PENDING', 'SETTLED', 'FAILED', 'CANCELLED'
    payment_method VARCHAR(64) NOT NULL,
    reference_id VARCHAR(128) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- The Slow Query (4+ seconds on 10 million rows without proper indexes):
-- SELECT id, user_id, amount, status, created_at
-- FROM transactions
-- WHERE user_id = 45892
--   AND status = 'SETTLED'
--   AND created_at >= '2026-08-01 00:00:00+00' 
--   AND created_at < '2026-09-01 00:00:00+00'
-- ORDER BY created_at DESC
-- LIMIT 50;


-- ============================================================================
-- OPTIMIZATION STRATEGY 1: COMPOSITE B-TREE INDEX
-- ============================================================================
-- Rule for multi-column B-tree: (Equality columns first, Range/Sort column last)
-- 1. user_id = 45892 (Equality)
-- 2. status = 'SETTLED' (Equality)
-- 3. created_at DESC (Range comparison + pre-sorted for ORDER BY created_at DESC)
-- Optional: INCLUDE (amount, currency) to allow 100% INDEX ONLY SCAN without heap access!

CREATE INDEX idx_transactions_user_status_created 
ON transactions_unoptimized (user_id, status, created_at DESC)
INCLUDE (amount, currency);


-- ============================================================================
-- OPTIMIZATION STRATEGY 2: PARTIAL INDEX FOR HIGH-SKEW STATUSES
-- ============================================================================
-- In typical transaction systems, 95%+ of rows are 'SETTLED' or 'COMPLETED'.
-- If queries predominantly filter active/pending items:
-- Size of index drops from ~300 MB to ~10 MB, fitting entirely in RAM!

CREATE INDEX idx_transactions_pending_user_created 
ON transactions_unoptimized (user_id, created_at DESC) 
WHERE status = 'PENDING';


-- ============================================================================
-- OPTIMIZATION STRATEGY 3: DECLARATIVE RANGE PARTITIONING (TABLE REDESIGN)
-- ============================================================================
-- Partition by created_at range (monthly).
-- Query planner performs Partition Pruning, immediately excluding 95%+ of partitions
-- without even touching their index or data pages!

CREATE TABLE transactions_partitioned (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',
    status VARCHAR(32) NOT NULL,
    payment_method VARCHAR(64) NOT NULL,
    reference_id VARCHAR(128) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Monthly Partitions (Example 2026 Q3):
CREATE TABLE transactions_y2026m07 PARTITION OF transactions_partitioned
    FOR VALUES FROM ('2026-07-01 00:00:00+00') TO ('2026-08-01 00:00:00+00');

CREATE TABLE transactions_y2026m08 PARTITION OF transactions_partitioned
    FOR VALUES FROM ('2026-08-01 00:00:00+00') TO ('2026-09-01 00:00:00+00');

CREATE TABLE transactions_y2026m09 PARTITION OF transactions_partitioned
    FOR VALUES FROM ('2026-09-01 00:00:00+00') TO ('2026-10-01 00:00:00+00');

-- Partition local index automatically applied to each sub-table:
CREATE INDEX idx_trans_part_user_status_created 
ON transactions_partitioned (user_id, status, created_at DESC)
INCLUDE (amount, currency);
