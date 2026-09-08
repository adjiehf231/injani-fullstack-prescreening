-- ============================================================================
-- PT Injani Systems - Fullstack Developer Prescreening
-- Q2: SLA Analytics Dashboard for Multi-Step Approval Workflows
-- PostgreSQL Production Schema Definition
-- ============================================================================

-- Ensure standard extensions are available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Departments Table
CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(32) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE RESTRICT,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(128) NOT NULL,
    role VARCHAR(64) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Workflow Definitions (Templates / Types)
CREATE TABLE workflow_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(64) NOT NULL UNIQUE,       -- e.g., 'PURCHASE_ORDER_APPROVAL', 'LEAVE_REQUEST'
    name VARCHAR(128) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4. Workflow Step Definitions (SLA Target Configuration)
CREATE TABLE workflow_step_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_def_id UUID NOT NULL REFERENCES workflow_definitions(id) ON DELETE CASCADE,
    step_type VARCHAR(64) NOT NULL,         -- e.g., 'DEPARTMENT_HEAD_REVIEW', 'FINANCE_APPROVAL', 'DIRECTOR_SIGN'
    step_order INT NOT NULL,                -- Sequence: 1, 2, 3
    target_sla_minutes INT NOT NULL,        -- SLA baseline in minutes (e.g., 240 mins = 4 hours)
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_workflow_step_order UNIQUE (workflow_def_id, step_order),
    CONSTRAINT chk_sla_positive CHECK (target_sla_minutes > 0)
);

-- 5. Workflow Instances
CREATE TABLE workflow_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_def_id UUID NOT NULL REFERENCES workflow_definitions(id) ON DELETE RESTRICT,
    requester_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE RESTRICT,
    reference_number VARCHAR(64) NOT NULL UNIQUE, -- e.g., 'PO-2026-09-0001'
    status VARCHAR(32) NOT NULL DEFAULT 'IN_PROGRESS', 
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    CONSTRAINT chk_workflow_status CHECK (status IN ('IN_PROGRESS', 'APPROVED', 'REJECTED', 'CANCELLED')),
    CONSTRAINT chk_workflow_completed_after_created CHECK (completed_at IS NULL OR completed_at >= created_at)
);

-- 6. Workflow Step Instances (Core Auditing & SLA Duration Tracking)
CREATE TABLE workflow_step_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_instance_id UUID NOT NULL REFERENCES workflow_instances(id) ON DELETE CASCADE,
    step_def_id UUID NOT NULL REFERENCES workflow_step_definitions(id) ON DELETE RESTRICT,
    assignee_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE RESTRICT,
    step_type VARCHAR(64) NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    target_sla_minutes INT NOT NULL,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    
    -- Calculated duration stored via GENERATED ALWAYS column in minutes
    elapsed_minutes INT GENERATED ALWAYS AS (
        CASE 
            WHEN completed_at IS NOT NULL 
            THEN CAST(EXTRACT(EPOCH FROM (completed_at - assigned_at)) / 60 AS INT)
            ELSE NULL 
        END
    ) STORED,
    
    is_sla_breached BOOLEAN GENERATED ALWAYS AS (
        CASE 
            WHEN completed_at IS NOT NULL 
            THEN (CAST(EXTRACT(EPOCH FROM (completed_at - assigned_at)) / 60 AS INT) > target_sla_minutes)
            ELSE NULL 
        END
    ) STORED,

    notes TEXT,
    CONSTRAINT chk_step_status CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'SKIPPED')),
    CONSTRAINT chk_step_completed_after_assigned CHECK (completed_at IS NULL OR completed_at >= assigned_at)
);

-- ============================================================================
-- INDEXING STRATEGY FOR SLA ANALYTICS DASHBOARD
-- ============================================================================

-- Fast filtering by department and assigned date range (Primary Dashboard Filter)
CREATE INDEX idx_step_instances_dept_assigned 
ON workflow_step_instances (department_id, assigned_at DESC);

-- Fast aggregation by step type and date range (Bottleneck identification)
CREATE INDEX idx_step_instances_step_type_assigned 
ON workflow_step_instances (step_type, assigned_at DESC);

-- Fast lookup for individual user workload and performance
CREATE INDEX idx_step_instances_assignee_status 
ON workflow_step_instances (assignee_id, status, assigned_at DESC);

-- Fast identification of SLA breaches for alert badges & filter views
CREATE INDEX idx_step_instances_sla_breach 
ON workflow_step_instances (is_sla_breached, assigned_at DESC) 
WHERE is_sla_breached = TRUE;

-- Composite index on workflow instances for status and time range
CREATE INDEX idx_workflow_instances_dept_created 
ON workflow_instances (department_id, status, created_at DESC);
