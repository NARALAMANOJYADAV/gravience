from django.contrib import admin
from django.utils.html import format_html
from .models import StudentCounseling
from django.utils import timezone

@admin.register(StudentCounseling)
class StudentCounselingAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'academic_year', 'counselor_name',
        'get_pass_count', 'get_fail_count',
        'get_subjects_display', 'get_attendance_display','roll_no',
    ]
    list_filter = ['status', 'counselor_approved', 'incharge_approved', 'hod_approved', 'director_approved']
    
    search_fields = [
        'student_name', 'counselor_name',
        'subject1', 'subject2', 'subject3', 'subject4', 'subject5',
        'attendance_percent1', 'attendance_percent2', 'attendance_percent3', 'attendance_percent4', 'attendance_percent5','roll_no'
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        attendance_search = request.GET.get('attendance_search', '').strip()

        # Store for UI form
        self.attendance_search = attendance_search

        if attendance_search:
            try:
                attendance_val = float(attendance_search)
                filtered_ids = []
                for student in queryset:
                    latest_attendance = None
                    for i in reversed(range(1, 6)):
                        att = getattr(student, f'attendance_percent{i}', None)
                        if att is not None:
                            latest_attendance = float(att)
                            break
                    if latest_attendance is not None and abs(latest_attendance - attendance_val) < 0.05:
                        filtered_ids.append(student.id)
                queryset = queryset.filter(id__in=filtered_ids)
            except ValueError:
                pass  # Ignore if input is not a valid float

        return queryset

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Add attendance search UI to top right
        extra_context['attendance_search_form'] = format_html("""
            <div style="float:right;margin:10px 20px;">
                <form method="get">
                    <input type="text" name="attendance_search" value="{}" placeholder="Search by Attendance">
                    <input type="submit" value="Search">
                    <a href="?" style="margin-left:10px;">Clear</a>
                </form>
                <small style="color:gray;">Matches students with latest attendance ≈ entered value (±0.05)</small>
            </div>
        """, self.attendance_search if hasattr(self, 'attendance_search') else '')

        # Subject search-based pass/fail summary
        search_query = request.GET.get('q', '')
        search_query = search_query.strip().lower() if search_query else ''
        if search_query:
            subject_names = set()
            filtered_queryset = self.get_queryset(request)
            for student in filtered_queryset:
                for i in range(1, 6):
                    subject = getattr(student, f'subject{i}', '')
                    subject = subject.strip().lower() if subject else ''
                    if subject:
                        subject_names.add(subject)

            if search_query in subject_names:
                subject_pass = 0
                subject_fail = 0
                for student in filtered_queryset:
                    for i in range(1, 6):
                        subject = getattr(student, f'subject{i}', '')
                        subject = subject.lower() if subject else ''
                        result = getattr(student, f'result{i}', '')
                        result = str(result or '')  # Convert None to empty string
                        if search_query in subject:
                            if result.upper() == 'P':
                                subject_pass += 1
                            elif result.upper() == 'F':
                                subject_fail += 1
                            break
                extra_context['title'] = format_html(
                    'Subject Summary → Passed: <span style="color:green">{}</span> | '
                    'Failed: <span style="color:red">{}</span> | Total: {}',
                    subject_pass, subject_fail, subject_pass + subject_fail
                )

        return super().changelist_view(request, extra_context=extra_context)

    def get_pass_count(self, obj):
        return sum(1 for i in range(1, 6) if (str(getattr(obj, f'result{i}', '') or '')).upper() == 'P')

    get_pass_count.short_description = 'Passes'

    def get_fail_count(self, obj):
        return sum(1 for i in range(1, 6) if (str(getattr(obj, f'result{i}', '') or '')).upper() == 'F')

    get_fail_count.short_description = 'Fails'

    def get_subjects_display(self, obj):
        subjects = []
        for i in range(1, 6):
            subject = getattr(obj, f'subject{i}', '')
            result = getattr(obj, f'result{i}', '')
            # Ensure result is not None before calling .upper()
            result = str(result or '')  # Convert None to empty string
            if subject and result:
                color = 'green' if result.upper() == 'P' else 'red' if result.upper() == 'F' else 'black'
                subjects.append(f"{subject}: <strong style='color:{color}'>{result.upper()}</strong>")
        return format_html("<br>".join(subjects) if subjects else 'No subjects')

    get_subjects_display.short_description = 'Subjects & Results'

    def get_attendance_display(self, obj):
        latest_attendance = None
        for i in reversed(range(1, 6)):
            att = getattr(obj, f'attendance_percent{i}', None)
            if att is not None:
                latest_attendance = att
                break
        if latest_attendance is not None:
            color = 'green' if float(latest_attendance) >= 75 else 'orange' if float(latest_attendance) >= 60 else 'red'
            return format_html('<span style="color:{}">{}</span>', color, latest_attendance)
        return '-'

    get_attendance_display.short_description = 'Latest Attendance %'
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
            return actions
    def student_photo_tag(self, obj):
        if obj.student_photo:  # check if photo uploaded
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover; border-radius:5px;"/>',
                obj.student_photo.url
            )
        return "No Photo"

    student_photo_tag.short_description = "Photo"
    def photo_preview(self, obj):
        """Show bigger preview inside edit page"""
        if obj.student_photo:
            return format_html('<img src="{}" width="150" style="border:1px solid #ccc"/>',
                               obj.student_photo.url)
        return "No Photo Uploaded"
    photo_preview.short_description = "Preview"
    readonly_fields = ('counselor_by','counselor_at','incharge_by','incharge_at','hod_by','hod_at','director_by','director_at')
    def save_model(self, request, obj, form, change):
        # When an approval flag is changed in admin, fill who/when if not present
        now = timezone.now()
        if 'counselor_approved' in form.changed_data and obj.counselor_by is None:
            obj.counselor_by = request.user
            obj.counselor_at = now
            if obj.counselor_approved is True:
                obj.status = 'counselor_accepted'
            else:
                obj.status = 'counselor_rejected'
        # also support admins changing the status field directly
        if 'status' in form.changed_data and obj.counselor_by is None and obj.status in ('counselor_accepted','counselor_rejected'):
            obj.counselor_by = request.user
            obj.counselor_at = now
        if 'status' in form.changed_data and obj.incharge_by is None and obj.status in ('incharge_accepted','incharge_rejected'):
            obj.incharge_by = request.user
            obj.incharge_at = now
        if 'status' in form.changed_data and obj.hod_by is None and obj.status in ('hod_accepted','hod_rejected'):
            obj.hod_by = request.user
            obj.hod_at = now
        if 'status' in form.changed_data and obj.director_by is None and obj.status in ('director_accepted','director_rejected'):
            obj.director_by = request.user
            obj.director_at = now
        if 'incharge_approved' in form.changed_data and obj.incharge_by is None:
            obj.incharge_by = request.user
            obj.incharge_at = now
            if obj.incharge_approved is True:
                obj.status = 'incharge_accepted'
            else:
                obj.status = 'incharge_rejected'
        if 'hod_approved' in form.changed_data and obj.hod_by is None:
            obj.hod_by = request.user
            obj.hod_at = now
            if obj.hod_approved is True:
                obj.status = 'hod_accepted'
            else:
                obj.status = 'hod_rejected'
        if 'director_approved' in form.changed_data and obj.director_by is None:
            obj.director_by = request.user
            obj.director_at = now
            if obj.director_approved is True:
                obj.status = 'director_accepted'
            else:
                obj.status = 'director_rejected'
        super().save_model(request, obj, form, change)
    


