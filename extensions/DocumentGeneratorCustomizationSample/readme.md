# ドキュメント出力内容カスタマイズエクステンションサンプル

ドキュメント出力機能をカスタマイズするエクステンションのサンプルです。

標準のドキュメント出力からの変化点は次の通りです。

* モデルごとのビューがビュー定義順で出力されます。
* ドキュメントフォーム上のフィールドのうち次の条件に合致するものは出力されません。
    * 値が未設定のテキストフィールドとリッチテキストフィールド
    * 関連先モデルが未設定のグリッドとリスト

ドキュメント出力機能のカスタマイズの詳細は次のマニュアルを参照ください。

* [エクステンション開発マニュアル > 高度なトピック > ドキュメント出力内容のカスタマイズ](https://docs.nextdesign.app/extension/docs/advanced/custom-document-export)

## 必ずお読みください

* 本サンプルはお客様が対象製品を有効に活用頂く上で参考にしていただくことを想定したものであり、一切の保証は行いません。
* 本サンプルは Next Design の使用許諾におけるサンプル扱いとなっています。
    詳しくは [Next Design 使用許諾契約書](https://www.nextdesign.app/agreements/LicenseAgreement.pdf) をご確認ください。

## 利用方法

* Visual Studio 2019 で次のソリューションを開き、ビルドしてください。

    > DocumentGeneratorCustomizationSample.sln

* ビルドに成功すると、次のフォルダにエクステンションが自動的に配置されます。

    > {ユーザーのホームパス}\AppData\Local\DENSO CREATE\Next Design\extensions\DocumentGeneratorCustomizationSample

    ユーザーのホームパスの例： C:\Users\user-name

* Next Design でプロジェクトを開いてドキュメント出力を行うと、カスタマイズされた
  ドキュメントが出力されます。

* 本エクステンションの機能を無効化するには、配置されたエクステンションのフォルダを削除してください。

ご不明な点等ございましたら、下記までお問い合わせください。  
ndsupport@denso-create.jp

----
Copyright (C) 2022 DENSO CREATE INC. All rights reserved.
