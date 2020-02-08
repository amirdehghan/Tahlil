from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template import Template
from ..forms import render_form, save_form
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from authentication.forms import StudentForm
from django.urls import reverse



from broker.models import *
from authentication.decorators import active_required

@login_required()
@active_required()
def student_home(request):
    student = request.user.student
    forms = ApplicationForm.objects.exclude(responses__owner=student)
    responses = student.responses.all()

    return render(request, 'broker/student/home.html', context={'user':request.user, 'forms':forms, 'responses': responses})

@login_required()
@active_required()
def application(request, id):
    form = ApplicationForm.objects.get(id=id)

    if request.method == "GET":
        form_template = Template(render_form(form, editable=True))
        form_html = form_template.render(RequestContext(request))

        return render(request, 'broker/student/application.html', context={'form': form_html})
    else:
        response = ApplicationResponse(owner=request.user.student, state = 'p', form=form)
        response.save()
        save_form(form, request.POST, response)

        return redirect('application_success')

def application_success(request):
    return render(request, 'broker/student/success.html', {'message' : 'Your Application Successfully Submited.'})


@login_required()
@active_required()
def view_profile(request):
    student = request.user.student
    return render(request, 'broker/student/view_student_profile.html', context={'student': student})

@method_decorator([login_required, active_required], name='dispatch')
class update_profile(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'broker/student/update_profile.html'

    def get_success_url(self):
        return reverse('student_home')

    def get_object(self, queryset=None):
        return self.request.user.student


@login_required()
@active_required()
def view_student_profile(request, pk):
    student = Student.objects.get(student_id=pk)
    return render(request, 'broker/student/view_student_profile.html', context={'student': student})