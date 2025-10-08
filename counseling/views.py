
from django.shortcuts import render, redirect
from .forms import StudentCounselingForm
import logging
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

logger = logging.getLogger(__name__)


def counseling_form_view(request):
    if request.method == 'POST':
        # Debug CSRF tokens to help diagnose 'CSRF token incorrect' issues
        token_in_post = request.POST.get('csrfmiddlewaretoken')
        csrf_cookie = request.COOKIES.get('csrftoken') or request.COOKIES.get('csrf')
        header_token = request.META.get('HTTP_X_CSRFTOKEN') or request.META.get('HTTP_X_CSRF_TOKEN')
        logger.debug('CSRF tokens - POST token: %s', token_in_post)
        logger.debug('CSRF tokens - cookie token: %s', csrf_cookie)
        logger.debug('CSRF tokens - header token: %s', header_token)

        form = StudentCounselingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  # You can create a success.html or message
        else:
            # Log form errors for debugging
            logger.debug('Form is not valid. Errors: %s', form.errors.as_json())
    else:
        form = StudentCounselingForm()

    return render(request, 'index.html', {'form': form})
def success_view(request):
    return render(request, 'success.html')


@login_required
def approve_view(request, pk):
    from .models import StudentCounseling
    from django.shortcuts import get_object_or_404
    obj = get_object_or_404(StudentCounseling, pk=pk)

    # Derive role from user/groups (context processor provides same var to templates)
    role = ''
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        if user.is_superuser:
            role = 'admin'
        elif user.groups.filter(name__iexact='counselor').exists():
            role = 'counselor'
        elif user.groups.filter(name__iexact__in=['class_incharge','incharge','class-incharge']).exists():
            role = 'class_incharge'
        elif user.groups.filter(name__iexact='hod').exists():
            role = 'hod'
        elif user.groups.filter(name__iexact='director').exists():
            role = 'director'

    if request.method == 'POST':
        action = request.POST.get('action')  # 'accept' or 'reject'
        reason = request.POST.get('reason', '').strip()
        user = request.user if request.user.is_authenticated else None
        now = timezone.now()
        # Prevent changing an approval once set
        def already_set(field_name):
            return getattr(obj, field_name) is not None

        if role == 'counselor':
            if already_set('counselor_approved'):
                return render(request, 'approve.html', {'obj': obj, 'error': 'Counselor approval already set'})
            obj.counselor_approved = True if action == 'accept' else False
            obj.counselor_by = user
            obj.counselor_at = now
            obj.counselor_reason = reason
            obj.status = 'counselor_accepted' if action == 'accept' else 'counselor_rejected'
        elif role == 'class_incharge':
            # require counselor to have accepted first
            if obj.counselor_approved is not True:
                return render(request, 'approve.html', {'obj': obj, 'error': 'Counselor must accept before incharge can act'})
            if already_set('incharge_approved'):
                return render(request, 'approve.html', {'obj': obj, 'error': 'Incharge approval already set'})
            obj.incharge_approved = True if action == 'accept' else False
            obj.incharge_by = user
            obj.incharge_at = now
            obj.incharge_reason = reason
            obj.status = 'incharge_accepted' if action == 'accept' else 'incharge_rejected'
        elif role == 'hod':
            # require incharge to have accepted first
            if obj.incharge_approved is not True:
                return render(request, 'approve.html', {'obj': obj, 'error': 'Incharge must accept before HOD can act'})
            if already_set('hod_approved'):
                return render(request, 'approve.html', {'obj': obj, 'error': 'HOD approval already set'})
            obj.hod_approved = True if action == 'accept' else False
            obj.hod_by = user
            obj.hod_at = now
            obj.hod_reason = reason
            obj.status = 'hod_accepted' if action == 'accept' else 'hod_rejected'
        elif role == 'director':
            # require hod to have accepted first
            if obj.hod_approved is not True:
                return render(request, 'approve.html', {'obj': obj, 'error': 'HOD must accept before Director can act'})
            if already_set('director_approved'):
                return render(request, 'approve.html', {'obj': obj, 'error': 'Director approval already set'})
            obj.director_approved = True if action == 'accept' else False
            obj.director_by = user
            obj.director_at = now
            obj.director_reason = reason
            obj.status = 'director_accepted' if action == 'accept' else 'director_rejected'
        else:
            # not authorized
            return render(request, 'approve.html', {'obj': obj, 'error': 'Not authorized for approvals'})

    obj.save()
    return redirect('submissions')

    return render(request, 'approve.html', {'obj': obj})


@login_required
def submissions_view(request):
    from .models import StudentCounseling
    items = StudentCounseling.objects.all().order_by('-id')
    return render(request, 'submissions.html', {'items': items})


def view_approval(request):
    """Public page: ask for roll number and show approval status via client JS."""
    return render(request, 'view_approval.html')


def status_by_roll(request, roll):
    from .models import StudentCounseling
    from django.http import JsonResponse
    item = StudentCounseling.objects.filter(roll_no=roll).order_by('-id').first()
    if not item:
        return JsonResponse({'found': False})
    def user_label(u):
        return u.username if u else None

    def ts_label(dt):
        return dt.isoformat() if dt else None

    data = {
        'found': True,
        'status': item.status,
        'counselor_approved': item.counselor_approved,
        'counselor_by': user_label(item.counselor_by),
        'counselor_at': ts_label(item.counselor_at),
        'incharge_approved': item.incharge_approved,
        'incharge_by': user_label(item.incharge_by),
        'incharge_at': ts_label(item.incharge_at),
        'hod_approved': item.hod_approved,
        'hod_by': user_label(item.hod_by),
        'hod_at': ts_label(item.hod_at),
        'director_approved': item.director_approved,
        'director_by': user_label(item.director_by),
        'director_at': ts_label(item.director_at),
        'id': item.id,
    }
    return JsonResponse(data)


