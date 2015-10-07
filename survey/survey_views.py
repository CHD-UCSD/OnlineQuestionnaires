# Create your views here.
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from survey.survey_forms import AuthenticationFormWithInactiveUsersOkay
from survey.models import Question, Answer, Survey, Log, Page, Available_Survey, Record, SubjectID
from django.contrib.auth.models import User
from django.template import RequestContext
from os.path import join, isdir, isfile
from datetime import datetime, timedelta
from django.db.models.loading import get_model
from django.conf import settings
import os
import operator
import csv
import re
import itertools

def logout_page(request):
    """
    Log users out and redirect to main page
    """
    logout(request)
    return HttpResponseRedirect(reverse('survey:index'))


def user_record(user):
    user = User.objects.get(username=user)
    record = Record.objects.filter(subjectid=user.subjectid)
    return (user, record[0])


def available_surveys(user, survey=None):    
    user = User.objects.get(username=user)
    survey_list = []
    if hasattr(user,'subjectid'):
		record, created = Record.objects.get_or_create(subjectid=user.subjectid)
		if not survey:
			for this_survey in Survey.objects.all():
				availability, created = Available_Survey.objects.get_or_create(record=record, survey=this_survey)
				if availability.available: survey_list.append(this_survey)
		else:
			availability, created = Available_Survey.objects.get_or_create(record=record, survey=survey)
			if availability.available: survey_list.append(survey)
            
    return survey_list

