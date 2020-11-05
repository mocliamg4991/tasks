# -*- coding: utf-8 -*-
from django.core.management import BaseCommand
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from tasks.models import TodoItem

class Command(BaseCommand):
	help = u"Read tasks from file (one line = one task)and save them to db"
	
	def add_arguments(self, parser):
		parser.add_argument('--file', dest='input_file', type=str)

	def handle(self, *args, **options):
		now = datetime.now(timezone.utc)
		with open (options['input_file'], 'r', encoding="utf-8") as f:
			for line in f:
				task = TodoItem.objects.create(description=line)
				task.save()
				print('Добавлена задача: ', task.description)
