import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'surveysite.settings'

from survey.models import Question, Answer, Survey, Page, Log
import csv, sys

survey_acronym = sys.argv[1]
surveys = []
if survey_acronym in ['FDH','all']:
    try:
        survey = Survey.objects.get(title='Family Developmental History Questionnaire')
        survey.delete()
        surveys.append(Survey(title='Family Developmental History Questionnaire', acronym='FDH', auto_number=False))
    except:
        surveys.append(Survey(title='Family Developmental History Questionnaire', acronym='FDH', auto_number=False))
if survey_acronym in ['AQ','all']:
    try:
        survey = Survey.objects.get(title='Activities Questionnaire')
        survey.delete()
        surveys.append(Survey(title='Activities Questionnaire', acronym='AQ', auto_number=False))
    except:
        surveys.append(Survey(title='Activities Questionnaire', acronym='AQ', auto_number=False))
if survey_acronym in ['LEQ','all']:
    try:
        survey = Survey.objects.get(title='Life Experiences Questionnaire')
        survey.delete()
        surveys.append(Survey(title='Life Experiences Questionnaire', acronym='LEQ', auto_number=False))
    except:
        surveys.append(Survey(title='Life Experiences Questionnaire', acronym='LEQ', auto_number=False))
if survey_acronym in ['CBQ','all']:
    try:
        survey = Survey.objects.get(title="Children's Behavior Questionnaire")
        survey.delete()
        surveys.append(Survey(title="Children's Behavior Questionnaire", acronym='CBQ', auto_number=False))
    except:
        surveys.append(Survey(title="Children's Behavior Questionnaire", acronym='CBQ', auto_number=False))
if survey_acronym in ['MCTQ','all']:
    try:
        surveyset = Survey.objects.filter(title='Middle Childhood Temperament Questionnaire')
        for survey in surveyset:
            for question in survey.question_set.all():
                question.delete()
            survey.delete()
        surveys.append(Survey(title="Middle Childhood Temperament Questionnaire", acronym='MCTQ', auto_number=False))
    except Exception as e:
        #surveys.append(Survey(title="Middle Childhood Temperament Questionnaire", acronym='MCTQ', auto_number=False))
        print "Error deleting", e
if survey_acronym in ['ADHD','all']:
    try:
        survey = Survey.objects.get(title='ADHD Rating Scale-IV')
        survey.delete()
        surveys.append(Survey(title="ADHD Rating Scale-IV", acronym='ADHD', auto_number=False))
    except:
        surveys.append(Survey(title="ADHD Rating Scale-IV", acronym='ADHD', auto_number=False))
if survey_acronym in ['PRQ','all']:
    try:
        survey = Survey.objects.get(title='Parent Relationship Questionnaire')
        survey.delete()
        surveys.append(Survey(title="Parent Relationship Questionnaire", acronym='PRQ', auto_number=False))
    except:
        surveys.append(Survey(title="Parent Relationship Questionnaire", acronym='PRQ', auto_number=False))
if survey_acronym in ['SCARED','all']:
    try:
        survey = Survey.objects.get(title='Self-Report for Childhood Anxiety Disorders - Parent')
        survey.delete()
        surveys.append(Survey(title="Self-Report for Childhood Anxiety Related Disorders - Parent", acronym='SCARED', auto_number=False))
    except:
        surveys.append(Survey(title="Self-Report for Childhood Anxiety Related Disorders - Parent", acronym='SCARED', auto_number=False))
if survey_acronym in ['Enrollment','all']:
    try:
        survey = Survey.objects.get(title='Enrollment Form')
        survey.delete()
        surveys.append(Survey(title='Enrollment Form', acronym='Enrollment', auto_number=False))
    except:
        surveys.append(Survey(title='Enrollment Form', acronym='Enrollment', auto_number=False))

if not surveys: 
    print 'survey %s not recognized' %survey_acronym
    print 'type(survey_acronym) is', type(survey_acronym)
    sys.exit()

