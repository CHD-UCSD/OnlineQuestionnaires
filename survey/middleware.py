from django.conf import settings
from django.utils import translation
from survey.models import User

class LocaleMiddleware(object):
    """Custom LocaleMiddleware that sets language based on user preference in SubjectID.language"""
    def process_request(self, request):
        try:
            user = User.objects.get(username=request.user)
            language = user.subjectid.language
        except:
            language = settings.LANGUAGES[0][0]

        translation.activate(language)
        request.LANGUAGE_CODE = language
