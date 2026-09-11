/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Q2: SLA Analytics - Deterministic Assessment Dataset & Aggregations
 * 
 * Provides a structured, deterministic sample dataset representing multi-step approval
 * workflows across company departments. All dashboard aggregations (KPIs, percentiles,
 * department rankings) are computed dynamically from this dataset to support real,
 * working URL-driven filtering without client state libraries or external database dependencies.
 */

export interface WorkflowRecord {
  id: string;
  referenceNumber: string;
  department: string;
  stepType: string;
  durationMinutes: number;
  slaMinutes: number;
  isCompleted: boolean;
  daysAgo: number;
}

export const DEPARTMENTS = [
  'All Departments',
  'Finance & Accounting',
  'Legal & Compliance',
  'Operations',
  'Human Resources',
] as const;

export const STEP_TYPES = [
  'All Steps',
  'Dept Head Review',
  'Finance Approval',
  'Legal Review',
  'Director Sign-off',
] as const;

export const DATE_RANGES = [
  { label: 'Past 7 Days', value: '7d', maxDays: 7 },
  { label: 'Past 30 Days', value: '30d', maxDays: 30 },
  { label: 'Past 90 Days', value: '90d', maxDays: 90 },
] as const;

export const SLA_TARGETS: Record<string, number> = {
  'Dept Head Review': 120, // 2 hours
  'Finance Approval': 240, // 4 hours
  'Legal Review': 300,    // 5 hours
  'Director Sign-off': 180, // 3 hours
};

