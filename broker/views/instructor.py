from datetime import datetime, timedelta

from django.db.models.query import EmptyQuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, CreateView
from ..models import *
from ..forms import render_form
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from authentication.forms import InstructorForm
from authentication.decorators import active_required


@login_required()
def instructor_home(request):
    user = request.user
    forms = user.instructor.forms.all()
    return render(request, 'broker/instructor/home.html', context={'user':user, 'forms':forms })


@login_required()
def instructor_form_detail(request, id):
    form = ApplicationForm.objects.filter(id=id).first()

    if form is None:
        return redirect('instructor_home')

    #responses = [answer.response for answer in form.questions.first().answers.all()]
    responses = ApplicationResponse.objects.filter(form = form).distinct()
    return render(request, 'broker/instructor/form.html', context={'form':form , 'responses':responses})


@method_decorator([login_required], name='dispatch')
class FormDeleteView(DeleteView):
    model = ApplicationForm
    context_object_name = 'form'
    template_name = 'broker/instructor/form_delete.html'
    success_url = reverse_lazy('instructor_home')


    def get_queryset(self):
        return self.request.user.instructor.forms.all()


@login_required()
def instructor_response_detail(request, id):
    response = ApplicationResponse.objects.filter(id=id).first()
    if response is None:
        return redirect('instructor_home')

    form = response.get_form()
    html = render_form(form, response, False)

    return render(request, 'broker/instructor/response.html', context={'html':html, 'response':response})


@csrf_exempt
@login_required()
def instructor_create_form(request):
    if request.method == "GET":
        courses = Course.objects.filter(instructor=request.user.instructor)
        print(courses)
        return render(request, 'broker/instructor/form_creation.html', {'courses': courses})
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
def view_instructor_profile(request, pk):
    instructor = Instructor.objects.get(pk=pk)
    return render(request, 'broker/instructor/view_instructor_profile.html', context={'instructor': instructor})

@method_decorator([login_required], name='dispatch')
class CreateCourse(CreateView):
    model = Course
    fields = ('course_id', 'course_name', 'requirement', )
    template_name = 'broker/instructor/course_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        print(self.object)
        self.object.instructor = self.request.user.instructor
        self.object.save()
        print(self.object)

        return redirect('home')

@login_required()
@active_required()
def view_course(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'broker/instructor/view_course.html', context={'course': course})