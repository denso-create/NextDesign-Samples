# 名前の重複ミスを防ぐエクステンションサンプル

<div style="text-align: right">株式会社デンソークリエイト</div>

## 概要

名前の重複ミスを自動検出し、モデル名の一意性を確保する Next Design 用エクステンションサンプルです。

一意性チェックの対象とする所有フィールドはメタモデルで柔軟に指定できます。

## 必ずお読みください

* 本サンプルはお客様が対象製品を有効に活用頂く上で参考にしていただくことを想定したものであり、一切の保証は行いません。
* 本サンプルは Next Design の使用許諾におけるサンプル扱いとなっています。
    詳しくは [Next Design 使用許諾契約書](https://www.nextdesign.app/agreements/LicenseAgreement.pdf) をご確認ください。

## 利用方法

1. 次のマニュアルを参考に本エクステンションをビルドします。  
   > [Next Design エクステンション開発マニュアル > クイックスタート](https://docs.nextdesign.app/extension/docs/getting-started/intro)

   ビルドに成功すると自動配置され、Next Deisgn を起動時にエクステンションが有効化されます。

2. メタモデルを編集し、対象としたい所有関連フィールドにタグ `IsUniqueNameEnforced` を設定します。値は `true` を指定してください。
3. リボンタブから [ホーム] > [モデル] > [エラーチェック] を実行すると、プロジェクト内の全モデルを対象に重複チェックを行います。
4. 対象フィールド配下のモデルの「名前」を変更すると、兄弟モデル間で名前の重複が自動的にチェックされ、重複する場合は変更がキャンセルされます。

本エクステンションの動作確認には、次のサンプルプロジェクトファイルを利用できます。

* `RestrictNamesUnique/pkgContents/samples/RestrictNamesUniqueSample.nproj`

## 機能概要

- エラーチェック実行時
  - モデルのエラーチェックイベントをフックし、次のルールで対象モデルを判別しチェックします。
	- 親モデルが存在すること
	- 所有関連フィールドに `IsUniqueNameEnforced` タグが付与されていること
	- 現在の名前が初期値（初期値未設定の場合はクラスの表示名）と異なること
	- 同一フィールド内の兄弟モデルに、同じ名前を持つモデルが存在しないこと
  - モデルの名前が重複している場合は、モデルにエラーを追加します。

- モデルのフィールド編集時
  - モデルのフィールド値変更イベントをフックし、上記と同様のルールでチェックします。
  - モデルの名前が重複している場合は、メッセージボックスで通知して変更をキャンセルします。

## 実装概要

- エントリポイント: `RestrictNamesUniqueEntryPoint` (`RestrictNamesUniqueEntryPoint.cs`)
	- アクティベート時にモデルフィールド変更イベントハンドラ `ModelsFieldChangedEvent` と、モデル検証イベントハンドラ `ModelsValidateEvent` を登録します。
	- 名前の一意性を判定する共通ロジックは `NameUniquenessRules` (`NameUniquenessRules.cs`) に実装しています。

- イベントハンドラ: `ModelsFieldChangedEvent` (`Events/ModelsFieldChangedEvent.cs`)
	- `ModelsFieldChangedEventHandlerBase` を継承し、`OnHandle` でフィールド編集時の検証処理を実装しています。
	- モデルの名前が重複している場合は、メッセージボックスで通知して変更をキャンセルします。

- イベントハンドラ: `ModelsValidateEvent` (`Events/ModelsValidateEvent.cs`)
	- `ModelsValidateEventHandlerBase` を継承し、エラーチェック実行時に対象モデルの名前一意性を検証します。
	- モデルの名前が重複している場合は、モデルにエラーを追加します。

## 備考

- 名前が初期値（初期値未設定の場合はクラスの表示名）の場合は、ユーザーがまだ名前を設定していないとみなし、重複チェックの対象外としています。
- これにより、設計開始時点で必要なモデルの枠を準備するといった操作が許容されます。

以上
