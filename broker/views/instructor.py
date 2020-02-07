from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from authentication.forms import InstructorForm
from django.urls import reverse

from ..models import *
from ..forms import render_form

@login_required()
def instructor_home(request):
    user = request.user
    forms = user.instructor.forms.all()
    return render(request, 'broker/instructor/home.html', context={'user':user, 'forms':forms })


@login_required()
def instructor_form_detail(request, id):
    form = ApplicationForm.objects.filter(id=id).first()
    # if isinstance(form, EmptyQuerySet):
    #     # todo: error
    #     pass
    #responses = [answer.response for answer in form.questions.first().answers.all()]
    responses = ApplicationResponse.objects.filter(answers__question__form = form).distinct()
    return render(request, 'broker/instructor/form.html', context={'form':form , 'responses':responses})


@login_required()
def instructor_response_detail(request, id):
    user = request.user
    response = ApplicationResponse.objects.filter(id=id).first()
    form = response.get_form()
    html = render_form(form, response, False)
    # if isinstance(response, EmptyQuerySet):
    #     # todo: error
    #     pass
    return render(request, 'broker/instructor/response.html', context={'html':html, 'response':response})

# TODO move this shit to API
@csrf_exempt
@login_required()
def instructor_create_form(request):
    if request.method == "GET":
        return render(request, 'broker/instructor/form_creation.html', {})
    else:
        form = ApplicationForm(creator=request.user.instructor)
        form.release_date = datetime.now()
        form.deadline = request.POST["deadline"]
        form.course_id = request.POST["course"]
        form.info = request.POST["info"]
        form.save()
        for i in range(1, int(request.POST["length"]) + 1):
            if request.POST["q_%d_type" % i] == "textual":
                q = TextualQuestion(form=form, question=request.POST["q_%d_body" % i], number=i)
                q.save()

        return HttpResponse()

@login_required()
def view_profile(request):
    instructor = request.user.instructor
    return render(request, 'broker/instructor/view_instructor_profile.html', context={'instructor': instructor})

@method_decorator([login_required], name='dispatch')
class update_profile(UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = 'broker/instructor/update_instructor_profile.html'

    def get_success_url(self):
        return reverse('instructor_home')

    def get_object(self, queryset=None):
        return self.request.user.instructor

@login_required()
def view_student_profile(request, pk):
    instructor = Instructor.objects.get(instructor_id=pk)
    return render(request, 'broker/instructor/view_instructor_profile.html', context={'instructor': instructor})
