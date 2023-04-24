# API仕様書

## OCR

```
curl -X 'POST' \
  'http://localhost:8080/ocr/v2' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "http://localhost:8080/static/target.jpg",
  "psmScore": 6,
  "psmDifficult": 7,
  "psmTitle": 11,
  "psmJudge": 6,
  "borderTitle": 215,
  "borderJudge": 230,
  "blurScore": true,
  "blurDifficult": true,
  "blurTitle": true,
  "blurJudge": true,
  "candidateRatio": 0.3
}'
```

```
{
  "score": {
    "builder": "DigitBuilder",
    "psm": "6",
    "time": {
      "preprocessing": 1.049041748046875e-05,
      "grayscale": 0.012390851974487305,
      "ocr": 0.15609359741210938
    },
    "result": "462713"
  },
  "difficult": {
    "builder": "TextBuilder + whitelist",
    "psm": "7",
    "time": {
      "preprocessing": 1.1444091796875e-05,
      "grayscale": 0.007577657699584961,
      "ocr": 0.1644895076751709
    },
    "result": "EXPERT"
  },
  "title": {
    "builder": "TextBuilder",
    "psm": "11",
    "time": {
      "preprocessing": 1.1444091796875e-05,
      "grayscale": 0.005440473556518555,
      "ocr": 0.1829392910003662
    },
    "result": "Nsで2インビジブル"
  },
  "judge": {
    "builder": "DigitBuilder",
    "psm": "6",
    "time": {
      "prepare": 0.25745630264282227,
      "ocr": 0.6182889938354492
    },
    "result": {
      "PERFECT": "1283",
      "GREAT": "82",
      "GOOD": "4",
      "BAD": "0",
      "MISS": "16"
    }
  },
  "candidateTitle": {
    "ratio": 0.3,
    "time": {
      "database": 0.007360935211181641,
      "process": 0.0038421154022216797,
      "sort": 4.291534423828125e-06
    },
    "result": [
      {
        "title": "インビジブル",
        "credibility": 0.75,
        "musicId": 284
      },
      {
        "title": "インタビュア",
        "credibility": 0.375,
        "musicId": 330
      },
      {
        "title": "フロイライン＝ビブリォチカ",
        "credibility": 0.34782608695652173,
        "musicId": 251
      }
    ]
  },
  "candidateDifficult": {
    "time": {
      "process": 7.43865966796875e-05
    },
    "result": [
      {
        "credibility": 1.0,
        "musicDifficulty": "EXPERT"
      },
      {
        "credibility": 0.3333333333333333,
        "musicDifficulty": "MASTER"
      },
      {
        "credibility": 0.2,
        "musicDifficulty": "EASY"
      },
      {
        "credibility": 0.2,
        "musicDifficulty": "HARD"
      },
      {
        "credibility": 0.16666666666666666,
        "musicDifficulty": "NORMAL"
      }
    ]
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
      "creator": "livetune"....
    },
    "2": {
      "id": 2,
      "creator": "みきとP"....
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
  "data": {
    "1": {
      "id": 1,
      "title": "Tell Your World"....
    },
    "3": {
      "id": 3,
      "title": "テオ"....
    },
    "6": {
      "id": 6,
      "title": "ヒバナ -Reloaded-"....
    }
  }
}

---

{
  "ok": false
}
```

## Set `default_data`

```
curl -X 'GET' \
  'http://localhost:8080/set-online' \
  -H 'accept: application/json'
```

```
{
  "ok": true
}

---

{
  "ok": false
}
```
