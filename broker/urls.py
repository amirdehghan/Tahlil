from django.urls import path,re_path
from django.conf.urls import url
from . import views, api
from broker.views import student, instructor

urlpatterns = [
    path('', views.home, name='home'),
    path('student/', views.student_home, name='student_home'),
    path('apply/<int:id>/', views.application, name='apply_form'),
    path('apply/success/', views.application_success, name='application_success'),
    path('instructor/', views.instructor_home, name='instructor_home'),
    path('instructor/form/new/', views.instructor_create_form, name='create_form'),
    path('instructor/form/<int:id>/', views.instructor_form_detail, name='instructor_form_detail'),
    path('instructor/form/<int:pk>/delete', views.FormDeleteView.as_view(), name='instructor_form_delete'),
    path('instructor/res/<int:id>/', views.instructor_response_detail, name='instructor_response_detail'),
    path('api/change_response_state', api.change_response_state, name='change_response_state'),
    path('student/view_profile/', student.view_profile, name='view_profile'),
    path('student/update_profile/', student.update_profile.as_view(), name='update_profile'),
    path('instructor/view_profile/', instructor.view_profile, name="view_instructor_profile"),
    path('instructor/update_profile/', instructor.update_profile.as_view(), name="update_instructor_profile"),
    path('instructor/view_student_profile/<int:pk>', student.view_student_profile, name='view_student_profile'),
    path('student/view_instructor_profile/<int:pk>', instructor.view_instructor_profile, name='student_view_instructor_profile'),
]
