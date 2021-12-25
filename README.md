# pmx_to_blender_asset

## 概要：　pmxファイルを自動的にBlenderのアセット化するアドオン
前提：mmd_toolsがインストールされていること

![ui](https://user-images.githubusercontent.com/44924233/147359325-23c6837c-1df4-4513-94a3-9f30969826a8.jpg)

### 機能1. 単一pmxファイルのアセット化

1. Asset Folderを指定する。
1. single PMX Azzetizeボタンを押し、pmxファイルを設定すると、pmxファイル名のpmx拡張子をblendに変更したファイルとしてアセット化される（時間がかかります）

   - オプション：Asembleにチェックを入れると、物理／モーフBindなどを設定した状態でアセット化する（時間がかかるためまずはOFFで試すことを推奨）
   - オプション：Auto Smooth MeshをOFFにすると、Auto Smooth をオフにした状態のメッシュで保存する

1. アセットプレビューの自動設定
    1. AutoCamをOFFにした場合、アクティブなカメラで原点にインポートされたキャラクターを撮影してプレビューに設定する。
    2. AutoCamがONの場合、cam loc、cam rotに指定した位置角度にテンポラリのカメラで240x240pxのレンダリングを行いプレビューに設定する。
    - いずれの場合でも、照明は実行時点のblendファイルの設定が採用される。
    - 実行時点のファイルがそのままアセットファイルになるため不要なオブジェクトがない状態で実行することを推奨。

### 機能2. アセットプレビュー自動設定
- 3Dviewport もしくは Outlinerで、アセット化を選択し、"Set Asset IMG"を押すことで、レンダリングとプレビュー設定を行うことが出来る
    * アセットブラウザでの選択には対応していません。

### 機能3.一括アセット化
1. PMX Folderと、Asset Folderを指定する
2. Batch Assetizeボタンを押すとPMX Folderに含まれる全てのpmxファイルを一括でblendファイルにアセット化。

### アセットの利用方法
1. アセットブラウザから3D Viewportにアセットをドラッグドロップすると、MMDモデルの実体とインスタンスの２つが3D Viewportに現れます。　インスタンスは不要なので削除してください
2. MMDモデルを選択し、MMD/Model Setupの可視性：リセットを押すことでリジッドボディなどの可視性を正常に戻すことが出来ます
3. 物理を動かすためには、MMD/Scen Setup：Update Worldを押して、Appendしたリジッドボディを有効化する必要があります


## 重要な注意事項
- 同一pmxファイル名をアセット化した場合、アセットは上書きされる。　プリファレンスのバージョン保存設定によりblend1,blend2...は作成される。
- 長時間走行するため、システムコンソールを表示することを推奨。**システムコンソールを開いていればCTRL-Cで中断することができる。** また途中でアセット化がどこまで進んだかはblenderでは確認できないため、blenderのアセットフォルダを確認してください。
- blender3.xのアセットブラウザの仕様は流動的であり、作成したアセットは将来利用できなくなる可能性もあります。

## サンプル
![sample](https://user-images.githubusercontent.com/44924233/147364858-256338a0-434a-4998-8c2d-5d2891d097ac.jpg)

- Batch Assetizeの対象は全てのpmxファイルのため、キャラクターの複数のバリエーションや付属のアクセサリもアセット化されます。プレビューが適切な位置にならないものも多いので、その場合、open blend fileで、アセットファイルを開き、機能２により手動でプレビューの自動設定が必要です

## 仕様補足
- 名前

    (a) pmxファイル名(.pmx)　→　コレクション名＝blendファイル名(.blend)

    (b) mmd_root名(Empty)

    (c) アセット名は(a)をインスタンス化した名前(Empty)
    
    → (b)と(c)が同じ場合Empty名が重複し、.001にリネームされアセットの表示上見栄えが悪いため、001を削除し、末尾"."に変更している

    アセットをAppendすると、(a)のコレクション名の下に、(b)のmmd_root名になる。 (c)はあくまでインスタンス名＝アセット名

## TODO
1. 手動でのアセット化より遅い気がするが要性能確認。~~アセット化完了後のPMXコレクション以下の削除が遅い。特にAsembleしてnccなど大量のtemporaryがある場合。outlinerからの階層削除は速いのでそちらにしたいがbpy.ops.outlinerをpythonから使う方法がわからない~~
```python
        for obj in pmx_collection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
    
        bpy.data.collections.remove(pmx_collection)
```
2. タグを付けるべき（MMDなど）だが、bpy.ops.asset.tag_add()の使い方がわからない。
1. カメラを適切なの位置に修正するようにしたい。以下の２種類は必要。
    - キャラクターの場合は身長にあわせてバストアップ: → Auto Angleで対応した。ただしZoomの自動調整もしたい
    - 背景、小物、アクセサリの場合は全体像: 未対応

1. アセット利用時の３ステップ（インスタンス削除、可視性リセット、Update World）は煩雑なので、自動化出来ないか？ (おそらく無理)
1. アセットをFile-Openでプレビューした場合、Workbenchのプレビューになっている。
 Eeveeレンダーモードにし、インスタンスを非表示にして保存すればFile-Openのプレビューの見栄えは良くなる。
（実態と重複しリジッドボディが表示状態になるのでインスタンスを非表示にする必要がある）
 カメラ位置も調整が必要だが
1. エラーが発生した場合（元々のpmxがおかしくテクスチャ不足でパックできないなど）でも、継続したほうがよい。大量実行時、どこまで終わったのか確認して再開するのが面倒だから。
その場合タグでテクスチャエラーのタグを付けるなどは必要。
  エラーの詳細確認も含めて、import時のログをtextで付属させても良いかもしれない（実装方法未調査）
1. Uuunyaa assetのタグやプレビューを利用すると便利だと思うが未実装。参考：https://github.com/UuuNyaa/blender_mmd_assets#get-latest-assetsjson
1. 全般的にPython,Blenderとも初めて作成したのでコードのお作法がおかしい可能性がある
1. アセットブラウザからblendアセットファイルを開くと以下のエラーが出る
```
Read blend: C:\bData\asset3.0\MMDtest\鬥呵廠.blend
find_node_operation: Failed for (RIGIDBODY_REBUILD, '')
add_relation(Rigid Body Rebuild -> Point Cache Reset) - Could not find op_from (OperationKey(type: TRANSFORM, component name: '', operation code: RIGIDBODY_REBUILD))
add_relation(Rigid Body Rebuild -> Point Cache Reset) - Failed, but op_to (ComponentKey(OB014_蜑肴漕_0_0, POINT_CACHE)) was ok
find_node_operation: Failed for (RIGIDBODY_REBUILD, '')
add_relation(Rigid Body Rebuild -> Point Cache Reset) - Could not find op_from (OperationKey(type: TRANSFORM, component name: '', operation code: RIGIDBODY_REBUILD))
add_relation(Rigid Body Rebuild -> Point Cache Reset) - Failed, but op_to (ComponentKey(OB01B_蜑肴漕_1_0, POINT_CACHE)) was ok
```

BUG:
1. 根暗少女(c)をアセット化すると非常に長い時間がかかりアボートした。Dependancy Cycle detectedのせい？　ログにより解析要