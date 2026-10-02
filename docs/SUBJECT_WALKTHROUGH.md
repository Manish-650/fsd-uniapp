# Subject: first implementation milestone

This module represents one enrolled subject. The full application, file storage and menus are not implemented yet.

## Read the code

1. __init__ receives an integer ID and mark, checks their ranges, and formats the ID with leading zeros. Subject(7, 85) gives ID "007".
2. grade is a property: access subject.grade like an attribute. It calculates Z/P/C/D/HD from the mark using if/elif conditions.
3. create receives the collection of used IDs as three-character strings, e.g. {"001", "007"}. It chooses an available ID and generates a mark once. The future enrolment service must pass the full applicable collection; this class alone cannot guarantee uniqueness across students or restarts.
4. to_dict returns the ID and mark in a plain dictionary for future persistence.
5. from_dict reconstructs a subject from saved values. It does not call random functions. The grade is calculated again from the unchanged mark.

The uniqueness scope (global or per student) remains a tutor clarification. The calling service will control that scope by choosing which used IDs to supply. Dictionary conversion does not select the final file format or implement students.data persistence.

## Try it

From the repository root, run Python:

```python
from uniapp.models.subject import Subject

subject = Subject(7, 85)
print(subject.id, subject.mark, subject.grade)
# 007 85 HD

new_subject = Subject.create({"007"})
print(new_subject.id, new_subject.mark, new_subject.grade)

restored = Subject.from_dict(subject.to_dict())
print(restored.id, restored.mark, restored.grade)
# 007 85 HD
```

Run the checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

The tests cover grade boundaries, invalid inputs, ID exhaustion and preservation of saved marks. No third-party libraries are needed. Next: Student and the four-subject enrolment limit.
