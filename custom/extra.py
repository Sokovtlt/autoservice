from django.core.exceptions import ValidationError
from django.contrib import messages


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160


def validate_file_size(value):
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("You cannot upload file more than 5Mb")
    else:
        return value


class CustomSuccessMessageMixin:
    """The class for displaying a message when working with the form.
    The inherited classes receive the variable success_msg, and a message is passed in it"""
    @property
    def success_msg(self):
        return False

    def error_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg, self.error_msg)
        return super().form_valid(form)
