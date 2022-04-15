from apps.notification.services.message import NotificationMessage
import django.conf
from apps.users.models import User

class SendReportStaffEveryWeek(NotificationMessage):
    def __init__(self, user, staff):
        self._user = user
        self.staff = staff

    @property
    def user(self):
        return self._user

    @property
    def payload(self):
        assignee = self._user
        assignee_first_name = assignee.first_name
        staffs = self.staff
        return {
            "staffs": staffs,
            "assignee_first_name": assignee_first_name,
            "preview_link": django.conf.settings.FRONTEND_URL + "/schedule",
        }

    @property
    def verb(self) -> str:
        return "Send mail to notify the schedule of staff every week"

    @property
    def title(self) -> str:
        assignee = self._user
        return "Send mail to notify the schedule of staff every week"

    @property
    def content(self):
        assignee = self._user
        return "{0} {1} <{2}> Check your schedule staff.".format(
            assignee.first_name,
            assignee.last_name,
            assignee.email,
        )

    @property
    def template(self):
        return "reports/sending_total_income__to_admin.html"