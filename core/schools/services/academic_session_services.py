from datetime import date

from django.db import transaction
from django.core.exceptions import ValidationError

from schools.models import School, AcademicSession


@transaction.atomic
def create_session(
    *,
    school_id: str,
    name: str,
    start_date: date,
    end_date: date,
) -> AcademicSession:
    # Validate that the school exists 
    try:
       school = School.objects.get(id=school_id)
    except School.DoesNotExist:
        raise ValidationError({
        "school_id": "School with the provided ID does not exist."
    }) 
    
     # Clean the name input
    name = name.strip()

    if not name:
        raise ValidationError({
            "name": "Session name cannot be empty."
        })
    

    # Validate the date 
    if end_date <= start_date:
        raise ValidationError({
            "end_date": "End date must be after the start date."
        })
    


    # Check duplicate name 
    if AcademicSession.objects.filter(
        school=school,
        name__iexact=name
    ).exists():
        raise ValidationError({
            "name": "A session with this name already exists for the specified school."
        })
    

    # Check for overlapping dates
    if AcademicSession.objects.filter(
        school=school,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists():
        raise ValidationError({
            "non_field_errors": ["This session overlaps with an existing session."] 
        })

        
    # Create the new session
    session = AcademicSession(
        school=school,
        name=name,
        start_date=start_date,
        end_date=end_date,
    )


    session.save()

    return session



@transaction.atomic
def update_session(
    *,
    session_id: str,
    name: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> AcademicSession:
    # Validate that the session exists
    try:
        session = AcademicSession.objects.get(id=session_id)
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "session_id": "Session with the provided ID does not exist."
        })
    
    # Build the updated values 
    new_name = name.strip() if name is not None else session.name
    new_start_date = start_date if start_date is not None else session.start_date
    new_end_date = end_date if end_date is not None else session.end_date

    # Validate name for empty string
    if new_name == "":
        raise ValidationError({
            "name": "Session name cannot be empty."
        })
    
    # Validate the updated dates
    if new_start_date and new_end_date and new_end_date <= new_start_date:
        raise ValidationError({
            "end_date": "End date must be after the start date."
        })


    # Validate duplicates
    if AcademicSession.objects.filter(
        school=session.school,
        name__iexact=new_name,
    ).exclude(
        id=session.id,
    ).exists():
        raise ValidationError({
            "name": "A session with this name already exists for the specified school."
    })

    # Check for overlapping dates
    if AcademicSession.objects.filter(
        school=session.school,
        start_date__lte=new_end_date,
        end_date__gte=new_start_date
    ).exclude(
        id=session.id
    ).exists():
        raise ValidationError({
            "non_field_errors": ["This session overlaps with an existing session."] 
        })

    # Assign Values
    session.name = new_name
    session.start_date = new_start_date
    session.end_date = new_end_date

    session.save()

    return session


@transaction.atomic
def activate_session(
        *,
        session_id : str,
) -> AcademicSession:
    # Validate that the session exists
    try:
        session = AcademicSession.objects.get(id=session_id)
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "session_id": "Session with the provided ID does not exist."
        })

    if session.is_current:
         return session
        
    # Deactivate any other current sessions for the same school
    AcademicSession.objects.filter(
        school=session.school,
        is_current=True
    ).update(
        is_current=False
    )

    session.is_current = True

    session.save()

    return session


@transaction.atomic
def deactivate_session(
        *,
        session_id : str
) -> AcademicSession:
    # Validate that the session exists
    try:
        session = AcademicSession.objects.get(id=session_id)
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "session_id": "Session with the provided ID does not exist."
        })

    if not session.is_current:
        return session

    session.is_current = False

    session.save()

    return session
