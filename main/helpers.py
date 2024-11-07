import json
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password


def dd(variable):
    content = json.dumps(variable, indent=4, default=str)
    response_content = f"<pre>{content}</pre>"
    return HttpResponse(response_content)


def bcrypt(password):
    return make_password(password, hasher='bcrypt')