## モデル名一意制約エクステンションサンプル

<div style="text-align: right">株式会社デンソークリエイト</div>

## 概要

特定フィールドの兄弟モデルで名前が重複しないように制限する Next Design 用エクステンションサンプルです。

`IsUniqueNameEnforced` タグが付与された所有関連フィールドを対象に、名前の一意性を検証します。

## 必ずお読みください

* 本サンプルはお客様が対象製品を有効に活用頂く上で参考にしていただくことを想定したものであり、一切の保証は行いません。
* 本サンプルは Next Design の使用許諾におけるサンプル扱いとなっています。
    詳しくは [Next Design 使用許諾契約書](https://www.nextdesign.app/agreements/LicenseAgreement.pdf) をご確認ください。

## 利用方法

1. 対象としたい所有関連フィールドに、タグ `IsUniqueNameEnforced` を設定します。値は `true` を指定してください。
2. 本エクステンションを Next Design に読み込みます。
3. 対象フィールド配下のモデルの「名前」を変更すると、兄弟モデル間で名前の重複が自動的にチェックされます。

## 機能概要

- モデルのフィールド値変更イベントをフックし、名前の変更時に以下をチェックします:
	- 親モデルが存在すること
	- 所有関連フィールドに `IsUniqueNameEnforced` タグが付与されていること
	- 現在の名前がデフォルト値（またはメタクラスの表示名）と異なること
	- 同一フィールド内の兄弟モデルに、同じ名前を持つモデルが存在しないこと
- 重複している場合はメッセージボックスで通知し、変更をキャンセルします。

## 実装概要

- エントリポイント: `RestrictNamesUniqueEntryPoint` (`RestrictNamesUniqueEntryPoint.cs`)
	- アクティベート時にモデルフィールド変更イベントハンドラ `ModelFieldChanged` を登録します。
	- タグ名定数 `c_TagName_IsUniqueNameEnforced` を共通定義しています。

- イベントハンドラ: `ModelFieldChanged` (`Events/ModelFieldChanged.cs`)
	- `ModelsFieldChangedEventHandlerBase` を継承し、`OnHandle` で検証処理を実装しています。
	- タグ名には `RestrictNamesUniqueEntryPoint.c_TagName_IsUniqueNameEnforced` を使用します。

## 備考

- 名前がデフォルト値（またはメタクラス表示名）の場合は、ユーザーがまだ名前を設定していないとみなし、重複チェックの対象外としています。
- エクステンションの配置方法は、Next Design のドキュメントを参照してください。
