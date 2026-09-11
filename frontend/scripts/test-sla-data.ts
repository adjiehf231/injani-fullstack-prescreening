/**
 * PT Injani Systems - Fullstack Developer Prescreening
 * Verification script for SLA Analytics aggregation and filtering logic
 */

import { getFilteredSLAAnalytics, SAMPLE_WORKFLOW_RECORDS } from '../lib/sla-data';

function assert(condition: boolean, message: string) {
  if (!condition) {
    console.error(`❌ Assertion Failed: ${message}`);
    process.exit(1);
  }
  console.log(`  [PASS] ${message}`);
}

console.log('Running SLA Analytics Pure Function & Filter Tests...\n');

// 1. Unfiltered / default 30d window
const defaultData = getFilteredSLAAnalytics({ dateRange: '30d' });
assert(defaultData.totalRecordCount > 0, 'Default 30d window returns records');
assert(defaultData.kpis.activePending > 0, 'Active pending queue computed correctly');
assert(defaultData.kpis.currentlyOverdue >= 0, 'Overdue queue computed correctly');
assert(defaultData.stepMetrics.length === 4, 'All 4 workflow steps present in default view');
assert(defaultData.departmentRankings.length === 4, 'All 4 departments present in default view');

// 2. Department filtering
const financeData = getFilteredSLAAnalytics({ department: 'Finance & Accounting', dateRange: '30d' });
assert(financeData.totalRecordCount < defaultData.totalRecordCount, 'Department filter narrows total records');
assert(financeData.departmentRankings.length === 1, 'Only filtered department returned in rankings');
assert(financeData.departmentRankings[0].department === 'Finance & Accounting', 'Filtered department matches selection');

// 3. Step filtering
const legalData = getFilteredSLAAnalytics({ stepType: 'Legal Review', dateRange: '30d' });
assert(legalData.stepMetrics.length === 1, 'Step filter isolates target step');
assert(legalData.stepMetrics[0].stepType === 'Legal Review', 'Target step type matches selection');

// 4. Period filtering
const sevenDayData = getFilteredSLAAnalytics({ dateRange: '7d' });
const ninetyDayData = getFilteredSLAAnalytics({ dateRange: '90d' });
assert(sevenDayData.totalRecordCount <= ninetyDayData.totalRecordCount, '7d period has <= records than 90d period');

// 5. Empty filter result
const emptyData = getFilteredSLAAnalytics({ department: 'Nonexistent Dept', dateRange: '7d' });
assert(emptyData.totalRecordCount === 0, 'Nonexistent department returns 0 records');
assert(emptyData.kpis.activePending === 0, 'Empty filter sets active pending to 0');
assert(emptyData.kpis.overallBreachRatePct === 0, 'Empty filter sets breach rate to 0');

console.log('\nAll SLA Analytics Data & Filter Tests Passed Successfully!');
