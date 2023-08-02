# from django import template

# from users.models import CustomUser

# register = template.Library()

# @register.filter
# def check_podpiski(quoted_string):
#     user = CustomUser.get_request_user()
#     podchik = CustomUser.objects.get(id=quoted_string)
#     for podski in user.friendship_requests_from.all():
#         podki = podski.to_user
#         if podki == podchik:
#             return "True"
#         else:
#             return "False"