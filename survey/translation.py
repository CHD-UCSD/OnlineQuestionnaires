from modeltranslation.translator import translator, TranslationOptions
from survey.models import Question, Answer, Page

class QuestionTranslationOptions(TranslationOptions):
    fields = ('qtext',)
    pass

class AnswerTranslationOptions(TranslationOptions):
    fields = ('atext','pretext')
    pass

class PageTranslationOptions(TranslationOptions):
    fields = ('page_title', 'page_subtitle',)
    pass

translator.register(Question, QuestionTranslationOptions)
translator.register(Answer, AnswerTranslationOptions)
translator.register(Page, PageTranslationOptions)