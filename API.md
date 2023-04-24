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
