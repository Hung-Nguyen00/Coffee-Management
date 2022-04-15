from django.core.management.base import BaseCommand
from faker import Faker

from apps.notification import choices
from apps.notification.models import Category, Message
from apps.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            dest="username_or_email",
            type=str,
            help="Existed username or email.",
        )
        parser.add_argument(
            "notification_number",
            type=int,
            help="Generate number of fake notifications.",
        )

    def handle(self, *args, **options):
        if options["username_or_email"] and options["notification_number"]:
            if int(options["notification_number"] <= 0):
                self.stdout.write(self.style.NOTICE("Contact number must be from 1."))
                return

            if (
                not User.objects.filter(username=options["username_or_email"]).exists()
                and not User.objects.filter(email=options["username_or_email"]).exists()
            ):
                self.stdout.write(self.style.NOTICE("Username or email not exists."))
                return
            fake = Faker()
            user = None

            if User.objects.filter(username=options["username_or_email"]).exists():
                user = User.objects.get(username=options["username_or_email"])
            if User.objects.filter(email=options["username_or_email"]).exists():
                user = User.objects.get(email=options["username_or_email"])

            category = Category.objects.create(name=fake.sentence(), description=fake.text())
            for index in range(int(options["notification_number"])):
                Message.objects.create(
                    category=category,
                    verb=fake.word(),
                    user=user,
                    topic=fake.sentence(),
                    title=fake.sentence(),
                    content=fake.text(),
                    status=choices.MESSAGE_STATUS_SENT,
                )
