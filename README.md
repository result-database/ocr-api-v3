# ocr-api

## ToDo

- ぼかしを検討
  - difficult
  - title
  - score
- すべてのgrayscaleをnumpyに書き換えてもらう
- psmとborderの初期値を受け取るようにする
- psmとborderのバリデーションをきれいにする

## Parameter

- score
  - 6 (or 7)
- difficult
  - 7 (or 6)
- title
  - 11 (( or 7 or 6))
  - 215
- judge
  - 6 (( or 7))
  - 230

## Memo

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
