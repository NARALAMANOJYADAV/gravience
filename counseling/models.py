from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentCounseling(models.Model):
    # Basic Information
    year_sem = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    rtf = models.BooleanField(default=False)
    mq = models.BooleanField(default=False)
    any_other = models.BooleanField(default=False)
    student_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    counselor_name = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    roll_no=models.CharField(max_length=15, null=True, blank=True)
    student_phone = models.CharField(max_length=15)
    father_phone = models.CharField(max_length=15)
    
    # Residence Information
    residence_hostel = models.BooleanField(default=False)
    residence_days_scholar = models.BooleanField(default=False)
    residence_college_bus = models.BooleanField(default=False)
    residence_rtc_bus = models.BooleanField(default=False)
    
    hostel_name = models.CharField(max_length=100, blank=True, null=True)
    room_no = models.CharField(max_length=10, blank=True, null=True)
    
    # Roommates
    roommate1 = models.CharField(max_length=100, blank=True, null=True)
    roll_no1 = models.CharField(max_length=10, blank=True, null=True)
    roommate2 = models.CharField(max_length=100, blank=True, null=True)
    roll_no2 = models.CharField(max_length=10, blank=True, null=True)
    roommate3 = models.CharField(max_length=100, blank=True, null=True)
    roll_no3 = models.CharField(max_length=10, blank=True, null=True)
    
    # Transportation
    bus_route = models.CharField(max_length=100, blank=True, null=True)
    bus_no = models.CharField(max_length=10, blank=True, null=True)
    rtc_travel_place = models.CharField(max_length=100, blank=True, null=True)
    vehicle_details = models.CharField(max_length=100, blank=True, null=True)
    
    # Days Scholar Information
    day_scholar_address = models.TextField(blank=True, null=True)
    ds_name1 = models.CharField(max_length=100, blank=True, null=True)
    ds_roll1 = models.CharField(max_length=20, blank=True, null=True)
    ds_name2 = models.CharField(max_length=100, blank=True, null=True)
    ds_roll2 = models.CharField(max_length=20, blank=True, null=True)
    ds_name3 = models.CharField(max_length=100, blank=True, null=True)
    ds_roll3 = models.CharField(max_length=20, blank=True, null=True)
    
    # Monthly Follow-up
    month1 = models.CharField(max_length=20, blank=True, null=True)
    classes_conducted1 = models.IntegerField(blank=True, null=True)
    classes_attended1 = models.IntegerField(blank=True, null=True)
    attendance_percent1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_letter1 = models.CharField(max_length=3, blank=True, null=True, choices=[('Yes', 'Yes'), ('No', 'No')])
    followup1 = models.TextField(blank=True, null=True)
    
    month2 = models.CharField(max_length=20, blank=True, null=True)
    classes_conducted2 = models.IntegerField(blank=True, null=True)
    classes_attended2 = models.IntegerField(blank=True, null=True)
    attendance_percent2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_letter2 = models.CharField(max_length=3, blank=True, null=True, choices=[('Yes', 'Yes'), ('No', 'No')])
    followup2 = models.TextField(blank=True, null=True)
    
    month3 = models.CharField(max_length=20, blank=True, null=True)
    classes_conducted3 = models.IntegerField(blank=True, null=True)
    classes_attended3 = models.IntegerField(blank=True, null=True)
    attendance_percent3 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_letter3 = models.CharField(max_length=3, blank=True, null=True, choices=[('Yes', 'Yes'), ('No', 'No')])
    followup3 = models.TextField(blank=True, null=True)
    
    month4 = models.CharField(max_length=20, blank=True, null=True)
    classes_conducted4 = models.IntegerField(blank=True, null=True)
    classes_attended4 = models.IntegerField(blank=True, null=True)
    attendance_percent4 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_letter4 = models.CharField(max_length=3, blank=True, null=True, choices=[('Yes', 'Yes'), ('No', 'No')])
    followup4 = models.TextField(blank=True, null=True)
    
    month5 = models.CharField(max_length=20, blank=True, null=True)
    classes_conducted5 = models.IntegerField(blank=True, null=True)
    classes_attended5 = models.IntegerField(blank=True, null=True)
    attendance_percent5 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    monthly_letter5 = models.CharField(max_length=3, blank=True, null=True, choices=[('Yes', 'Yes'), ('No', 'No')])
    followup5 = models.TextField(blank=True, null=True)
    
    # Academic Record
    subject1 = models.CharField(max_length=100, blank=True, null=True)
    mid1_1 = models.IntegerField(blank=True, null=True)
    mid2_1 = models.IntegerField(blank=True, null=True)
    sessional1 = models.IntegerField(blank=True, null=True)
    endsem1 = models.IntegerField(blank=True, null=True)
    total1 = models.IntegerField(blank=True, null=True)
    result1 = models.CharField(max_length=1, choices=[('P', 'Pass'), ('F', 'Fail')], blank=True, null=True)
    pass_year1 = models.CharField(max_length=4, blank=True, null=True)
    
    subject2 = models.CharField(max_length=100, blank=True, null=True)
    mid1_2 = models.IntegerField(blank=True, null=True)
    mid2_2 = models.IntegerField(blank=True, null=True)
    sessional2 = models.IntegerField(blank=True, null=True)
    endsem2 = models.IntegerField(blank=True, null=True)
    total2 = models.IntegerField(blank=True, null=True)
    result2 = models.CharField(max_length=1, choices=[('P', 'Pass'), ('F', 'Fail')], blank=True, null=True)
    pass_year2 = models.CharField(max_length=4, blank=True, null=True)
    
    subject3 = models.CharField(max_length=100, blank=True, null=True)
    mid1_3 = models.IntegerField(blank=True, null=True)
    mid2_3 = models.IntegerField(blank=True, null=True)
    sessional3 = models.IntegerField(blank=True, null=True)
    endsem3 = models.IntegerField(blank=True, null=True)
    total3 = models.IntegerField(blank=True, null=True)
    result3 = models.CharField(max_length=1, choices=[('P', 'Pass'), ('F', 'Fail')], blank=True, null=True)
    pass_year3 = models.CharField(max_length=4, blank=True, null=True)
    
    subject4 = models.CharField(max_length=100, blank=True, null=True)
    mid1_4 = models.IntegerField(blank=True, null=True)
    mid2_4 = models.IntegerField(blank=True, null=True)
    sessional4 = models.IntegerField(blank=True, null=True)
    endsem4 = models.IntegerField(blank=True, null=True)
    total4 = models.IntegerField(blank=True, null=True)
    result4 = models.CharField(max_length=1, choices=[('P', 'Pass'), ('F', 'Fail')], blank=True, null=True)
    pass_year4 = models.CharField(max_length=4, blank=True, null=True)
    
    subject5 = models.CharField(max_length=100, blank=True, null=True)
    mid1_5 = models.IntegerField(blank=True, null=True)
    mid2_5 = models.IntegerField(blank=True, null=True)
    sessional5 = models.IntegerField(blank=True, null=True)
    endsem5 = models.IntegerField(blank=True, null=True)
    total5 = models.IntegerField(blank=True, null=True)
    result5 = models.CharField(max_length=1, choices=[('P', 'Pass'), ('F', 'Fail')], blank=True, null=True)
    pass_year5 = models.CharField(max_length=4, blank=True, null=True)
    
    # Counseling and Other Information
    counseling_date1 = models.CharField(max_length=100, blank=True, null=True)
    counseling_description1 = models.TextField(blank=True, null=True)
    counseling_date2 = models.CharField(max_length=100, blank=True, null=True)
    prizes_participations2 = models.TextField(blank=True, null=True)
    counseling_date3 = models.CharField(max_length=100, blank=True, null=True)
    prizes_participations3 = models.TextField(blank=True, null=True)
    counseling_date4 = models.CharField(max_length=100, blank=True, null=True)
    prizes_participations4 = models.TextField(blank=True, null=True)
    counseling_date5 = models.CharField(max_length=100, blank=True, null=True)
    prizes_participations5 = models.TextField(blank=True, null=True)
    counseling_date6 = models.CharField(max_length=100, blank=True, null=True)
    prizes_participations6 = models.TextField(blank=True, null=True)

    # Workflow / approvals
    STATUS_CHOICES = [
        ('raised', 'Raised'),
        ('counselor_accepted', 'Counselor Accepted'),
        ('counselor_rejected', 'Counselor Rejected'),
        ('incharge_accepted', 'Class Incharge Accepted'),
        ('incharge_rejected', 'Class Incharge Rejected'),
        ('hod_accepted', 'HOD Accepted'),
        ('hod_rejected', 'HOD Rejected'),
        ('director_accepted', 'Director Accepted'),
        ('director_rejected', 'Director Rejected'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='raised')

    counselor_approved = models.BooleanField(null=True, blank=True)
    counselor_by = models.ForeignKey(User, null=True, blank=True, related_name='counselor_actions', on_delete=models.SET_NULL)
    counselor_at = models.DateTimeField(null=True, blank=True)
    counselor_reason = models.TextField(null=True, blank=True)

    incharge_approved = models.BooleanField(null=True, blank=True)
    incharge_by = models.ForeignKey(User, null=True, blank=True, related_name='incharge_actions', on_delete=models.SET_NULL)
    incharge_at = models.DateTimeField(null=True, blank=True)
    incharge_reason = models.TextField(null=True, blank=True)

    hod_approved = models.BooleanField(null=True, blank=True)
    hod_by = models.ForeignKey(User, null=True, blank=True, related_name='hod_actions', on_delete=models.SET_NULL)
    hod_at = models.DateTimeField(null=True, blank=True)
    hod_reason = models.TextField(null=True, blank=True)

    director_approved = models.BooleanField(null=True, blank=True)
    director_by = models.ForeignKey(User, null=True, blank=True, related_name='director_actions', on_delete=models.SET_NULL)
    director_at = models.DateTimeField(null=True, blank=True)
    director_reason = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.student_name