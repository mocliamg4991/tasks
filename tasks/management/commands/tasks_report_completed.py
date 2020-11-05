# coding: utf-8
from django.core.management import BaseCommand
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from tasks.models import TodoItem
class Command(BaseCommand):
	help = u"Displays all tasks completed in the last `days` days\
			(default=3 days)"
	
	def add_arguments(self, parser):
		parser.add_argument('--days', dest='days', type=int, default=3)
	
	def handle(self, *args, **options):
		now = datetime.now(timezone.utc)
		for t in TodoItem.objects.filter(is_completed=True):
			if (now - t.created).days < options['days']:
				print("Задачи которые были выполнены за последние ",\
					options['days'],' дней : ', t,' | ', t.created)
