from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from core.models import Category, Report


class Command(BaseCommand):
    help = "Seed the database with sample categories and 10 reports."

    def handle(self, *args, **options):
        with transaction.atomic():
            user = self._get_or_create_demo_user()
            categories = self._get_or_create_categories()
            created_reports = self._create_reports(user, categories)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_reports)} reports successfully."))

    def _get_or_create_demo_user(self):
        user, created = User.objects.get_or_create(
            email="demo@foundly.local",
            defaults={
                "username": "demo_user",
                "first_name": "Demo",
                "last_name": "User",
            },
        )
        if created:
            user.set_password("demo12345")
            user.save(update_fields=["password"])
            self.stdout.write(self.style.SUCCESS("Created demo user: demo@foundly.local / demo12345"))
        return user

    def _get_or_create_categories(self):
        category_names = [
            "Electronics",
            "Documents",
            "Accessories",
            "Keys",
            "Clothing",
            "Bags",
            "Stationery",
            "Phones",
        ]

        categories = {}
        for name in category_names:
            category, _ = Category.objects.get_or_create(title=name)
            categories[name] = category
        return categories

    def _create_reports(self, user, categories):
        sample_reports = [
            {
                "report_type": "lost",
                "status": "open",
                "category": categories["Electronics"],
                "item_name": "iPhone 13",
                "colour": "Midnight",
                "description": "Lost an iPhone 13 with a black case near the cafeteria.",
                "location": "University cafeteria",
                "date_incident": date.today() - timedelta(days=2),
            },
            {
                "report_type": "found",
                "status": "open",
                "category": categories["Keys"],
                "item_name": "Set of car keys",
                "colour": "Silver",
                "description": "Found a set of car keys with a Toyota fob on a bench.",
                "location": "Central park bench",
                "date_incident": date.today() - timedelta(days=1),
            },
            {
                "report_type": "lost",
                "status": "claimed",
                "category": categories["Documents"],
                "item_name": "Student ID card",
                "colour": "Blue",
                "description": "Lost my student ID card inside the library.",
                "location": "Main library",
                "date_incident": date.today() - timedelta(days=6),
            },
            {
                "report_type": "found",
                "status": "resolved",
                "category": categories["Bags"],
                "item_name": "Black backpack",
                "colour": "Black",
                "description": "Found a black backpack with a laptop charger in it.",
                "location": "Bus terminal",
                "date_incident": date.today() - timedelta(days=4),
            },
            {
                "report_type": "lost",
                "status": "open",
                "category": categories["Accessories"],
                "item_name": "Wristwatch",
                "colour": "Brown",
                "description": "Brown leather wristwatch dropped around the sports complex.",
                "location": "Sports complex",
                "date_incident": date.today() - timedelta(days=8),
            },
            {
                "report_type": "found",
                "status": "open",
                "category": categories["Clothing"],
                "item_name": "Grey hoodie",
                "colour": "Grey",
                "description": "Grey hoodie found on a classroom chair after lectures.",
                "location": "Engineering block",
                "date_incident": date.today() - timedelta(days=3),
            },
            {
                "report_type": "lost",
                "status": "open",
                "category": categories["Phones"],
                "item_name": "Samsung Galaxy S22",
                "colour": "Phantom Black",
                "description": "Phone disappeared after a taxi ride downtown.",
                "location": "Taxi stand",
                "date_incident": date.today() - timedelta(days=10),
            },
            {
                "report_type": "found",
                "status": "claimed",
                "category": categories["Stationery"],
                "item_name": "Notebook",
                "colour": "Red",
                "description": "Red notebook with handwritten notes left in the lecture hall.",
                "location": "Lecture hall 2",
                "date_incident": date.today() - timedelta(days=5),
            },
            {
                "report_type": "lost",
                "status": "open",
                "category": categories["Bags"],
                "item_name": "Laptop sleeve",
                "colour": "Navy",
                "description": "Navy laptop sleeve with a charger and USB drive inside.",
                "location": "Coworking space",
                "date_incident": date.today() - timedelta(days=7),
            },
            {
                "report_type": "found",
                "status": "resolved",
                "category": categories["Documents"],
                "item_name": "Passport pouch",
                "colour": "Green",
                "description": "Found a green passport pouch near the reception desk.",
                "location": "Hotel reception",
                "date_incident": date.today() - timedelta(days=9),
            },
        ]

        created = []
        for data in sample_reports:
            report, was_created = Report.objects.get_or_create(
                user=user,
                item_name=data["item_name"],
                location=data["location"],
                defaults={
                    "report_type": data["report_type"],
                    "status": data["status"],
                    "category": data["category"],
                    "colour": data["colour"],
                    "description": data["description"],
                    "date_incident": data["date_incident"],
                },
            )
            if was_created:
                created.append(report)

        return created
