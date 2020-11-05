from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
	path('', views.index, name='index'),
	path('complete/<int:uid>', views.complete_task, name='complete'),
	path('delete/<int:uid>', views.delete_task, name='delete'),
	# ссылки для шаблонов основанных на функциях
	# path('list/', views.tasks_list, name='list'),
	# path('create/', views.task_create, name = 'create'),
	# path('add-task/', views.add_task, name = 'api-add-task'),

	# ссылки для шаблонов основанных на классах
	path("list/", views.TaskListView.as_view(), name="list"),
	path("create/", views.TaskCreateView.as_view(), name="create"),
	path("details/<int:pk>", views.TaskDetailsView.as_view(),\
	name="details"),
	path("edit/<int:pk>", views.TaskEditView.as_view(), name="edit"),
	path("export/", views.TaskExportView.as_view(), name="export"),
]