for survey in surveys:

    survey.save()
    survey_acronym = survey.acronym

    dir = '/opt/Computerized Questionnaires/'
    input_csv = '%s/%s_online_conditions.csv'%(survey_acronym.replace('_Parent',''), survey_acronym)
    gen_output_key = '%s/%s_online_output_key.csv'%(survey_acronym.replace('_Parent',''), survey_acronym)

    content=[]
    reader = csv.reader(open(dir + input_csv, 'rU'))
    Q_to_row = {}
    current_row=0
    for line in reader: 
        content.extend([line])
        Q_to_row[line[0]]=current_row
    

    reader = csv.reader(open(dir + gen_output_key, 'rb'))
    headers = reader.next()
    Q_converter={}
    current_Q = 0
    ind_cond_from = None
    ind_cond_to_add = None
    ind_cond_until = None

    for line in reader:
        current_Q+=1
        Q_converter[line[headers.index('Q Number')]] = current_Q

    def write(qrow, qnumber, rootrow=None, qvariable=None, ianswer=None):
        global group_to
        global page_number
        global ind_cond_to_add
        global ind_cond_until
        global ind_cond_from
         
        converted_qnumber = Q_converter[qnumber]
    
        # make new page if needed
        if group_to==None:
            page_number+=1
            if qrow[loop_label_index] and qvariable:
                page = Page(survey=survey, page_number=page_number, page_title=qrow[label_index], page_subtitle=qvariable)
            else:
                page = Page(survey=survey, page_number=page_number, page_title=qrow[label_index])
                if qrow[sublabel_index]!='': page.page_subtitle = qrow[sublabel_index]
            page.save()
            if qrow[group_index]!='': group_to = qrow[group_index]
        else: page=Page.objects.get(survey=survey, page_number=page_number)
        if group_to==qrow[Q_num_index]: group_to=None
        
        # make question and answers
        qtext = qrow[Q_index]
        if '%s' in qtext: qtext = qtext %qvariable
        
        #dependent conditions
        if qrow[conditions_index]: 
            conditions=eval(qrow[conditions_index])
            for k in conditions.keys():
                #this replaces keys inside loops with correct key
                if k not in Q_converter.keys() and rootrow: conditions[qnumber.replace(qnumber.split('-')[1], k)] = conditions.pop(k)
        else: conditions={}
    
        #add independent conditions
        if ind_cond_to_add and ind_cond_until in qnumber: 
            ind_cond_to_add=None
            ind_cond_until=None
        elif ind_cond_to_add: conditions.update(ind_cond_to_add)
    
        #add loop conditions
        if rootrow and rootrow[conditions_index]: conditions.update(eval(rootrow[conditions_index]))
    
        #process conditions
        if conditions:    
            new_conditions={}
            for k,v in conditions.iteritems(): 
                if v=='any' and ianswer!=None: new_conditions[Q_converter[k]] = ianswer
                elif type(v)==list and ianswer!=None: new_conditions[Q_converter[k]] = ianswer
                else: new_conditions[Q_converter[k]] = v
        else: new_conditions=qrow[conditions_index]
    
        #create question
        q = Question(page=page, survey=page.survey, qnumber=converted_qnumber, qtext=qtext, conditions=new_conditions, newcolumn=qrow[col_index]=='Y', required=qrow[req_index]=='Y')
        q.save()
    
        #create answers
        if qrow[answers_index]:
            triggers=[]
            for a in eval(qrow[answers_index]):
                this_answer = Answer(question=q, atype=a['atype'])
                for attr in [attr for attr in a.keys() if attr != 'atype']:
                    if attr=='trigger': triggers.append((this_answer, a['trigger']))
                    else: exec('this_answer.'+attr+'='+'a[attr]')
                this_answer.save()
            for trigger in triggers:
                trigger[0].trigger = q.answer_set.all()[trigger[1]]
                trigger[0].save()
            if qrow[no_ans_index]=='Y':
                this_answer = Answer(question=q, atype='Ra', atext="Don't know")
                this_answer.save()
                this_answer = Answer(question=q, atype='Ra', atext="Decline to state")
                this_answer.save()

        #check if this is the final question
        if qrow[next_Q_index]=='END': 
            q.page.final_page=True
            q.page.save()
    
        #figure out independent conditions for next questions
        if qrow[ind_conditions_index]:
            ind_conds = eval(qrow[ind_conditions_index])
            items={} #e.g. items[17] = 'LM17'; needed because can't reliably compare numbers in strings
            for val in ind_conds: 
                items[int(''.join([str(s) for s in val if str(s).isdigit()]))] = val
            ind_cond_from = items[min(items.keys())]
            ind_cond_to_add = {qnumber: ind_conds.index(ind_cond_from)}
            ind_cond_until = items[max(items.keys())]
        
        
    page_number = 0
    group_to = None
    for num, row in enumerate(content):
        if num==0:
            Q_num_index=row.index('Q Number')
            label_index=row.index('Label')
            sublabel_index=row.index('Sublabel')
            Q_index=row.index('Question')
            #ptext_index=row.index('Posttext')
            Q_type_index=row.index('Q Type')
            loop_index=row.index('Loop')
            next_Q_index=row.index('Next Q')
            loop_info_index=row.index('Loop Info')
            answers_index=row.index('Answers')
            group_index=row.index('Group')
            conditions_index=row.index('Dependent Conditions')
            ind_conditions_index=row.index('Independent Conditions')
            loop_label_index=row.index('Loop Label')
            col_index=row.index('New Column')
            req_index=row.index('Response Required')
            no_ans_index=row.index('No Answer Option')
        if row[Q_num_index][0]=='Q' and row[Q_num_index][1].isdigit() and num>0:
            if not row[loop_index]:
                write(qrow=row,qnumber=row[Q_num_index])
        
            elif row[loop_index]: #first look for the loop start
                print 'entered section for loop type Qs'
                look_for_end=False
                for second_num, second_row in enumerate(content):
                    if second_row[Q_num_index]==row[loop_index]:
                        start_loop=second_num; look_for_end=True
                    if look_for_end and second_row[next_Q_index]=='loop end':
                        end_loop=second_num; look_for_end=False

                if row[loop_info_index] == '':
                    for loop_num in range(start_loop,end_loop+1):# make new page if needed
                        write(qrow=content[loop_num], rootrow = row, qnumber=row[Q_num_index]+'-'+content[loop_num][Q_num_index], qvariable = row[Q_index])
                        # make new page if needed
 
                elif row[loop_info_index] != '':
                    loop_info=eval(row[loop_info_index])
                    if type(loop_info[0])==list:
                        try: look_for = loop_info[0][1]
                        except:
                            chars = list(loop_info[0][0])
                            start = chars.index('-'); chars.pop(start)
                            look_for = loop_info[0][0][start+1:chars.index('-')]
                    elif type(loop_info[0])==str:
                        look_for = loop_info[0]
                    for ref_num, ref_line in enumerate(content):
                        if ref_line[Q_num_index]==look_for:
                            these_answers=eval(ref_line[answers_index])
                            ref_index = ref_num
                            if not these_answers: print 'could not get answers from loop info', loop_info
                    for ianswer, answer in enumerate(these_answers):
                        if type(loop_info[1])==list and ianswer not in loop_info[1]: continue
                        if content[ref_index][Q_type_index] in ['radio','check']:
                            if 'trigger' in answer.keys(): continue # don't need a loop for an elaboration
                            for loop_num in range(start_loop,end_loop+1):# make new page if needed
                                write(qrow=content[loop_num], rootrow=row, qnumber=row[Q_num_index]+'-'+content[loop_num][Q_num_index]+'-'+answer['atext'], qvariable = answer['atext'], ianswer=ianswer)
                        elif content[ref_index][Q_type_index] == 'check/free':
                            if 'trigger' in answer.keys(): continue # don't need a loop for an elaboration
                            for iter_num in range(1,11):
                                for loop_num in range(start_loop,end_loop+1):# make new page if needed
                                    if iter_num==1: write(qrow=content[loop_num], qnumber=row[Q_num_index]+'-'+content[loop_num][Q_num_index]+'-'+answer['atext'], qvariable = answer['atext'], ianswer=ianswer)
                                    else: write(qrow=content[loop_num], rootrow=row, qnumber=row[Q_num_index]+'-'+content[loop_num][Q_num_index]+'-'+answer['atext'] + ' %d' % iter_num, qvariable = answer['atext'], ianswer=ianswer)
                         
