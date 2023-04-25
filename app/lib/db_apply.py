def apply(models, db, request):
    db.query(models.Music).delete()
    db.commit()

    for id in request.data.keys():
        data = request.data[id]
        item = models.Music(
            id = data.id,
            title = data.title,
            pronunciation = data.pronunciation,
            creator = data.creator,
            lyricist = data.lyricist,
            composer = data.composer,
            arranger = data.arranger,
            level_easy = data.level_easy,
            level_normal = data.level_normal,
            level_hard = data.level_hard,
            level_expert = data.level_expert,
            level_master = data.level_master,
            totalNote_easy = data.totalNote_easy,
            totalNote_normal = data.totalNote_normal,
            totalNote_hard = data.totalNote_hard,
            totalNote_expert = data.totalNote_expert,
            totalNote_master = data.totalNote_master
        )
        db.add(item)
    db.commit()

    return { "ok": True }