// Deterministic assessment dataset reflecting realistic approval distributions
export const SAMPLE_WORKFLOW_RECORDS: WorkflowRecord[] = [
  // Finance & Accounting (high volume, prone to tail latency bottlenecks)
  { id: 'wf-01', referenceNumber: 'PO-2026-001', department: 'Finance & Accounting', stepType: 'Dept Head Review', durationMinutes: 40, slaMinutes: 120, isCompleted: true, daysAgo: 2 },
  { id: 'wf-02', referenceNumber: 'PO-2026-002', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 190, slaMinutes: 240, isCompleted: true, daysAgo: 4 },
  { id: 'wf-03', referenceNumber: 'PO-2026-003', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 410, slaMinutes: 240, isCompleted: true, daysAgo: 5 }, // Breach
  { id: 'wf-04', referenceNumber: 'PO-2026-004', department: 'Finance & Accounting', stepType: 'Legal Review', durationMinutes: 215, slaMinutes: 300, isCompleted: true, daysAgo: 6 },
  { id: 'wf-05', referenceNumber: 'PO-2026-005', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 280, slaMinutes: 240, isCompleted: false, daysAgo: 3 }, // Overdue pending
  { id: 'wf-06', referenceNumber: 'PO-2026-006', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 310, slaMinutes: 240, isCompleted: false, daysAgo: 4 }, // Overdue pending
  { id: 'wf-07', referenceNumber: 'PO-2026-007', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 120, slaMinutes: 240, isCompleted: false, daysAgo: 1 },
  { id: 'wf-08', referenceNumber: 'PO-2026-008', department: 'Finance & Accounting', stepType: 'Dept Head Review', durationMinutes: 50, slaMinutes: 120, isCompleted: false, daysAgo: 1 },
  { id: 'wf-09', referenceNumber: 'PO-2026-009', department: 'Finance & Accounting', stepType: 'Director Sign-off', durationMinutes: 65, slaMinutes: 180, isCompleted: true, daysAgo: 12 },
  { id: 'wf-10', referenceNumber: 'PO-2026-010', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 430, slaMinutes: 240, isCompleted: true, daysAgo: 18 }, // Breach
  { id: 'wf-11', referenceNumber: 'PO-2026-011', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 360, slaMinutes: 240, isCompleted: false, daysAgo: 5 }, // Overdue pending
  { id: 'wf-12', referenceNumber: 'PO-2026-012', department: 'Finance & Accounting', stepType: 'Legal Review', durationMinutes: 520, slaMinutes: 300, isCompleted: true, daysAgo: 22 }, // Breach
  { id: 'wf-13', referenceNumber: 'PO-2026-013', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 175, slaMinutes: 240, isCompleted: true, daysAgo: 28 },
  { id: 'wf-14', referenceNumber: 'PO-2026-014', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 295, slaMinutes: 240, isCompleted: false, daysAgo: 4 }, // Overdue pending
  { id: 'wf-15', referenceNumber: 'PO-2026-015', department: 'Finance & Accounting', stepType: 'Director Sign-off', durationMinutes: 145, slaMinutes: 180, isCompleted: true, daysAgo: 45 },
  { id: 'wf-16', referenceNumber: 'PO-2026-016', department: 'Finance & Accounting', stepType: 'Finance Approval', durationMinutes: 260, slaMinutes: 240, isCompleted: false, daysAgo: 3 }, // Overdue pending

  // Legal & Compliance (specialized review, significant tail delays on complex contracts)
  { id: 'wf-17', referenceNumber: 'CTR-2026-001', department: 'Legal & Compliance', stepType: 'Dept Head Review', durationMinutes: 45, slaMinutes: 120, isCompleted: true, daysAgo: 3 },
  { id: 'wf-18', referenceNumber: 'CTR-2026-002', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 210, slaMinutes: 300, isCompleted: true, daysAgo: 6 },
  { id: 'wf-19', referenceNumber: 'CTR-2026-003', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 510, slaMinutes: 300, isCompleted: true, daysAgo: 8 }, // Breach
  { id: 'wf-20', referenceNumber: 'CTR-2026-004', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 340, slaMinutes: 300, isCompleted: false, daysAgo: 5 }, // Overdue pending
  { id: 'wf-21', referenceNumber: 'CTR-2026-005', department: 'Legal & Compliance', stepType: 'Director Sign-off', durationMinutes: 55, slaMinutes: 180, isCompleted: true, daysAgo: 10 },
  { id: 'wf-22', referenceNumber: 'CTR-2026-006', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 320, slaMinutes: 300, isCompleted: false, daysAgo: 4 }, // Overdue pending
  { id: 'wf-23', referenceNumber: 'CTR-2026-007', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 195, slaMinutes: 300, isCompleted: false, daysAgo: 2 },
  { id: 'wf-24', referenceNumber: 'CTR-2026-008', department: 'Legal & Compliance', stepType: 'Dept Head Review', durationMinutes: 105, slaMinutes: 120, isCompleted: true, daysAgo: 19 },
  { id: 'wf-25', referenceNumber: 'CTR-2026-009', department: 'Legal & Compliance', stepType: 'Legal Review', durationMinutes: 490, slaMinutes: 300, isCompleted: true, daysAgo: 25 }, // Breach
  { id: 'wf-26', referenceNumber: 'CTR-2026-010', department: 'Legal & Compliance', stepType: 'Director Sign-off', durationMinutes: 135, slaMinutes: 180, isCompleted: true, daysAgo: 55 },

  // Operations (consistent execution, low overdue count)
  { id: 'wf-27', referenceNumber: 'OPS-2026-001', department: 'Operations', stepType: 'Dept Head Review', durationMinutes: 35, slaMinutes: 120, isCompleted: true, daysAgo: 1 },
  { id: 'wf-28', referenceNumber: 'OPS-2026-002', department: 'Operations', stepType: 'Dept Head Review', durationMinutes: 45, slaMinutes: 120, isCompleted: false, daysAgo: 1 },
  { id: 'wf-29', referenceNumber: 'OPS-2026-003', department: 'Operations', stepType: 'Finance Approval', durationMinutes: 160, slaMinutes: 240, isCompleted: true, daysAgo: 5 },
  { id: 'wf-30', referenceNumber: 'OPS-2026-004', department: 'Operations', stepType: 'Director Sign-off', durationMinutes: 60, slaMinutes: 180, isCompleted: true, daysAgo: 7 },
  { id: 'wf-31', referenceNumber: 'OPS-2026-005', department: 'Operations', stepType: 'Dept Head Review', durationMinutes: 50, slaMinutes: 120, isCompleted: false, daysAgo: 2 },
  { id: 'wf-32', referenceNumber: 'OPS-2026-006', department: 'Operations', stepType: 'Finance Approval', durationMinutes: 175, slaMinutes: 240, isCompleted: false, daysAgo: 2 },
  { id: 'wf-33', referenceNumber: 'OPS-2026-007', department: 'Operations', stepType: 'Director Sign-off', durationMinutes: 70, slaMinutes: 180, isCompleted: false, daysAgo: 1 },
  { id: 'wf-34', referenceNumber: 'OPS-2026-008', department: 'Operations', stepType: 'Dept Head Review', durationMinutes: 40, slaMinutes: 120, isCompleted: true, daysAgo: 16 },
  { id: 'wf-35', referenceNumber: 'OPS-2026-009', department: 'Operations', stepType: 'Director Sign-off', durationMinutes: 85, slaMinutes: 180, isCompleted: true, daysAgo: 29 },
  { id: 'wf-36', referenceNumber: 'OPS-2026-010', department: 'Operations', stepType: 'Finance Approval', durationMinutes: 255, slaMinutes: 240, isCompleted: true, daysAgo: 60 }, // Breach

  // Human Resources (efficient turnaround, minimal breaches)
  { id: 'wf-37', referenceNumber: 'HR-2026-001', department: 'Human Resources', stepType: 'Dept Head Review', durationMinutes: 30, slaMinutes: 120, isCompleted: true, daysAgo: 2 },
  { id: 'wf-38', referenceNumber: 'HR-2026-002', department: 'Human Resources', stepType: 'Dept Head Review', durationMinutes: 40, slaMinutes: 120, isCompleted: false, daysAgo: 1 },
  { id: 'wf-39', referenceNumber: 'HR-2026-003', department: 'Human Resources', stepType: 'Director Sign-off', durationMinutes: 50, slaMinutes: 180, isCompleted: true, daysAgo: 4 },
  { id: 'wf-40', referenceNumber: 'HR-2026-004', department: 'Human Resources', stepType: 'Director Sign-off', durationMinutes: 60, slaMinutes: 180, isCompleted: false, daysAgo: 2 },
  { id: 'wf-41', referenceNumber: 'HR-2026-005', department: 'Human Resources', stepType: 'Dept Head Review', durationMinutes: 35, slaMinutes: 120, isCompleted: false, daysAgo: 1 },
  { id: 'wf-42', referenceNumber: 'HR-2026-006', department: 'Human Resources', stepType: 'Dept Head Review', durationMinutes: 110, slaMinutes: 120, isCompleted: true, daysAgo: 20 },
  { id: 'wf-43', referenceNumber: 'HR-2026-007', department: 'Human Resources', stepType: 'Director Sign-off', durationMinutes: 75, slaMinutes: 180, isCompleted: true, daysAgo: 38 },
];

