from django.core.paginator import Paginator
from django.shortcuts import render
from authentication.models import Teacher


def teacher_view(request):
    teacher_list = Teacher.objects.select_related('user').all()
    paginator = Paginator(teacher_list, 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'teachers': page_obj,
    }
    return render(request, 'instructors.html', context)
