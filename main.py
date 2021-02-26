"""
this will file will get data month by month from 2008 - 2021 from stackoverflow
using the python api library StackAPI. This will return posts in json format which
can be converted to a python dictionary and iterated through. This data can be filtered
if needed. We then feed each row and save it into a pandas dataframe that we save into a
corresponding csv file formatted as "{year}/questions_{month}.csv" or "{year}/answers_{month}.csv".

Data we want:
Id, PostTypeId, AcceptedAnswerId, ParentId, CreationDate,
Score, ViewCount, Body, Title, AnswerCount, FavoriteCount

"""
from stackapi import StackAPI
import datetime
import pandas as pd
import json


def getEpochTime(y: int, m: int, is_date_to: bool) -> int:
    sub = 0
    if is_date_to:
        sub = 86400
        if m != 12:
            m += 1
        else:
            y += 1
            m = 1
    return int(datetime.datetime(y, m, 1, 0, 0).timestamp()) - sub


def getDateTime(epoch_time: int) -> str:
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%m:%d:%Y')


def getSaveFileName(file: str, y: int, m: int) -> str:
    return str(y) + file + str(m) + '.csv'


def dictToList(d: dict, post_type: int) -> list:
    if post_type == 1:  # question
        accepted_answer_id = ""
        if 'accepted_answer_id' in d:
            accepted_answer_id = d['accepted_answer_id']
        return [d['question_id'], post_type, accepted_answer_id, '', d['link'],
                getDateTime(d['creation_date']), d['title'], d['body'], d['score'], d['view_count'],
                d['answer_count']]
    elif post_type == 2:  # answer
        return [d['answer_id'], post_type, '', d['question_id'], '',
                getDateTime(d['creation_date']), '', d['body'], d['score'], '',
                '']
    else:
        return None


# declare relevant variables
QUESTION, ANSWER = (1, 2)
q_file = '/questions_'
a_file = '/answers_'
tags = "android"
year = [y for y in range(2008, 2022)]
month = [m for m in range(1, 13)]
columns = ['Id', 'PostTypeId', 'AcceptedAnswerId', 'ParentId', 'Url', 'CreationDate',
           'Title', 'Body', 'Score', 'ViewCount', 'AnswerCount']
SITE = StackAPI('stackoverflow')

# iterate through list of years and months
for y in year:
    for m in month:
        # get start and end date
        from_date = getEpochTime(y, m, False) # 2021 01
        to_date = getEpochTime(y, m, True)   # 2021 02

        # get questions data
        q_data = []
        questions = SITE.fetch("questions", fromdate=from_date, todate=to_date,
                               min=1, tagged=tags, filter="withbody")
        for q in questions['items']:
            q_data.append(dictToList(q, QUESTION))

        q_df = pd.DataFrame(q_data, columns=columns)
        q_df.to_csv(getSaveFileName(q_file, y, m))

        # get answer data
        a_data = []
        answers = SITE.fetch("answers", fromdate=from_date, todate=to_date,
                             min=1, tagged=tags, filter="withbody")

        for a in answers['items']:
            a_data.append(dictToList(a, ANSWER))
        a_df = pd.DataFrame(a_data, columns=columns)
        a_df.to_csv(getSaveFileName(a_file, y, m))
        break
    break
