import difflib
from lib.util import sort_for_difficult

def candidateDifficult(target):
    difficults = ['EASY', 'NORMAL', 'HARD', 'EXPERT', 'MASTER']
    datas = []

    for j in difficults:
        result = difflib.SequenceMatcher(None, target, j).ratio()
        datas.append({'credibility': result, 'musicDifficulty': j})

    datas = sort_for_difficult(datas)

    return datas
