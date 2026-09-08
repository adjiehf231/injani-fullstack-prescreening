-- ============================================================================
-- PT Injani Systems - Fullstack Developer Prescreening
-- Q2: SLA Analytics Dashboard - Analytical Queries for Process Bottlenecks
-- ============================================================================

-- 1. Step Bottleneck Analysis: P50, P90, P95 and Average Elapsed Time by Step Type
-- Identifies which steps in the workflow create the longest friction for users.
SELECT 
    wsi.step_type,
    COUNT(*) AS total_completed_steps,
    ROUND(AVG(wsi.elapsed_minutes), 1) AS avg_duration_minutes,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY wsi.elapsed_minutes) AS p50_median_minutes,
    PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY wsi.elapsed_minutes) AS p90_tail_minutes,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY wsi.elapsed_minutes) AS p95_extreme_minutes,
    MAX(wsi.elapsed_minutes) AS max_duration_minutes,
    ROUND(
        (COUNT(*) FILTER (WHERE wsi.is_sla_breached = TRUE)::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 
        2
    ) AS sla_breach_percentage
FROM workflow_step_instances wsi
WHERE wsi.status IN ('APPROVED', 'REJECTED')
  AND wsi.completed_at IS NOT NULL
  AND wsi.assigned_at >= :start_date 
  AND wsi.assigned_at <= :end_date
  AND (:department_id::UUID IS NULL OR wsi.department_id = :department_id::UUID)
GROUP BY wsi.step_type
ORDER BY p90_tail_minutes DESC;


-- 2. Departmental SLA Breach Rates & Active Backlog
-- Shows which departments are consistently violating SLA and their current pending load.
SELECT 
    d.name AS department_name,
    COUNT(*) FILTER (WHERE wsi.status = 'PENDING') AS active_pending_tasks,
    COUNT(*) FILTER (WHERE wsi.status = 'PENDING' AND EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - wsi.assigned_at)) / 60 > wsi.target_sla_minutes) AS currently_overdue_tasks,
    COUNT(*) FILTER (WHERE wsi.completed_at IS NOT NULL) AS completed_tasks,
    COUNT(*) FILTER (WHERE wsi.is_sla_breached = TRUE) AS total_sla_breaches,
    ROUND(
        (COUNT(*) FILTER (WHERE wsi.is_sla_breached = TRUE)::NUMERIC / 
         NULLIF(COUNT(*) FILTER (WHERE wsi.completed_at IS NOT NULL), 0)) * 100, 
        2
    ) AS historical_breach_rate_pct,
    ROUND(AVG(wsi.elapsed_minutes), 1) AS avg_elapsed_minutes
FROM departments d
LEFT JOIN workflow_step_instances wsi ON wsi.department_id = d.id
  AND wsi.assigned_at >= :start_date 
  AND wsi.assigned_at <= :end_date
GROUP BY d.id, d.name
ORDER BY currently_overdue_tasks DESC, historical_breach_rate_pct DESC;


-- 3. Individual Assignee Workload & Resolution Efficiency
-- Pinpoints whether bottlenecks are structural (step design) or operational (individual overload).
SELECT 
    u.full_name AS assignee_name,
    u.email,
    d.name AS department_name,
    COUNT(*) FILTER (WHERE wsi.status = 'PENDING') AS current_queue_count,
    COUNT(*) FILTER (WHERE wsi.completed_at IS NOT NULL) AS total_processed,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY wsi.elapsed_minutes) AS median_completion_minutes,
    COUNT(*) FILTER (WHERE wsi.is_sla_breached = TRUE) AS total_breaches,
    ROUND(
        (COUNT(*) FILTER (WHERE wsi.is_sla_breached = TRUE)::NUMERIC / 
         NULLIF(COUNT(*) FILTER (WHERE wsi.completed_at IS NOT NULL), 0)) * 100, 
        2
    ) AS breach_rate_pct
FROM users u
JOIN departments d ON u.department_id = d.id
JOIN workflow_step_instances wsi ON wsi.assignee_id = u.id
WHERE wsi.assigned_at >= :start_date 
  AND wsi.assigned_at <= :end_date
  AND (:department_id::UUID IS NULL OR wsi.department_id = :department_id::UUID)
GROUP BY u.id, u.full_name, u.email, d.name
ORDER BY current_queue_count DESC, breach_rate_pct DESC;


-- 4. Workflow Lifecycle Duration & Drop-Off / Rejection Rate
-- Assesses end-to-end efficiency across the entire approval journey.
SELECT 
    wd.name AS workflow_type,
    COUNT(wi.id) AS total_instances,
    COUNT(*) FILTER (WHERE wi.status = 'APPROVED') AS approved_count,
    COUNT(*) FILTER (WHERE wi.status = 'REJECTED') AS rejected_count,
    COUNT(*) FILTER (WHERE wi.status = 'IN_PROGRESS') AS ongoing_count,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (wi.completed_at - wi.created_at)) / 3600) 
        FILTER (WHERE wi.completed_at IS NOT NULL)::NUMERIC, 
        2
    ) AS avg_lifecycle_hours,
    ROUND(
        (COUNT(*) FILTER (WHERE wi.status = 'REJECTED')::NUMERIC / NULLIF(COUNT(wi.id), 0)) * 100, 
        2
    ) AS rejection_rate_pct
FROM workflow_instances wi
JOIN workflow_definitions wd ON wi.workflow_def_id = wd.id
WHERE wi.created_at >= :start_date 
  AND wi.created_at <= :end_date
GROUP BY wd.id, wd.name
ORDER BY total_instances DESC;
