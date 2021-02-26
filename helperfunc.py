import datetime


# takes a year and month and whether or not it is the end date then
# returns the desired date in epoch time
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


# takes epoch time and returns formatted date time string
def getDateTime(epoch_time: int) -> str:
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%m:%d:%Y')


# takes a file name, month, and year then returns the full file name
def getSaveFileName(file: str, y: int, m: int) -> str:
    return str(y) + file + str(m) + '.csv'


# takes a dict from the api and turns it into a row of data
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
