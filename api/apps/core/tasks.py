# from celery.schedules import crontab
# from celery.task import PeriodicTask, Task

# class TestPeriodicTask(PeriodicTask):
#     # Execute every minute
#     run_every = crontab(minute=1)

#     def run(self):
#         print("Periodic Task is running ....")


# class TestAddTask(Task):
#     name = "core_test_add_task"

#     def run(self, a, b, **kwargs):
#         return a + b
