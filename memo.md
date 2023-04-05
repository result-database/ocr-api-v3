# てきとーメモ

## 比較の流れ(特にmusicとdifficultのリレーション)

musicとdifficultは一対多

- [x] difficultのテストデータを作成

- [x] Idの重複がないかバリデーション
- [x] sha256で順番が変わってしまわないか？

- [x] そもそもmusicが増えてたり減ってたりするかを確認
- [x] (idのリストを比較する)
- [x] for music
- [x] (共通のidのリストをfor)
  - [x] music自体の変化を確認
  - [x] (check-sumのhashを確認)
  - musicに紐づくdifficultの増減を確認
  - (musicIdをkeyとするアレが必須)
    - for difficult
    - (difficultの増減を確認したときのアレのvalueのリスト)
    - difficult自体の変化を確認
    - (difficultのIdをkeyとするリストでcheck-sumを比較)

## テストデータのメモ

### `music.json` → `db`

- id1(`Tell Your World`)の読み
  - `てるゆあわーるど` → `てるゆあわーるどっどどどどど`
- id2
  - `ロキ`が削除
- id6
  - `ヒバナ -Reloaded-`が追加
