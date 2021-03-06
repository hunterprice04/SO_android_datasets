"""
this will file will get data month by month from 2008 - 2021 from stackoverflow
using the python api library StackAPI. This will return posts in json format which
can be converted to a python dictionary and iterated through. This data can be filtered
if needed. We then feed each row and save it into a pandas dataframe that we save into a
corresponding csv file formatted as "{year}/questions_{month}.csv" or "{year}/answers_{month}.csv".

Data we want:
'Id', 'PostTypeId', 'AcceptedAnswerId', 'ParentId', 'Url',
'CreationDate', 'Title', 'Body', 'Score', 'ViewCount', 'AnswerCount'

"""
import os
from stackapi import StackAPI
import pandas as pd
from helperfunc import getEpochTime, dictToList, getSaveFileName

# declare relevant variables
QUESTION, ANSWER = (1, 2)
q_file, a_file, tags = ('/questions_', '/answers_', "android")
year = [y for y in range(2008, 2022)]
month = [m for m in range(1, 13)]
columns = ['Id', 'PostTypeId', 'AcceptedAnswerId', 'ParentId', 'Url', 'CreationDate',
           'Title', 'Body', 'Score', 'ViewCount', 'AnswerCount']
SITE = StackAPI('stackoverflow')

# set up directories that store csv files
for y in year:
    if not os.path.exists(str(y)):
        os.makedirs(str(y))

# iterate through list of years and months
for y in year:
    for m in month:
        # get start and end date
        from_date = getEpochTime(y, m, False)
        to_date = getEpochTime(y, m, True)

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
        break  # remove this break statement for full download
    break  # remove this break statement for full download
