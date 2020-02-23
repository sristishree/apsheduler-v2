from django.urls import include, path
from rest_framework import routers
from . import views
from . import scheduler

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('schedule/', views.TaskAPIView.as_view(), name='create-task'),
    path('schedule/status/', views.sched_state, name='scheduler-state'),
    path('schedule/tasks/',views.sched_list, name='scheduler-tasks' )
]


# # scheduler.start()
# import logging
# logging.basicConfig(level="DEBUG")