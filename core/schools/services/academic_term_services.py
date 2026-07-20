from datetime import date

from django.db import transaction
from django.core.exceptions import ValidationError

from schools.models import AcademicTerm, AcademicSession, TermName


@transaction.atomic
def create_term(
        *,
        session_id: str,
        name: TermName,
        start_date: date,
        end_date: date,
) -> AcademicTerm:
    #Validate session exists
    try:
        session = AcademicSession.objects.get(id=session_id)
    except AcademicSession.DoesNotExist:
        raise ValidationError({
            "session_id": "Session with the provided ID does not exist."
        })
    
    #Validate dates
    if end_date <= start_date:
        raise ValidationError({
            "end_date": "End date must be after the start date."
        })
    
    
     #Validate term limit (max 3)
    if AcademicTerm.objects.filter(
        session=session
    ).count() >= 3:
        raise ValidationError({
            "non_field_errors": ["A session cannot have more than three academic terms."]
        })
    
    #Validate creation order    
    if name == TermName.SECOND:
        if not AcademicTerm.objects.filter(
            session=session,
            name=TermName.FIRST,
        ).exists():
            raise ValidationError({
                "name":"First term must exist before the Second term."
            })

    elif name == TermName.THIRD:

        first_exists = AcademicTerm.objects.filter(
            session=session,
            name=TermName.FIRST,
        ).exists()

        second_exists = AcademicTerm.objects.filter(
            session=session,
            name=TermName.SECOND,
        ).exists()

        if not first_exists or not second_exists:
            raise ValidationError({
                "name": "First Term and Second Term must exist before creating Third Term."
            })
        

    #Validate duplicate term
    if AcademicTerm.objects.filter(
        session=session,
        name=name,
    ).exists():
         raise ValidationError({
            "name": "A term with this name already exists for the specified school in this session."
        })
    

    
    #Validate term dates are inside the session
    if (
        start_date < session.start_date 
        or end_date > session.end_date
    ):
        raise ValidationError({
            "non_field_errors":["Term dates must fall within the academic session."]
        })
    
    #Validate overlapping dates
    if AcademicTerm.objects.filter(
        session=session,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).exists():
        raise ValidationError({
            "non_field_errors": ["This term overlaps with an existing term."] 
        })
    
    #Create and save the term
    term = AcademicTerm(
        session=session,
        name=name,
        start_date=start_date,
        end_date=end_date
    )

    term.save()

    return term 



@transaction.atomic
def update_term(
    *,
    term_id: str,
    start_date: date | None = None,
    end_date: date | None = None,
) -> AcademicTerm:

    # Validate term exists
    try:
        term = AcademicTerm.objects.get(id=term_id)
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "term_id": "Term with the provided ID does not exist."
        })

    # Build new values
    new_start_date = (
        start_date
        if start_date is not None
        else term.start_date
    )

    new_end_date = (
        end_date
        if end_date is not None
        else term.end_date
    )

    # Validate dates
    if new_end_date <= new_start_date:
        raise ValidationError({
            "end_date": "End date must be after the start date."
        })

    # Validate dates are within the session
    if (
        new_start_date < term.session.start_date
        or new_end_date > term.session.end_date
    ):
        raise ValidationError({
            "non_field_errors": [
                "Term dates must fall within the academic session."
            ]
        })

    # Validate overlapping dates
    if AcademicTerm.objects.filter(
        session=term.session,
        start_date__lte=new_end_date,
        end_date__gte=new_start_date,
    ).exclude(
        id=term.id,
    ).exists():
        raise ValidationError({
            "non_field_errors": [
                "This term overlaps with an existing term."
            ]
        })

    # Assign values
    term.start_date = new_start_date
    term.end_date = new_end_date

    term.save()

    return term


@transaction.atomic
def activate_term(
    *,
    term_id: str,
) -> AcademicTerm:
     # Validate term exists
    try:
        term = AcademicTerm.objects.get(id=term_id)
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "term_id": "Term with the provided ID does not exist."
        })
    
    # Validate if already active 
    if term.is_current:
        return term 
    
    # Deactivate other terms in the session 
    AcademicTerm.objects.filter(
        session=term.session,
        is_current=True
    ).update(
        is_current=False 
    )

    term.is_current=True

    term.save()

    return term


@transaction.atomic
def deactivate_term(
    *,
    term_id: str,
) -> AcademicTerm:
    # Validate term exists 
    try:
        term = AcademicTerm.objects.get(id=term_id)
    except AcademicTerm.DoesNotExist:
        raise ValidationError({
            "term_id": "Term with the provided ID does not exist."
        })
    
    # Validate if already inactive 
    if not term.is_current:
        return term
    
    term.is_current=False
    
    term.save()

    return term