from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from tasks.forms import AddTaskForm, TodoItemForm, TodoItemExportForm
from tasks.models import TodoItem
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

@login_required
def index(request):
	return HttpResponse("Примитивный ответ из приложения tasks")
# Create your views here.

# def tasks_list(request):
# 	all_tasks = TodoItem.objects.all()
# 	return render(request, 'tasks/list.html', {'tasks':all_tasks})

def complete_task(request, uid):
	task = TodoItem.objects.get(id=uid)
	task.is_completed = True
	task.save()
	return HttpResponse("OK")

def delete_task(request, uid):
	deleted_task = TodoItem.objects.get(id=uid).delete()
	messages.success(request, "Задача удалена")
	return HttpResponseRedirect(reverse("tasks:list"))

# def task_create(request):
# 	if request.method == "POST":	
# 		form = TodoItemForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return redirect("tasks:list")
# 	else:
# 		form = TodoItemForm()

# 	return render(request, "tasks/create.html", {"form": form})

# def add_task(request):
# 	if request.method == "POST":
# 		desc = request.POST["description"]
# 		t = TodoItem(description=desc)
# 		t.save()
# 	return redirect("tasks:list")

class TaskListView(LoginRequiredMixin,ListView):
	model = TodoItem
	context_object_name = "tasks"
	template_name = "tasks/list.html"

	def get_queryset(self):
		u = self.request.user
		return u.tasks.all()

class TaskCreateView(View):
	def my_render(self, request, form):
		return render(request, "tasks/create.html", {"form": form})
	def post(self, request, *args, **kwargs):
		form = TodoItemForm(request.POST)
		if form.is_valid():
			new_task = form.save(commit=False)
			new_task.owner = request.user
			new_task.save()
			return HttpResponseRedirect(reverse("tasks:list"))
		return self.my_render(request, form)
	def get(self, request, *args, **kwargs):
		form = TodoItemForm()
		return self.my_render(request, form)

class TaskDetailsView(DetailView):
	model = TodoItem
	template_name = 'tasks/details.html'

class TaskEditView(LoginRequiredMixin, View):
	def my_render(self, request, form, t):
		return render(request, "tasks/edit.html", {"form": form, "task": t})
	def post(self, request, pk,*args, **kwargs):
		t = TodoItem.objects.get(id = pk)
		form = TodoItemForm(request.POST, instance=t)
		if form.is_valid():
			new_task = form.save(commit=False)
			new_task.owner = request.user
			new_task.save()
			return HttpResponseRedirect(reverse("tasks:list"))

		return self.my_render(request, form, t)
	def get(self, request, pk, *args, **kwargs):
		t = TodoItem.objects.get(id=pk)
		form = TodoItemForm(instance=t)
		return self.my_render(request, form, t)

class TaskExportView(LoginRequiredMixin, View):
	
	def generate_body(self, user, priorities):
		q = Q()
		if priorities["prio_high"]:
			q = q | Q(priority=TodoItem.PRIORITY_HIGH)
		if priorities["prio_med"]:
			q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
		if priorities["prio_low"]:
			q = q | Q(priority=TodoItem.PRIORITY_LOW)
		
		tasks = TodoItem.objects.filter(owner=user).filter(q).all()
		
		body = "Ваши задачи и приоритеты:\n"
		for t in list(tasks):
			if t.is_completed:
				body += f"[x] {t.description} ({t.get_priority_display()})\n"
			else:
				body += f"[ ] {t.description} ({t.get_priority_display()})\n"
		return body
	
	def post(self, request, *args, **kwargs):
		form = TodoItemExportForm(request.POST)
		if form.is_valid():
			email = request.user.email
			body = self.generate_body(request.user, form.cleaned_data) 
			send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
			messages.success(
				request, "Задачи были отправлены на почту %s" % email)
		else:
			messages.error(request, "Что-то пошло не так, попробуйте ещё раз")
		return redirect(reverse("tasks:list"))
	
	def get(self, request, *args, **kwargs):
		form = TodoItemExportForm()
		return render(request, "tasks/export.html", {"form": form})