@login_required
def main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take them to the login page.
    """
    survey_list = available_surveys(request.user)
    
    return render_to_response(
        'survey/index.html',
        {'survey_list':survey_list, 'all_surveys':Survey.objects.all(), 'request': request},
        context_instance=RequestContext(request)
    )

@login_required
def get_qlist(request, page):
    qlist=[]
    while not qlist:
        shortcircuit = False
        page_questions = page.question_set.all().order_by('qnumber')
        for question in page_questions:
            if question.conditions: 
                include=True #to handle "AND" operator
                exclude=True #to handle "OR" operator
                conds = eval(question.conditions)
            
                #loop through all conditions given
                for qnum, needed_answers in conds.items():
                    qcond = Question.objects.get(survey=page.survey, qnumber=qnum)
                
                    #if no log, don't include
                    if qcond not in [log.question for log in Log.objects.filter(user=request.user)]:
                        include=False
                        if question.condition_operator=='AND': break
                        if question.condition_operator=='OR': continue
                
                    #if any response found, break; otherwise don't include this question
                    if needed_answers=='any':
                        if Log.objects.get(question=qcond, user=request.user) and eval(Log.objects.get(question=qcond, user=request.user).response): #[resp for resp in eval(Log.objects.get(question=qcond, user=request.user).response).values() if resp!='']: #found a positive response
                            exclude=False
                            if question.condition_operator=='OR': break
                        else: #did not find a positive response
                            include=False
                            if question.condition_operator=='AND': break
                
                    #if the responses match the conditions, break; otherwise don't include this question
                    else: 
                        if type(needed_answers) == int: needed_answers=[needed_answers]
                        # if condition met
                        if Log.objects.get(question=qcond, user=request.user) and [item for item in eval(Log.objects.get(question=qcond, user=request.user).response).keys() if item in [qcond.answer_set.all()[i].id for i in needed_answers]]:
                            exclude=False
                            if question.condition_operator=='OR': break
                        else: 
                            include=False
                            if question.condition_operator=='AND': break
                        
                #add to qlist if conditions are met
                if question.condition_operator=='OR' and not exclude: qlist.append(question)
                elif question.condition_operator=='AND' and include: qlist.append(question)
                
                #try to delete log if we skip this question
                elif question.condition_operator=='OR' and exclude:
                    try: Log.objects.get(question=question, user=request.user).delete()
                    except: pass
                
                #try to delete log if we skip this question
                elif question.condition_operator=='AND' and not include:
                    try: Log.objects.get(question=question, user=request.user).delete() #if we skip a question that was answered previously, delete log
                    except: pass
                    
                    #if conditions not met for AND and no qlist from previous questions, see if we can short-circuit to the next valid page
                    if not qlist:
                        while True:
                            page_questions = page.question_set.all().order_by('qnumber')
                            # if all questions on the page have the failed condition and are an "AND" operator
                            if len(page_questions)>1 and reduce(operator.mul, [q.conditions!='' and (qnum,conds[qnum]) in eval(q.conditions).items() and q.condition_operator=='AND' for q in page_questions], 1)==1:
                                for q in page_questions:
                                    try: Log.objects.get(question=q, user=request.user).delete()
                                    except: pass
                                page = Page.objects.get(survey = page.survey, page_number=int(page.page_number)+1)
                                print 'short-circuited page %d' %page.page_number
                                shortcircuit = True
                            else: break
            
            #if no conditions, add to qlist
            elif not question.conditions: qlist.append(question)
            
            #break for loop if short-circuited the page
            if shortcircuit: break
            
        #if we returned no questions for the page, we didn't short-circuit the page, and it's not the last page, try the next page
        if page.final_page and not qlist: return 'END'
        if not qlist and not shortcircuit and not page.final_page: page = Page.objects.get(survey = page.survey, page_number=int(page.page_number)+1)
    
    return qlist

@login_required
def get_q_log_list(request, qlist):
    q_log_list = []
    newq_count=1
    for q in qlist:
        try:
            response = eval(Log.objects.get(question=q, user=request.user).response)
            # if len(q.answer_set.all()): # if the question is not simply text
            	# count all the logs we have for previous questions
            	# presented_number = len([log for log in Log.objects.all() if log.question.survey==q.survey and log.question.qnumber<q.qnumber and len(log.question.answer_set.all())>0]) + 1
            # else: presented_number = False
            log_list = []
            answer_list = []
            for a in q.answer_set.all():
                if a.id in response.keys():
                    # answer list is (answer object, response)
                    if a.atype in ['Ra','Ch']: answer_list.append((a,True))
                    else: answer_list.append((a,response[a.id]))
                else: 
                	if a.atype in ['Ra','Ch']: answer_list.append((a,False))
                	else: answer_list.append((a,''))
        except:
            #if len(q.answer_set.all()): # if the question is not simply text
                # count all the logs we have for previous questions
                # presented_number = len([log for log in Log.objects.all() if log.question.survey==q.survey and log.question.qnumber<q.qnumber and len(log.question.answer_set.all())>0]) + newq_count
                # newq_count += 1
            # else: presented_number = False
            answer_list = [(a,'') for a in q.answer_set.all()]
        
        q_log_list.append((q,answer_list))
    return q_log_list


@login_required
def question_page(request, survey_pk, page_num):
    """
    If users are authenticated, direct them to the main page. Otherwise, take them to the login page.
    """

    survey = Survey.objects.get(pk=int(survey_pk))
    user, record = user_record(request.user)
    if len(Available_Survey.objects.filter(survey=survey, record=record))==0:
    #if survey not in list(available_surveys(request.user, survey=survey)):
        return HttpResponseRedirect(reverse('survey:notavailable', args=(survey.pk,)))
    page = Page.objects.get(survey=survey, page_number=page_num)
    question_list = list(get_qlist(request, page))
    #print 'question_list:', question_list
    if question_list=='END':
        last_page = [p for p in survey.page_set.all() if p.final_page][-1]
        return render_to_response('survey/completed.html', 
            {'survey':survey, 'last_page': last_page}, context_instance = RequestContext(request))
    
    else:
        q_log_list = get_q_log_list(request, question_list)
        page = question_list[0].page
    
        return render_to_response('survey/questiondetail.html',
                                {'survey': survey, 'q_log_list': q_log_list, 'page': page},
                                context_instance=RequestContext(request))

@login_required
def back(request, survey_pk, page_num):
    survey = Survey.objects.get(pk=int(survey_pk))
    page = Page.objects.get(survey=survey, page_number=page_num)
    q = Question.objects.get(survey=survey, qnumber = min([q.qnumber for q in page.question_set.all()]))
    new_page_num = False
    try:
        previous_question = Question.objects.get(survey = survey, qnumber= max([log.question.qnumber for log in Log.objects.all() if log.question.survey==q.survey and log.question.qnumber<q.qnumber]))
        new_page_num = previous_question.page.page_number
    except:
        new_page_num = None
    
    if new_page_num: return HttpResponseRedirect(reverse('survey:questiondetail', args=(survey.pk, int(new_page_num),)))
    else: return HttpResponseRedirect(reverse('survey:questiondetail', args=(survey.pk, int(page_num),)))

@login_required
def response(request, survey_pk, page_num):
    print request.POST
    survey = Survey.objects.get(pk=int(survey_pk))
    page = Page.objects.get(survey=survey, page_number=page_num)
    question_list = get_qlist(request, page)
    q_log_list = get_q_log_list(request, question_list)
    errors = []
    highlight_entry_box=[]
    highlight_question=[]
    free_resps = [k for k in request.POST.keys() if 'Free Answer' in k]
    for i,q in enumerate(question_list):
        #these_free_resps = [k for k in free_resps if [str(a.id)==k[-len(str(a.id)):] for a in q.answer_set.all()]]
        #print '%d free_resps:'%q.id, free_resps
        #print '%d these_free_resps:'%q.id, these_free_resps
        #check if all required questions have a response; applicable for questions with only radio or free responses
        
        #dictionary to store all positive answers in dictionary with k,v = answer.id, response
        these_answers = {}
        verbose_response = []
        for entry in request.POST.keys():
        	if str(q.id)==entry: 
        		for answerid in request.POST.getlist(entry): these_answers[int(answerid)]=True
        		for answerid in request.POST.getlist(entry): verbose_response.append(Answer.objects.get(id=answerid).atext)
        	elif '_' in entry and str(q.id)==entry[:entry.index('_')] and request.POST.get(entry)!= '': 
        		answerid = int(entry[entry.index('_')+1:])
        		these_answers[answerid]=request.POST.get(entry)
        		if Answer.objects.get(id=answerid).atext: verbose_response.append(request.POST.get(entry) + ' ' + Answer.objects.get(id=answerid).atext)
        		else: verbose_response.append(request.POST.get(entry))
        
        #these_answer_keys = [k for k in request.POST.keys() if str(q.id) == k[:k.index('_')]]
        if q.required and not these_answers:# (set([str(a.id) for a in q.answer_set.all()]).intersection(set([k for k in request.POST.keys() if request.POST.get(k)!='']))): #or request.POST.getlist(str(q.id))==['']):
            highlight_question.append(q.id)
            if survey.auto_number: errors.append('Question %d requires a response.'%q_log_list[i][0].qnumber)
            else: errors=['Questions with an asterisk require a response']
        
        #check formats of answers
        for a in [a for a in q.answer_set.all() if a.atype=='Fr' and a.aformat and a.id in these_answers.keys()]: #request.POST.get('Free Answer %d'%a.id)!='']:
            if a.aformat=='In':
                try: int(these_answers[a.id])
                except: 
                    errors.append('Your response for the highlighted answer should be a whole number.')
                    highlight_entry_box.append(a.id)
            elif a.aformat=='Nm':
                try: float(these_answers[a.id])
                except:
                    errors.append('The highlighted answer requires a numerical response.')
                    highlight_entry_box.append(a.id)
            elif a.aformat=='Dt':
                try: datetime.strptime(these_answers[a.id], "%m/%d/%Y")
                except:
                    errors.append('The highlighted answer requires a date in the format: "MM/DD/YYYY".')
                    highlight_entry_box.append(a.id)
            if a.aformat in ['In','Nm']:
                if a.range_min and not errors:
                    if a.range_min>float(these_answers[a.id]):
                        if a.range_max: errors.append('The highlighted answer must be between {0} and {1}'.format(a.range_min,a.range_max))
                        else: errors.append('The highlighted answer must be greater than {0}'.format(a.range_min))
                        highlight_entry_box.append(a.id)
                if a.range_max and not errors:
                    if a.range_max<float(these_answers[a.id]):
                        if a.range_min: errors.append('The highlighted answer must be between {0} and {1}'.format(a.range_min,a.range_max))
                        else: errors.append('The highlighted answer must be less than {0}'.format(a.range_max))
                        highlight_entry_box.append(a.id)
        try: log = Log.objects.get(question=q, user=request.user); print 'got log'
        except: log = Log(question=q, user=request.user); print 'made log'
        #response = {}
        #verbose_response = []
        #if str(q.id) in request.POST.keys(): 
        #    for a_id in request.POST.getlist(str(q.id)):
        #        response[int(a_id)] = True
        #        verbose_response.append(Answer.objects.get(id=int(a_id)).atext)
        #
        #for k in these_free_resps:
        #    free_resp = request.POST.get(k)
        #    response[int(k.replace('Free Answer ',''))] = free_resp
        #    if free_resp: verbose_response.append(free_resp + ' ' + Answer.objects.get(id=int(k.replace('Free Answer ',''))).atext)
        
        # save response
        log.response = these_answers
        log.verbose_response = verbose_response
        log.question_id = q.id
        log.subjectid = User.objects.get(username=request.user).subjectid
        log.save()
        print 'qnumber %d logged as %s' %(q.qnumber, log.response)

    if errors:
        q_log_list = get_q_log_list(request, question_list)
        return render(request, 'survey/questiondetail.html',
                    {'survey': survey, 'q_log_list': q_log_list, 'page': page,
                    'errors': errors, 'highlight_entry_box': highlight_entry_box,
                    'highlight_question': highlight_question})
    
    elif page.final_page: return HttpResponseRedirect(reverse('survey:completed', args=(survey.pk,)))
    else: return HttpResponseRedirect(reverse('survey:questiondetail', args=(survey.pk, int(page_num)+1,)))

@login_required
def completed(request, survey_pk):
    survey = Survey.objects.get(pk=survey_pk)
    last_page = [p for p in survey.page_set.all() if p.final_page][-1]
    print 'last_page:', last_page
    print os.getcwd()
    return render_to_response('survey/completed.html', 
            {'survey':survey, 'last_page':last_page}, context_instance = RequestContext(request))

@login_required
def save_survey(request, survey_pk):
    survey = Survey.objects.get(pk=survey_pk)
    
    #update record, making survey unavailable
    record = Record.objects.get(subjectid=User.objects.get(username=request.user).subjectid)
    availability = Available_Survey.objects.get(record=record, survey=survey)
    availability.available = False
    availability.save()
    
    #create data folder if it doesn't already exist
    if not isdir('/opt/surveysite/data/'+os.sep+survey.acronym): os.makedirs('/opt/surveysite/data/'+os.sep+survey.acronym)
    
    #save an output file for the survey data
    timestamp = datetime.now()
    subjid = SubjectID.objects.get(user=request.user)
    with open(join('/opt/surveysite/data/',survey.acronym,'%s_%s_%s.csv'%(survey.acronym, subjid, timestamp.strftime('%Y%m%d_%H%M%S'))), 'wb') as csvfile:
        datawriter = csv.writer(csvfile)
        columns = ['User','Timestamp']+['%s_%s'%(survey.acronym, str(q.qnumber)) for q in survey.question_set.all()]
        col_dictionary = {'User': 'User','Timestamp': 'Timestamp of questionnaire submission'}
        if not isfile('/opt/surveysite/data/%s/%s_question_key.csv'%(survey.acronym, survey.acronym)):
            for q in survey.question_set.all(): col_dictionary['%s_%s'%(survey.acronym, str(q.qnumber))] = str(q.qtext)
            with open('/opt/surveysite/data/%s/%s_question_key.csv'%(survey.acronym, survey.acronym), 'wb') as keyfile:
                keywriter = csv.writer(keyfile)
                for col in columns: keywriter.writerow([col, col_dictionary[col]])
        datawriter.writerow(columns)
        responses = {'User': subjid, 'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        for q in [log.question for log in Log.objects.filter(user=request.user) if log.question.survey==survey]:
            if Log.objects.get(user=request.user, question=q).verbose_response: responses['%s_%s'%(survey.acronym, str(q.qnumber))] = str(", ".join(eval(Log.objects.get(user=request.user, question=q).verbose_response)))
        resp_row = []
        for col in columns:
            if col in responses.keys(): resp_row.append(responses[col])
            else: resp_row.append('')
        datawriter.writerow(resp_row)
    
    return HttpResponseRedirect(reverse('survey:index'))

def save_models(whitelist, params):
    is_whitelisted = lambda model_name, field_name: field_name in whitelist.get(model_name, {})

    for key, value in params:
        match = re.match('(?P<model_name>.*?)_(?P<pk>\d*?)_(?P<field_name>.*)', key)
        if not match:
            continue

        model_name = match.group('model_name')
        pk = match.group('pk')
        field_name = match.group('field_name')
        if is_whitelisted(model_name, field_name) == False:
            continue

        model = get_model('survey', model_name)
        obj = model.objects.get(pk=int(pk))
        original_value = getattr(obj, field_name)
        if (original_value == value):
            continue

        setattr(obj, field_name, value)
        obj.save()

@user_passes_test(lambda u: u.is_superuser)
def edit_survey_save(request, survey_pk, page_num):
    page_num = int(page_num)
    action = request.POST.get('action', '')
    if action == 'save':
        # model name to field name dict; whitelists what's allowed to be modified.
        save_whitelist = {
            'Question': 
                [('qtext_%s' % language_code) for language_code,_ in settings.LANGUAGES ],
            'Answer':
                [('pretext_%s' % language_code) for language_code,_ in settings.LANGUAGES ] +
                [('atext_%s' % language_code) for language_code,_ in settings.LANGUAGES ],
        }

        save_models(save_whitelist, request.POST.iteritems())
    elif action == 'back':
        page_num = page_num - 1 if page_num > 1 else page_num
    elif action == 'next':
        page = Page.objects.get(survey_id=survey_pk, page_number=page_num)
        page_num = page_num if page.final_page else page_num + 1

    return HttpResponseRedirect(reverse('survey:edit_survey', args=(survey_pk, page_num,)))

@user_passes_test(lambda u: u.is_superuser)
def edit_survey(request, survey_pk, page_num):
    survey = Survey.objects.get(pk=int(survey_pk))
    page = Page.objects.get(survey=survey, page_number=page_num)
    question_list = list(get_qlist(request, page))

    if question_list=='END':
        last_page = [p for p in survey.page_set.all() if p.final_page][-1]
        return render_to_response('survey/completed.html', 
            {'survey':survey, 'last_page': last_page}, context_instance = RequestContext(request))
    else:
        q_log_list = get_q_log_list(request, question_list)
        page = question_list[0].page
    
        return render_to_response('survey/edit.html',
                                {'survey': survey, 'q_log_list': q_log_list, 'page': page, 'page_num': page_num, 'request': request},
                                context_instance=RequestContext(request))

@login_required
def survey_not_available(request, survey_pk):
    return render_to_response('survey/notavailable.html', context_instance = RequestContext(request))