export interface SLAFilterOptions {
  department?: string;
  stepType?: string;
  dateRange?: string;
}

export interface AggregatedSLAData {
  kpis: {
    activePending: number;
    currentlyOverdue: number;
    overallBreachRatePct: number;
    medianTurnaroundMinutes: number;
  };
  stepMetrics: Array<{
    stepType: string;
    p50Minutes: number;
    p90Minutes: number;
    targetSla: number;
    breachRatePct: number;
    totalCount: number;
  }>;
  departmentRankings: Array<{
    department: string;
    activeQueue: number;
    overdueCount: number;
    breachRatePct: number;
    totalCount: number;
  }>;
  totalRecordCount: number;
  selectedDepartment: string;
  selectedStepType: string;
  selectedRange: string;
}

/**
 * Calculates median (P50) and 90th percentile (P90) from an array of numbers.
 */
function calculatePercentiles(values: number[]): { p50: number; p90: number } {
  if (values.length === 0) return { p50: 0, p90: 0 };
  const sorted = [...values].sort((a, b) => a - b);
  
  // P50 calculation
  const mid = Math.floor(sorted.length / 2);
  const p50 = sorted.length % 2 !== 0 ? sorted[mid] : Math.round((sorted[mid - 1] + sorted[mid]) / 2);
  
  // P90 calculation (nearest rank)
  const p90Index = Math.min(Math.ceil(sorted.length * 0.9) - 1, sorted.length - 1);
  const p90 = sorted[p90Index];

  return { p50, p90 };
}

