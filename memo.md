# てきとーメモ

## めんどくさいので、musicにdifficultを押し込む(カラムを極限まで増やす)

- DBをJSONとして吐き出すAPI
- ReactでAPIとJSONでDiffを表示する
- ボタン一つでJSONをApplyするAPI

## テストデータのメモ

### `music.json` → `db`

- id1(`Tell Your World`)の読み
  - `てるゆあわーるど` → `てるゆあわーるどっどどどどど`
- id2
  - `ロキ`が削除
- id6
  - `ヒバナ -Reloaded-`が追加

## DB周りのコマンド

```bash
$ docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v $(pwd)/data:/var/lib/postgresql/data -d postgres:15.2-bullseye

$ psql -h localhost -U postgres -d postgres
```