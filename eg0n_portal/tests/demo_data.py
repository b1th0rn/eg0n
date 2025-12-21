"""
Create demo data using Django Shell.

Usage:

python ./manage.py shell < tests/demo_data.py
"""

import random
from lorem_text import lorem
from django.contrib.auth.models import Group, User

# from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from ioc_management.models import CodeSnippet, Event, FQDN, Hash, IpAdd, Vuln, CONFIDENCE_CHOICES, LANGUAGES, PLATFORM, VALIDATION_CHOICES


# Drop data
Token.objects.all().delete()
Group.objects.all().delete()
User.objects.all().exclude(username="admin").delete()
Event.objects.all().delete()


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        pass
    return None


def get_choice(choices):
    choice = choices[random.randint(0, len(choices) - 1)]
    return choice[0]


USERS = [
    {"first_name": "Luca", "last_name": "Rinaldi"},
    {"first_name": "Giulia", "last_name": "Ferraro"},
    {"first_name": "Marco", "last_name": "Gentile"},
    {"first_name": "Sara", "last_name": "Colombo"},
    {"first_name": "Andrea", "last_name": "De Angelis"},
]

FIRMS = [
    "TechNova Solutions",
    "BlueWave Networks",
    "GreenLogic Systems",
]


# Create superuser
admin_obj = get_or_none(User, username="admin")
if not admin_obj:
    admin_obj = User.objects.create_superuser(
        username="admin", password="admin", email="admin@example.com"
    )
    admin_obj.full_clean()


# Create groups
group_list = []
for firm in FIRMS:
    group = Group.objects.create(name=firm)
    group.full_clean()
    group_list.append(group)


# Create users
user_list = []
# password_hash = make_password("password")
password_hash = "pbkdf2_sha256$1000000$eF2L5tYyTWTEro6dJaU9HS$n7JgU23uuRDpd+6ko7Zpd+UYpdRQhFLw9gvu945iGCU="
for user in USERS:
    username = (
        f'{user["first_name"][0]}{user["last_name"]}'.replace("'", "")
        .replace(" ", "")
        .lower()
    )
    role_id = random.randint(0, 2)
    is_admin = True if role_id == 0 else False
    is_staff = True if is_admin or role_id == 1 else False
    is_active = bool(random.randint(0, 1))
    payload = {
        "username": username,
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": f"{username}@example.com",
        "is_superuser": is_admin,
        "is_staff": is_staff,
        "is_active": is_active,
        "password": password_hash,
    }
    user_obj = User.objects.create(**payload)
    user_obj.full_clean()
    user_list.append(user_obj)
    Token.objects.create(user=user_obj)
    groups_obj = []
    for _ in range(0, 3):
        firm_id = random.randint(0, len(FIRMS) - 1)
        groups_obj.append(Group.objects.get(name=FIRMS[firm_id]))
    user_obj.groups.set(groups_obj)
    user_obj.save()


# Create events
event_list = []
for user_obj in user_list:
    for _ in range(0, 10):
        payload = {
            "author_id": user_obj.id,
            "description": lorem.paragraphs(3),
            "name": " ".join(lorem.sentence().split()[:4]),
        }
        event_obj = Event.objects.create(**payload)
        event_obj.full_clean()
        event_list.append(event_obj)


        # Add Code Snippet
        if bool(random.randint(0, 1)):
            payload = {
                "author_id": user_obj.id,
                "code": lorem.paragraphs(3),
                "confidence": get_choice(CONFIDENCE_CHOICES),
                "description": lorem.paragraphs(3),
                "event_id": str(event_obj.id),
                "language": get_choice(LANGUAGES),
                "name": " ".join(lorem.sentence().split()[:4]),
                "validation_status": get_choice(VALIDATION_CHOICES),
            }
            attribute_obj = CodeSnippet.objects.create(**payload)
            attribute_obj.full_clean()


        # Add FQDN
        if bool(random.randint(0, 1)):
            payload = {
                "author_id": user_obj.id,
                "confidence": get_choice(CONFIDENCE_CHOICES),
                "description": lorem.paragraphs(3),
                "event_id": str(event_obj.id),
                "fqdn": f'www.{" ".join(lorem.sentence().split())[0]}.com',
                "ip_address": f"{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}.{random.randint(1, 200)}",
                "validation_status": get_choice(VALIDATION_CHOICES),
            }
            attribute_obj = FQDN.objects.create(**payload)
            attribute_obj.full_clean()
