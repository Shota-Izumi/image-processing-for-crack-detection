# image-processing-for-crack-detection

## develop-branch
開発用ブランチ

## feature/basefunc
各関数，クラスの作成
- 前処理関数
  - 元画像の読み取り
  - シャッフル
  - パディング
  - クロップ
- 後処理関数
  - 再構築
  - 面積閾値計算
  - 面積ごとに削除
  - lossの描画関数
- GUI機能
  - 画像をどのように加工するかがわかるように表示
  - GUIベースで処理をすすめることができる

## feature/mrcnndataset
- 前処理関数
  - jsonファイルの作成
    - 領域面積の閾値オプションの追加