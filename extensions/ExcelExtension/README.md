# Excel連携エクステンションサンプル

<div style="text-align: right">株式会社デンソークリエイト</div>

## 概要

* Next Design の導入時、既存資産をいかにして効率よくモデル化できるかが課題になります。
  この課題に対して Next Design では、エクステンションを開発して既存資産の外部ファイルをインポートすることで、モデルを自動作成できます。
* 本プログラムでは、特定フォーマットの Excel シートをインポートして、階層構造のモデルを自動作成します。
  加えて、階層構造のモデルから Excel シートへのエクスポートも行えます。

## 必ずお読みください

* 本サンプルはお客様が対象製品を有効に活用頂く上で参考にしていただくことを想定したものであり、一切の保証は行いません。
* 本サンプルは Next Design の使用許諾におけるサンプル扱いとなっています。
  詳しくは [Next Design 使用許諾契約書](https://www.nextdesign.app/agreements/LicenseAgreement.pdf) をご確認ください。

## 対象バージョン

* Next Design V3.1

## 利用方法

* Visual Studio 2022 以降で次のファイルを開き、ビルドしてください。

    > src\ExcelExtension.sln

    なお、ビルドするためには、事前に次のパッケージをインストールしておく必要があります。

    > .NET SDK 6.0.x  
    > <https://dotnet.microsoft.com/ja-jp/download/dotnet/6.0>

* Next Design で次のプロジェクトを開きます。

    > src\ExcelExtension\pkgContents\samples\Excel連携サンプルプロジェクト.nproj

* Next Design のモデルナビゲータで、次のモデルを選択します。

    > Excel連携サンプルプロジェクト/ソフト設計/ソフト構造

* UIリボンから [エクステンション] > [データ連携] > [Excel インポート] をクリックします。
* 次の Excel ファイルを選択します。

    > src\ExcelExtension\pkgContents\samples\Excel連携データ.xlsx

* Excel ファイルに記述されたレイヤとコンポーネントが Next Design にインポートされます。
* 次に Next Design のモデルナビゲータで任意の [ソフト構造] モデルを選択します。
* UIリボンから [エクステンション] > [データ連携] > [Excel エクスポート] をクリックします。
* 出力先の Excel ファイルを指定します。
* Next Design でモデリングされた [ソフト構造] モデルが Excel ファイルにエクスポートされます。

## 注意事項

* インポート／エクスポートする Excel ファイルを Excel で開いているとインポート／エクスポートに失敗します。
* インポート対象の Excel ファイルへの行追加には対応していますが、列追加・列移動には対応していません。

## 構成ファイル

Visual Studio 2022 以降でビルド・デバッグ実行が可能なエクステンション開発プロジェクト一式が含まれています。

* src
    * ExcelExtension.sln ほかプロジェクト一式
* src\ExcelExtension\pkgContents\samples
    * Excel連携サンプルプロジェクト.nproj
    * Excel連携データ.xlsx

## プログラムのポイント

### エクステンション処理の開始

* Excel インポートボタンおよび Excel エクスポートボタンを押下すると、次のメソッドが呼び出されます（エントリーポイントのコマンドハンドラ）。

    > src\ExcelExtension\ExcelExtension.cs : ExcelExtension クラスの Import メソッド
    > src\ExcelExtension\ExcelExtension.cs : ExcelExtension クラスの Export メソッド

### Excel ファイルの読み込み

* Excel ファイルの読み込み処理は、次のメソッドに実装されています。

    > src\ExcelExtension\ExcelHandler.cs : ExcelHandler クラスの Read メソッド

* Excelファイルの操作にはオープンソースの NPOI を利用しています。

    > <https://github.com/nissl-lab/npoi>

    > <https://www.nuget.org/packages/NPOI/>

### Next Design への書き込み

* Next Design への書き込み処理は、次のメソッドに実装されています。

    > src\ExcelExtension\SoftwareStructureModelHandler.cs : SoftwareStructureModelHandler クラスの AddStructuredModel メソッド

* Next Design への書き込み処理中の次の箇所で、エクステンション API を利用しています。

    ```
    var addedModel = model.AddNewModel(childrenFieldName, dto.ClassName);

    addedModel.SetField("Name", dto.Name);
    addedModel.SetField("Responsibility", dto.Responsibility);
    ```

    * API: IModel.AddNewModel メソッド
    * API: IModel.SetField メソッド

* Next Design で開いている書き込み先のモデルは、次の箇所でエクステンション API を利用して特定しています。

    > src\ExcelExtension\ExcelExtension.cs : ExcelExtension クラスの Import メソッド内

    ```
    var targetModel = m_Context.App.Window.EditorPage.CurrentModel;
    ```

    * API: IEditorPage.CurrentModel プロパティ

### エクスポート時のモデル情報の読み込み

* エクスポートするモデル情報を Next Design から読み込む処理は、次のメソッドに実装されています。

    > src\ExcelExtension\SoftwareStructureModelHandler.cs : SoftwareStructureModelHandler クラスの FetchStructuredModel メソッド

* モデル情報の読み込み処理では、次のエクステンション API を利用しています。

    * API: IModel.GetFieldString メソッド
    * API: IModel.GetFieldValues メソッド
    * API: IModel.Metaclass プロパティ

### Excel ファイルの書き込み

* Excel ファイルの書き込み処理は、次のメソッドに実装されています。

    > src\ExcelExtension\ExcelHandler.cs : ExcelHandler クラスの Write メソッド

## 注意事項

* インポート・エクスポートする Excel ファイルを Excel で開いたままエクステンション機能を実行するとエラーになります。
* インポートする Excel シートへの行追加には対応していますが、列追加・列移動には対応していません。

----
Copyright (C) 2021 DENSO CREATE INC. All rights reserved.
