# Excelインポートエクステンションサンプル

<div style="text-align: right">株式会社デンソークリエイト</div>

## 概要

* Next Design の導入時、既存資産をいかにして効率よくモデル化できるかが課題になります。
  この課題に対して Next Design では、エクステンションを開発して既存資産の外部ファイルをインポートすることで、モデルを自動作成できます。
* 本プログラムでは、特定フォーマットの Excel シートをインポートして、階層構造のモデルを自動作成します。

## 必ずお読みください

* 本サンプルはお客様が対象製品を有効に活用頂く上で参考にしていただくことを想定したものであり、一切の保証は行いません。
* 本サンプルは Next Design の使用許諾におけるサンプル扱いとなっています。
    詳しくは [Next Design 使用許諾契約書](https://www.nextdesign.app/agreements/LicenseAgreement.pdf) をご確認ください。

## 利用方法

* 次の Visual Studio Solution を開き、ビルドしてください。

    > src\ExcelImportExtension.sln

    なお、ビルドするためには、事前に次のパッケージをインストールしておく必要があります。

    > .NET Core 3.1 SDK  
    > <https://dotnet.microsoft.com/en-us/download/dotnet/3.1>

* Next Design で次のプロジェクトを開きます。

    > sample-files\ExcelImportProject.nproj

* Next Design のモデルナビゲータで、次のモデルを選択します。

    > Excelインポート・サンプルプロジェクト/ソフト設計/ソフト構造

* UIリボンから [エクステンション] > [データ連携] > [Excel インポート] をクリックします。
* 次の Excel ファイルを選択します。

    > sample-files\ExcelImportData.xlsx

* Excel ファイルに記述されたレイヤとコンポーネントが Next Design にインポートされます。

## 注意事項

* インポートする Excel ファイルを Excel で開いているとインポートできません。
* Excel ファイルへの行追加には対応していますが、列追加・列移動には対応していません。

## 構成ファイル

Visual Studio 2019 以降でビルド・デバッグ実行が可能なエクステンション開発プロジェクト一式が含まれています。

* src
    * ExcelImportExtension.sln ほかプロジェクト一式
* sample-files
    * ExcelImportProject.nproj
    * ExcelImportData.xlsx

## プログラムのポイント

### エクステンション処理の開始

* Excel インポートボタンを押下すると、次のメソッドが呼び出されます（エントリーポイントのコマンドハンドラ）。

    > src\ExcelImportExtension\ExcelImportExtension.cs : ExcelImportExtension クラスの Run メソッド

### Excel ファイルの読み込み

* Excel ファイルの読み込み処理は、次のメソッドに実装されています。

    > src\ExcelImportExtension\DataReader\ExcelReader.cs : ExcelReader クラスの Read メソッド

* Excelファイルの操作にはオープンソースの NPOI を利用しています。

    > <https://github.com/nissl-lab/npoi>

    > <https://www.nuget.org/packages/NPOI/>

### Next Design への書き込み

* Next Design への書き込み処理は、次のメソッドに実装されています。

    > src\ExcelImportExtension\ModelBuilder\SoftwareStructureModelBuilder.cs : SoftwareStructureModelBuilder クラスの AddStructuredModel メソッド

* Next Design への書き込み処理中の次の箇所で、エクステンション API を利用しています。

    ```
    var addedModel = model.AddNewModel(childrenFieldName, dto.ClassName);

    addedModel.SetField("Name", dto.Name);
    addedModel.SetField("Responsibility", dto.Responsibility);
    ```

    * API: IModel.AddNewModel メソッド
    * API: IModel.SetField メソッド

* Next Design で開いている書き込み先のモデルは、次の箇所でエクステンション API を利用して特定しています。

    > src\ExcelImportExtension\ExcelImportExtension.cs : ExcelImportExtension クラスの Run メソッド内

    ```
    var targetModel = m_Context.App.Window.EditorPage.CurrentModel;
    ```

    * API: IEditorPage.CurrentModel プロパティ

----
Copyright (C) 2019 DENSO CREATE INC. All rights reserved.
