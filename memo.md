# 比較の流れ(特にmusicとdifficultのリレーション)

musicとdifficultは一対多

- Idの重複がないかバリデーション
- sha256で順番が変わってしまわないか？

- そもそもmusicが増えてたり減ってたりするかを確認
- (idのリストを比較する)
- for music
- (共通のidのリストをfor)
  - music自体の変化を確認
  - (check-sumのhashを確認)
  - musicに紐づくdifficultの増減を確認
  - (musicIdをkeyとするアレが必須)
    - for difficult
    - (difficultの増減を確認したときのアレのvalueのリスト)
    - difficult自体の変化を確認
    - (difficultのIdをkeyとするリストでcheck-sumを比較)

# テストデータのメモ

## `music.json` → `db`

- id1(`Tell Your World`)の読み
  - `てるゆあわーるど` → `てるゆあわーるどっどどどどど`
- id2
  - `ロキ`が削除
- id6
  - `ヒバナ -Reloaded-`が追加
