# coding: utf-8
import collections
from django.core.management import BaseCommand
from tasks.models import TodoItem
from django.contrib.auth.models import User
class Command(BaseCommand):
	help = u"Displays top with most tasks on user\
			(default=25)"

	def add_arguments(self, parser):
		parser.add_argument('--user_count', dest='user_count', type=int, default=25)
	
	def handle(self, *args, **options):
		top = {}
		for u in User.objects.all():
			n = 0
			for t in u.tasks.all():
				n+=1
			dict_1 = {u:n}
			top.update(dict_1)

		print ('топ',options['user_count'], 'пользователей')	
		for k,v in sorted(top.items(),key = lambda count:count[1],\
			reverse=True)[:options['user_count']]:
			print('Пользователь',k,'| количество задач - ',v)
		print('_______________________________________________________')
		User_5 = sorted(top.items(),key = lambda count:count[1],\
				reverse=True)[4]
		print ('Пользователь, который на пятом месте по числу задач - ',\
			User_5)
		print('_______________________________________________________')
		n = 0	
		for t in TodoItem.objects.filter(is_completed=True):
			n +=1
		print('Общее количество выполненных задач - ',n)
		
		print('_______________________________________________________')
		uN = 0
		for u in User.objects.all():
			n = 0
			for t in u.tasks.filter(is_completed=False):
				n+=1
			if n<20:
				uN +=1	
		print ('Пользователей, у которых число невыполненных задач меньше 20 - ', uN)
		print('_______________________________________________________')
		top = {}
		for u in User.objects.all():
			n = 0
			for t in u.tasks.filter(is_completed=False):
				n+=1
			dict_1 = {u:n}
			top.update(dict_1)
		User_2 = sorted(top.items(),key = lambda count:count[1],\
				reverse=True)[2]
		print ('Пользователь, который на втором месте по числу не выполненных задач - ',\
			User_2)






