import sqlite3
import surveysite.settings

c = None

def rchop(s, ending):
    """ Removes 'ending' from the end of str 's'. """
    return s[:-len(ending)] if s.endswith(ending) else s

def answers(question):
    """ Return a Question's corresponding Answers. """
    return c.execute("SELECT * FROM survey_answer WHERE question_id=? ORDER BY id", (question['id'],)).fetchall()

def question(survey, qnumber):
    """ Returns a Question given its Survey and qnumber. """
    return c.execute(
        "SELECT * FROM survey_question WHERE survey_id=? AND qnumber=?", 
        (survey['id'], qnumber)
    ).fetchone()

def questions(survey):
    """ Returns a survey's corresponding Questions. """
    return c.execute("SELECT * FROM survey_question WHERE survey_id=?", (survey['id'],)).fetchall()

def en_survey(es_survey):
    """ Given a Spanish survey, return the corresponding English survey. """
    en_survey_title = rchop(es_survey['title'], 'Spanish').strip()
    return c.execute("SELECT * FROM survey_survey WHERE title=?", (en_survey_title,)).fetchone()

def es_surveys():
    """ Return a list of Spanish surveys. """
    return c.execute("SELECT * FROM survey_survey WHERE title LIKE '%Spanish'").fetchall()

def merge_i18n_surveys():
    """ Find Spanish surveys and merge them to the *_es fields of their corresponding English surveys. """
    for es_survey in es_surveys():
        _en_survey = en_survey(es_survey)
        if _en_survey == None:
            continue

        for en_question in questions(_en_survey):
            es_question = question(es_survey, en_question['qnumber'])
            c.execute(
                "UPDATE survey_question SET qtext_es=? WHERE id=?",
                (es_question['qtext'], en_question['id'])
            )

            en_answers = answers(en_question)
            es_answers = answers(es_question)
            for en_answer, es_answer in zip(en_answers, es_answers):
                c.execute(
                    "UPDATE survey_answer SET atext_es=? WHERE id=?",
                    (es_answer['atext'], en_answer['id'])
                )

def setup_en_surveys():
    """ Sets qtext_en and atext_en to qtext and atext respectively. """
    """ This way, the *text accessor won't return NULL when it tries reading *text_en """
    c.execute("UPDATE survey_question SET qtext_en = qtext")
    c.execute("UPDATE survey_answer SET atext_en = atext")

def main():
    global c
    conn = sqlite3.connect(surveysite.settings.DATABASES['default']['NAME'])
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Uncomment this to reset *_en and *_es fields if you wish to test this script after running it.
    # c.execute("UPDATE survey_question SET qtext_en = NULL")
    # c.execute("UPDATE survey_question SET qtext_es = NULL")
    # c.execute("UPDATE survey_answer SET atext_en = NULL")
    # c.execute("UPDATE survey_answer SET atext_es = NULL")

    merge_i18n_surveys()
    setup_en_surveys()

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()