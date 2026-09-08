"""
PT Injani Systems - Fullstack Developer Prescreening
Q6(b): Async Background Job Manager & Real-Time Progress Tracking
"""

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from app.schemas.task import TaskStatus, TaskProgressResponse


class AsyncTaskManager:
    """
    Manages non-blocking async background tasks and maintains state/progress.
    In local/single-node development: in-memory state dictionary.
    In distributed production: backed by Redis Hashes (HSET task:{id} progress 60).
    """

    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def create_task(self, task_type: str = "report_generation") -> str:
        task_id = f"task_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        self._tasks[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "status": TaskStatus.PENDING,
            "progress_percent": 0,
            "current_step": "Task queued in background worker",
            "result": None,
            "error": None,
            "created_at": now,
            "updated_at": now,
        }
        return task_id

    def update_progress(
        self,
        task_id: str,
        status: TaskStatus,
        progress_percent: int,
        current_step: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> None:
        if task_id in self._tasks:
            self._tasks[task_id].update({
                "status": status,
                "progress_percent": progress_percent,
                "current_step": current_step,
                "result": result,
                "error": error,
                "updated_at": datetime.now(timezone.utc).isoformat()
            })

    def get_task_status(self, task_id: str) -> Optional[TaskProgressResponse]:
        raw = self._tasks.get(task_id)
        if not raw:
            return None
        return TaskProgressResponse(**raw)

    async def execute_mock_pdf_generation(self, task_id: str, order_id: str):
        """Simulates multi-stage async PDF generation reporting progress milestones."""
        try:
            # Stage 1: Fetch data (20%)
            self.update_progress(task_id, TaskStatus.IN_PROGRESS, 20, "Fetching order and ledger records from PostgreSQL")
            await asyncio.sleep(0.05)

            # Stage 2: Render PDF template (60%)
            self.update_progress(task_id, TaskStatus.IN_PROGRESS, 60, "Compiling Weasyprint / Puppeteer PDF template")
            await asyncio.sleep(0.05)

            # Stage 3: Upload to Cloud Storage & sign URL (90%)
            self.update_progress(task_id, TaskStatus.IN_PROGRESS, 90, "Uploading PDF to Google Cloud Storage")
            await asyncio.sleep(0.05)

            # Stage 4: Finished (100%)
            result = {
                "download_url": f"https://storage.googleapis.com/injani-reports/{order_id}_summary.pdf",
                "file_size_bytes": 148200,
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
            self.update_progress(task_id, TaskStatus.COMPLETED, 100, "PDF report generated successfully", result=result)
        except Exception as exc:
            self.update_progress(task_id, TaskStatus.FAILED, 100, f"Failed during generation: {str(exc)}", error=str(exc))


# Global singleton instance for app lifespan
global_task_manager = AsyncTaskManager()
