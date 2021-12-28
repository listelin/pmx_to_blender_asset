# pmx_to_blender_asset ＊本アドオンは開発中です

## 概要：　pmxファイルを自動的にBlenderのアセット化するアドオン
前提：mmd_toolsがインストールされていること

![ui](https://user-images.githubusercontent.com/44924233/147586613-118b4c7b-e1d7-40ca-aa77-718fa00622b3.jpg)

### 機能1. 単一pmxファイルのアセット化

1. Asset Folderを指定する。
1. single PMX Azzetizeボタンを押し、pmxファイルを設定すると、pmxファイル名のpmx拡張子をblendに変更したファイルとしてアセット化される（時間がかかります）

   - オプション Asemble：物理／モーフBindなどを設定した状態でアセット化する（時間がかかるためまずはOFFで試すことを推奨）
   - オプション Auto Smooth Mesh:OFFにすると、Auto Smooth をオフにした状態でメッシュで保存する
   - オプション ignore file pack error:テクスチャ不足でファイルパックできないエラーを無視する

1. アセットプレビューの自動設定
    1. Auto Cam=OFF: アクティブなカメラで原点にインポートされたキャラクターを撮影してプレビューに設定する。
    2. Auto Cam=ON: 自動的に一時的なサムネイル用カメラを作成し、プレビューを撮影する

        2.1.  Auto angle=ON: キャラクターの首を中心に正面から見たサムネイルを作成する。 zoom offsetでズームを調整可能。 (首が存在しないアクセサリなどは正面からの全体像が撮影される)

        2.2.  Auto angle=OFF: cam loc、cam rotに手動でカメラ位置を指定する

        Auto cam=onの制約事項：(1) アセットファイルにテンポラリのカメラも保存されます。（ファイル保存時点でカメラがないとファイルプレビューが全体のスクリーンショットになってしまうため）、(2)アセット保存ファイルのレンダーエンジンはEeveeに変更されます。（Cyclesの場合ファイルプレビューがworkbenchになってしまうため）。プレビュー撮影自体は事前にCyclesにしていればCyclesでプレビュー撮影されます

        
    - いずれの場合でも、照明は実行時点のblendファイルの設定が採用される。
    - 実行時点のファイルがそのままアセットファイルになるため不要なオブジェクトがない状態で実行することを推奨。

* アセットのblendファイルには"PMX asset info.txt"が追加され、元PMXファイルのパス名、及びエラー（テクスチャエラーなど）の情報が記録されます。

### 機能2. アセットプレビュー自動設定
- 3Dviewport もしくは Outlinerで、アセット化を選択し、"Set Asset IMG"を押すことで、レンダリングとプレビュー設定を行うことが出来る
    * アセットブラウザでの選択には対応していません。

### 機能3.一括アセット化
1. PMX Folderと、Asset Folderを指定する
2. Batch Assetizeボタンを押すとPMX Folderに含まれる全てのpmxファイルを一括でblendファイルにアセット化。
    * オプション Preserve foler structure：元のディレクトリ構造を維持します。

        例： pmx folderがC:\pmx で、C:\pmx\miku\miku.pmx 、C:\pmx\rin\rin.pmx、があり、
            asset folderが、D:\assetの場合、D:\asset\miku\miku.pmx、D:\asset\rin\rin.pmxが作成されます。<br>
            このオプションが指定されない場合は、D:\asset\miku.pmx 、D:\asset\rin.pmxが作成されます。


### アセットの利用方法
1. アセットブラウザから3D Viewportにアセットをドラッグドロップすると、MMDモデルの実体とインスタンスの２つが3D Viewportに現れます。　インスタンスは不要なので削除してください
2. MMDモデルを選択し、MMD/Model Setupの可視性：リセットを押すことでリジッドボディなどの可視性を正常に戻すことが出来ます
3. 物理を動かすためには、MMD/Scen Setup：Update Worldを押して、Appendしたリジッドボディを有効化する必要があります


## 重要な注意事項
- 同一pmxファイル名をアセット化した場合、アセットは上書きされる。プリファレンスのバージョン保存設定によりblend1,blend2...は作成される。* オプション Preserve foler structureをONにすれば重複はしません
- 元々のpmxにテクスチャ不足などがあった場合でも無視してアセット化します。コンソールログにエラーは出しますが、大量のログがあるため確認が難しいと思われます。"PMX asset info.txt"というテキストファイルにオリジナルのPMXのパス名とエラー内容が記録されているので確認してください。
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
1. 手動でのアセット化より遅い気がするが要性能確認
1. タグを付けるべき（MMDなど）だが、bpy.ops.asset.tag_add()の使い方がわからない。
1. auto angleの改善
    - キャラクターの場合は身長にあわせて位置調整するが、Zoomが適切でない場合がある
    - 背景、小物、アクセサリの場合は正面からの撮影 bpy.ops.view3d.camera_to_view_selected() だが斜めからの撮影にすべき

1. バッチアセット化の際、対象のバリエーション（服の違いなど）がインポートされる。ショートカットにより必要なpmxファイルだけを集めたフォルダを作成し、それをインポート対象pmxフォルダに指定することができれば便利だが、Path().rglobがWindowsのショートカットを追ってくれない
1. アセット利用時の３ステップ（インスタンス削除、可視性リセット、Update World）は煩雑なので、自動化出来ないか？ (おそらく無理)
1. エラーが発生した場合（元々のpmxがおかしくテクスチャ不足でパックできないなど）、ログだけにファイルを出力しているが、タグでテクスチャエラーのタグを付けるなどでエラー有無を判別できるべき
1. toonテクスチャがないpmxの場合は、toonテクスチャをOFFにしてアセット化すべきかもしれない
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
1. Add on Physics ver1.の set asset img
```
find_node_operation: Failed for (BONE_DONE, '')
add_relation(Copy Location) - Could not find op_from (OperationKey(type: BONE, component name: '鬥・, operation code: BONE_DONE))
add_relation(Copy Location) - Failed, but op_to (OperationKey(type: TRANSFORM, component name: '', operation code: TRANSFORM_CONSTRAINTS)) was ok
```
