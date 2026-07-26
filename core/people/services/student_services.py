from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from people.models import Student
from schools.models import School


@transaction.atomic
def create_student(
    *,
    school_id: str,
    admission_number: str,
    first_name: str,
    last_name: str,
    middle_name: str = "",
    gender: str,
    date_of_birth: date,
    admission_date: date,
) -> Student:

    # Validate school exists
    try:
        school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
            "school_id": "School with the provided ID does not exist."
        })


    # Clean input
    admission_number = admission_number.strip()
    first_name = first_name.strip()
    last_name = last_name.strip()
    middle_name = middle_name.strip()

    # Validate required fields
    if not admission_number:
        raise ValidationError({
            "admission_number": "Admission number cannot be empty."
        })

    if not first_name:
        raise ValidationError({
            "first_name": "First name cannot be empty."
        })

    if not last_name:
        raise ValidationError({
            "last_name": "Last name cannot be empty."
        })

    # Validate duplicate admission number
    if Student.objects.filter(
        school=school,
        admission_number__iexact=admission_number,
    ).exists():
        raise ValidationError({
            "admission_number": (
                "A student with this admission number already exists for this school."
            )
        })
    
    # Validate the admission date 
    if admission_date > date.today():
        raise ValidationError({
            "admission_date": "Admission date cannot be in the future."
        })
            
    # Validate the birth date 
    if date_of_birth > date.today():
        raise ValidationError({
            "date_of_birth": "Date of birth cannot be in the future."
        })
    
    # Validating the admission date against the date of birth 
    if admission_date < date_of_birth:
        raise ValidationError({
            "admission_date": (
                "Admission date cannot be earlier than the student's date of birth."
            )
        })


    # Create student
    student = Student(
        school=school,
        admission_number=admission_number,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        gender=gender,
        date_of_birth=date_of_birth,
        admission_date=admission_date,
    )

    student.save()

    return student




@transaction.atomic
def update_student(
    *,
    student_id: str,
    admission_number: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    middle_name: str | None = None,
    gender: str | None = None,
    date_of_birth: date | None = None,
    admission_date: date | None = None,
) -> Student:

    # Validate student exists
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id": "Student with the provided ID does not exist."
        })

    # Build new values
    new_admission_number = (
        admission_number.strip()
        if admission_number is not None
        else student.admission_number
    )

    new_first_name = (
        first_name.strip()
        if first_name is not None
        else student.first_name
    )

    new_last_name = (
        last_name.strip()
        if last_name is not None
        else student.last_name
    )

    new_middle_name = (
        middle_name.strip()
        if middle_name is not None
        else student.middle_name
    )

    new_gender = (
        gender
        if gender is not None
        else student.gender
    )

    new_date_of_birth = (
        date_of_birth
        if date_of_birth is not None
        else student.date_of_birth
    )

    new_admission_date = (
        admission_date
        if admission_date is not None
        else student.admission_date
    )

    # Validate required fields
    if not new_admission_number:
        raise ValidationError({
            "admission_number": "Admission number cannot be empty."
        })

    if not new_first_name:
        raise ValidationError({
            "first_name": "First name cannot be empty."
        })

    if not new_last_name:
        raise ValidationError({
            "last_name": "Last name cannot be empty."
        })

    # Validate duplicate admission number
    if Student.objects.filter(
        school=student.school,
        admission_number__iexact=new_admission_number,
    ).exclude(
        id=student.id,
    ).exists():
        raise ValidationError({
            "admission_number": (
                "A student with this admission number already exists for this school."
            )
        })

    # Validate dates
    if new_date_of_birth > date.today():
        raise ValidationError({
            "date_of_birth": "Date of birth cannot be in the future."
        })

    if new_admission_date > date.today():
        raise ValidationError({
            "admission_date": "Admission date cannot be in the future."
        })

    if new_admission_date < new_date_of_birth:
        raise ValidationError({
            "admission_date": (
                "Admission date cannot be earlier than the student's date of birth."
            )
        })

    # Assign values
    student.admission_number = new_admission_number
    student.first_name = new_first_name
    student.last_name = new_last_name
    student.middle_name = new_middle_name
    student.gender = new_gender
    student.date_of_birth = new_date_of_birth
    student.admission_date = new_admission_date

    student.save()

    return student


@transaction.atomic
def activate_student(
    *,
    student_id: str,
) -> Student:

    # Validate student exists
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id": "Student with the provided ID does not exist."
        })

    # Already active
    if student.is_active:
        return student

    student.is_active = True
    student.save()

    return student


@transaction.atomic
def deactivate_student(
    *,
    student_id: str,
) -> Student:

    # Validate student exists
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise ValidationError({
            "student_id": "Student with the provided ID does not exist."
        })

    # Already inactive
    if not student.is_active:
        return student

    student.is_active = False
    student.save()

    return student