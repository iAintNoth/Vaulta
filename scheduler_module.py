
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class BackupScheduler:
    def __init__(self, job_func):
        self.scheduler = BackgroundScheduler(daemon=True)
        self.job_func = job_func

    def start_daily(self, hour: int, minute: int):
        try:
            self.scheduler.remove_all_jobs()
        except Exception:
            pass
        trigger = CronTrigger(hour=hour, minute=minute)
        self.scheduler.add_job(self.job_func, trigger, id="daily_backup", replace_existing=True)
        if not self.scheduler.running:
            self.scheduler.start()
