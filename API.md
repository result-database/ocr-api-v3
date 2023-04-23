# API仕様書

## OCR

```
curl -X 'POST' \
  'http://localhost:8080/ocr/v2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "http://localhost:8080/static/wide.png",
  "psmScore": 6,
  "psmDifficult": 7,
  "psmTitle": 11,
  "psmJudge": 6,
  "borderTitle": 215,
  "borderJudge": 230,
  "blurScore": true,
  "blurDifficult": true,
  "blurTitle": true,
  "blurJudge": true
}'
```

```
{
  "score": {
    "builder": "DigitBuilder",
    "psm": "6",
    "time": {
      "preprocessing": 0.0003681182861328125,
      "grayscale": 0.02746105194091797,
      "ocr": 0.29795384407043457
    },
    "result": "596068"
  },
  "difficult": {
    "builder": "TextBuilder + whitelist",
    "psm": "7",
    "time": {
      "preprocessing": 0.000011205673217773438,
      "grayscale": 0.007710933685302734,
      "ocr": 0.15625810623168945
    },
    "result": "EXPERT"
  },
  "title": {
    "builder": "TextBuilder",
    "psm": "11",
    "time": {
      "preprocessing": 0.000010728836059570312,
      "grayscale": 0.004464626312255859,
      "ocr": 0.18338227272033691
    },
    "result": "BrandNewDay"
  },
  "judge": {
    "builder": "DigitBuilder",
    "psm": "6",
    "time": {
      "prepare": 0.36309003829956055,
      "ocr": 0.5867767333984375
    },
    "result": {
      "PERFECT": "1238",
      "GREAT": "22",
      "GOOD": "0",
      "BAD": "0",
      "MISS": "0"
    }
  }
}
```

## From DB

```
curl -X 'GET' \
  'http://localhost:8080/music' \
  -H 'accept: application/json'
```

```
{
  "data": {
    "1": {
      "id": 1,
      "creator": "livetune",
      "composer": "kz",
      "level_easy": 5,
      "level_hard": 16,
      "level_master": 26,
      "totalNote_normal": 492,
      "totalNote_expert": 961,
      "lyricist": "kz",
      "title": "Tell Your World",
      "pronunciation": "てるゆあわーるど",
      "arranger": "kz",
      "level_normal": 10,
      "level_expert": 22,
      "totalNote_easy": 220,
      "totalNote_hard": 719,
      "totalNote_master": 1147
    },
    "2": {
      "id": 2,
      "creator": "みきとP",
      "composer": "みきとP",
      "level_easy": 7,
      "level_hard": 17,
      "level_master": 28,
      "totalNote_normal": 296,
      "totalNote_expert": 827,
      "lyricist": "みきとP",
      "title": "ロキ",
      "pronunciation": "ろき",
      "arranger": "みきとP",
      "level_normal": 11,
      "level_expert": 24,
      "totalNote_easy": 166,
      "totalNote_hard": 635,
      "totalNote_master": 975
    },
    "3": {
      "id": 3,
      "creator": "Omoi",
      "composer": "Omoi",
      "level_easy": 9,
      "level_hard": 19,
      "level_master": 32,
      "totalNote_normal": 477,
      "totalNote_expert": 997,
      "lyricist": "Sakurai",
      "title": "テオ",
      "pronunciation": "てお",
      "arranger": "Omoi",
      "level_normal": 14,
      "level_expert": 27,
      "totalNote_easy": 135,
      "totalNote_hard": 681,
      "totalNote_master": 1221
    }
  }
}
```

## From `static`

```
curl -X 'GET' \
  'http://localhost:8080/get' \
  -H 'accept: application/json'
```

```
{
  "ok": true,
  "result": {
    "1": {
      "id": 1,
      "title": "Tell Your World",
      "pronunciation": "てるゆあわーるどっどどどどど",
      "creator": "livetune",
      "lyricist": "kz",
      "composer": "kz",
      "arranger": "kz",
      "level_easy": 5,
      "totalNote_easy": 2,
      "level_normal": 10,
      "totalNote_normal": 492,
      "level_hard": 16,
      "totalNote_hard": 719,
      "level_expert": 22,
      "totalNote_expert": 961,
      "level_master": 26,
      "totalNote_master": 1147
    },
    "3": {
      "id": 3,
      "title": "テオ",
      "pronunciation": "てお",
      "creator": "Omoi",
      "lyricist": "Sakurai",
      "composer": "Omoi",
      "arranger": "Omoi",
      "level_easy": 9,
      "totalNote_easy": 135,
      "level_normal": 14,
      "totalNote_normal": 477,
      "level_hard": 19,
      "totalNote_hard": 681,
      "level_expert": 27,
      "totalNote_expert": 997,
      "level_master": 32,
      "totalNote_master": 1221
    },
    "6": {
      "id": 6,
      "title": "ヒバナ -Reloaded-",
      "pronunciation": "ひばなりろーでっど",
      "creator": "DECO*27",
      "lyricist": "DECO*27",
      "composer": "DECO*27",
      "arranger": "Rockwell",
      "level_easy": 9,
      "totalNote_easy": 198,
      "level_normal": 14,
      "totalNote_normal": 394,
      "level_hard": 19,
      "totalNote_hard": 568,
      "level_expert": 28,
      "totalNote_expert": 808,
      "level_master": 32,
      "totalNote_master": 1060
    }
  }
}
```

## Set `default_data`

```
curl -X 'GET' \
  'http://localhost:8080/set' \
  -H 'accept: application/json'
```

```
{
  "ok": true
}
```

## Apply `new_data`

```
curl -X 'POST' \
  'http://localhost:8080/apply' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "1": {
      "id": 1,
      "title": "Tell Your World",
      "pronunciation": "てるゆあわーるどっどどどどど",
      "creator": "livetune",
      "lyricist": "kz",
      "composer": "kz",
      "arranger": "kz",
      "level_easy": 5,
      "totalNote_easy": 2,
      "level_normal": 10,
      "totalNote_normal": 492,
      "level_hard": 16,
      "totalNote_hard": 719,
      "level_expert": 22,
      "totalNote_expert": 961,
      "level_master": 26,
      "totalNote_master": 1147
    },
    "3": {
      "id": 3,
      "title": "テオ",
      "pronunciation": "てお",
      "creator": "Omoi",
      "lyricist": "Sakurai",
      "composer": "Omoi",
      "arranger": "Omoi",
      "level_easy": 9,
      "totalNote_easy": 135,
      "level_normal": 14,
      "totalNote_normal": 477,
      "level_hard": 19,
      "totalNote_hard": 681,
      "level_expert": 27,
      "totalNote_expert": 997,
      "level_master": 32,
      "totalNote_master": 1221
    },
    "6": {
      "id": 6,
      "title": "ヒバナ -Reloaded-",
      "pronunciation": "ひばなりろーでっど",
      "creator": "DECO*27",
      "lyricist": "DECO*27",
      "composer": "DECO*27",
      "arranger": "Rockwell",
      "level_easy": 9,
      "totalNote_easy": 198,
      "level_normal": 14,
      "totalNote_normal": 394,
      "level_hard": 19,
      "totalNote_hard": 568,
      "level_expert": 28,
      "totalNote_expert": 808,
      "level_master": 32,
      "totalNote_master": 1060
    }
  }
}'
```

```
{
  "ok": true
}
```
