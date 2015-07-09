from modeltranslation.translator import translator, TranslationOptions
from survey.models import Question, Answer, Page

class QuestionTranslationOptions(TranslationOptions):
    fields = ('qtext',)
    pass

class AnswerTranslationOptions(TranslationOptions):
    fields = ('atext',)
    pass

class PageTranslationOptions(TranslationOptions):
    fields = ('page_title', 'page_subtitle',)

translator.register(Question, QuestionTranslationOptions)
translator.register(Answer, AnswerTranslationOptions)
translator.register(Page, PageTranslationOptions)