/**
 * Filters the deterministic dataset and computes analytical aggregations.
 */
export function getFilteredSLAAnalytics(filters: SLAFilterOptions): AggregatedSLAData {
  const department = filters.department && filters.department !== 'All Departments' ? filters.department : undefined;
  const stepType = filters.stepType && filters.stepType !== 'All Steps' ? filters.stepType : undefined;
  const dateRange = filters.dateRange || '30d';

  const rangeObj = DATE_RANGES.find((r) => r.value === dateRange) || DATE_RANGES[1]; // default 30d
  const maxDays = rangeObj.maxDays;

  // Filter records
  const filtered = SAMPLE_WORKFLOW_RECORDS.filter((rec) => {
    if (rec.daysAgo > maxDays) return false;
    if (department && rec.department !== department) return false;
    if (stepType && rec.stepType !== stepType) return false;
    return true;
  });

  const totalRecordCount = filtered.length;

  // Compute KPIs
  const pendingRecords = filtered.filter((r) => !r.isCompleted);
  const activePending = pendingRecords.length;
  const currentlyOverdue = pendingRecords.filter((r) => r.durationMinutes > r.slaMinutes).length;

  const allBreachedCount = filtered.filter((r) => r.durationMinutes > r.slaMinutes).length;
  const overallBreachRatePct = totalRecordCount > 0
    ? Number(((allBreachedCount / totalRecordCount) * 100).toFixed(1))
    : 0;

  const allDurations = filtered.map((r) => r.durationMinutes);
  const { p50: medianTurnaroundMinutes } = calculatePercentiles(allDurations);

  // Compute Step-level metrics
  const activeStepTypes = stepType
    ? [stepType]
    : ['Dept Head Review', 'Finance Approval', 'Legal Review', 'Director Sign-off'];

  const stepMetrics = activeStepTypes.map((step) => {
    const stepRecords = filtered.filter((r) => r.stepType === step);
    const durations = stepRecords.map((r) => r.durationMinutes);
    const { p50, p90 } = calculatePercentiles(durations);
    const breaches = stepRecords.filter((r) => r.durationMinutes > r.slaMinutes).length;
    const breachRatePct = stepRecords.length > 0
      ? Number(((breaches / stepRecords.length) * 100).toFixed(1))
      : 0;

    return {
      stepType: step,
      p50Minutes: p50,
      p90Minutes: p90,
      targetSla: SLA_TARGETS[step] || 180,
      breachRatePct,
      totalCount: stepRecords.length,
    };
  });

  // Compute Department rankings
  const activeDepartments = department
    ? [department]
    : ['Finance & Accounting', 'Legal & Compliance', 'Operations', 'Human Resources'];

  const departmentRankings = activeDepartments.map((dept) => {
    const deptRecords = filtered.filter((r) => r.department === dept);
    const deptPending = deptRecords.filter((r) => !r.isCompleted);
    const deptOverdue = deptPending.filter((r) => r.durationMinutes > r.slaMinutes).length;
    const deptBreaches = deptRecords.filter((r) => r.durationMinutes > r.slaMinutes).length;
    const breachRatePct = deptRecords.length > 0
      ? Number(((deptBreaches / deptRecords.length) * 100).toFixed(1))
      : 0;

    return {
      department: dept,
      activeQueue: deptPending.length,
      overdueCount: deptOverdue,
      breachRatePct,
      totalCount: deptRecords.length,
    };
  }).sort((a, b) => b.overdueCount - a.overdueCount || b.activeQueue - a.activeQueue);

  return {
    kpis: {
      activePending,
      currentlyOverdue,
      overallBreachRatePct,
      medianTurnaroundMinutes,
    },
    stepMetrics,
    departmentRankings,
    totalRecordCount,
    selectedDepartment: filters.department || 'All Departments',
    selectedStepType: filters.stepType || 'All Steps',
    selectedRange: dateRange,
  };
}
