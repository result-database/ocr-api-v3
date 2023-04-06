def has_duplicates(seq):
    return len(seq) != len(set(seq))

def load_diff(music, difficult):
    error = []

    # バリデーション
    musicIds = list(set([j['id'] for j in music]))
    valid_difficulties = {'easy', 'normal', 'hard', 'expert', 'master'}
  
    # musicIdにリストmusicIdsに入っていないidがある場合をチェック
    ids = set(item['musicId'] for item in difficult)
    invalid_ids = ids - set(musicIds)
    if invalid_ids:
        error.append('invalid_ids: ' + str(invalid_ids))

    # musicIdとmusicDifficultyの重複をチェック
    music_data = [(item['musicId'], item['musicDifficulty']) for item in difficult]
    duplicates = [x for n, x in enumerate(music_data) if x in music_data[:n]]
    if duplicates:
        error.append('duplicates: ' + str(duplicates))

    # musicDifficultyの値のバリデーションをチェック
    invalid_difficulties = set(item['musicDifficulty'] for item in difficult) - valid_difficulties
    if invalid_difficulties:
        error.append('invalid_difficulties')
    
    # idの重複がないかバリデーション
    if has_duplicates([j['id'] for j in music]):
        error.append('has_duplicates')
    
    return error
