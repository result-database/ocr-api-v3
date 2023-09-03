# ocr-api

## 決めたこと

- `s3`とか`github`とかに`music.json`を作って、それを参照させる
    - musicDBは手動で更新する
    - DBを使わないようにする

## ToDo

- URL周り
  - `ocr/v2`の`default-url`
  - `web-ui`の`axios-url`
  - `api`の`database-uri`

## How to use (主にDB周り)

- `static/index.html`を見てremoteをapplyするか決める
  - applyする
    - `set-online`する
    - `DB`を直接いじる(`static/index.html`をちょこちょこ見ながら)
  - applyしない
    - ほっとく

## テストデータのメモ

- id1(`Tell Your World`)の読み
  - `てるゆあわーるど` → `てるゆあわーるどっどどどどど`
- id2
  - `ロキ`が削除
- id6
  - `ヒバナ -Reloaded-`が追加

## Memo

- `set-online`は何が何でも保護しなければならない
- ほかはオープンでOK

---

```python
img = cv2.imread('./img.png')
# numpy.ndarra
```

```python
img = Image.open('./img.png')
# PIL.Image
```

```python
# numpy to pillow
pil_img = Image.fromarray(numpy_img)

# pillow to numpy
numpy_img = np.array(pil_img)
```

```python
from fastapi.responses import StreamingResponse

@app.get('/img')
def img():
    img = any_numpy_img
    img_pil = Image.fromarray(img)
    img_pil = img_pil.convert("RGB")
    img_byteio = io.BytesIO()
    img_pil.save(img_byteio, format="JPEG")
    img_byteio.seek(0)
    return StreamingResponse(
        content=img_byteio,
        media_type="image/jpeg"
    )
```

```python
def has_duplicates(seq):
    return len(seq) != len(set(seq))
```

```python
import hashlib

def sha256(target):
    return hashlib.sha256(target.encode()).hexdigest()
```
