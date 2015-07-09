from modeltranslation.translator import translator, TranslationOptions
from survey.models import Question, Answer

class QuestionTranslationOptions(TranslationOptions):
    fields = ('qtext',)
    pass

class AnswerTranslationOptions(TranslationOptions):
    fields = ('atext',)
    pass

translator.register(Question, QuestionTranslationOptions)
translator.register(Answer, AnswerTranslationOptions)