from django.contrib import admin
from django.forms import TextInput, Textarea, Select
from django.db import models
from survey.models import Question, Answer, Survey, Page, Record, Available_Survey, SubjectID

class AnswerInline(admin.StackedInline):
    model = Answer
    fieldsets = [
        (None, {'fields': [('atype','atext','aformat')]}),
        ('Advanced Options', {'fields': [('pretext', 'size','trigger'),('range_min','range_max')], 'classes': ['collapse']})
    ]
    extra = 1
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(AnswerInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'trigger':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(question__exact = request._obj_)
            else:
                field.queryset = field.queryset.none()
        return field


class QuestionInline(admin.TabularInline):
    model = Question
    extra=3

class PageInline(admin.TabularInline):
    model = Page
    extra=3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['survey','page','qnumber','qtext']}),
        ('Advanced Options', {'fields': [('newcolumn','required'),('conditions','condition_operator')], 'classes': ['collapse']}),
    ]
    formfield_overrides = {
        models.IntegerField: {'widget': TextInput(attrs={'size':3})},
        models.CharField: {'widget': TextInput(attrs={'size':100})},
        models.TextField: {'widget': Textarea(attrs={'rows':2,'cols':100})}
    }
    inlines = [AnswerInline]

    list_filter = ['page']

    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super(QuestionAdmin, self).get_form(request, obj, **kwargs)

    #def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #    field = super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    #    if db_field.name == 'page':
    #        if request._obj_ is not None:
    #            field.queryset = field.queryset.filter(answer__exact = request._obj_.survey)
    #        else:
    #            field.queryset = field.queryset.none()
    #    return field

    #list_display = ('qnumber','qtext','newcolumn','required')
    #list_filter = ['qnumber']

#     class Media:
#         js = (
#             '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
#             'js/myscript.js',       # project static folder
#             'app/js/myscript.js',   # app static folder
#         )


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Page', {'fields':['survey', 'page_number', 'page_title','page_subtitle','final_page']}),
    ]
    #inlines = [QuestionInline]
    list_filter = ['survey']

class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Survey', {'fields':['title']}),
    ]
    inlines = [PageInline]

#class RecordAdmin(admin.ModelAdmin):
#    readonly_fields=('survey','subjectid')
#    fieldsets = [
#        ('Availability Record', {'fields': ['survey','subjectid','available']}),
#    ]
#    list_filter = ['subjectid']

class AvailabilityInline(admin.TabularInline):
    model = Available_Survey
    fieldsets = [
        ('Available_Survey', {'fields':['record','survey', 'available']}),
    ]
    extra=0

class RecordAdmin(admin.ModelAdmin):
    #readonly_fields=['subjectid']
    fieldsets = [
        (None, {'fields':['subjectid']}),
    ]
    inlines = [AvailabilityInline]


admin.site.register(Survey)
admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
#admin.site.register(AvailabilityRecord, RecordAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(SubjectID)
