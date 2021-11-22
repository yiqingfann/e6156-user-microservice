import re

paths_do_not_require_security = [
    '/login/google/?.*'
]

def check_authentication(request, google):
    # for regex in paths_do_not_require_security:
    #     if re.match(regex, request.path):
    #         return True

    # return True if google.authorized else False
    return True