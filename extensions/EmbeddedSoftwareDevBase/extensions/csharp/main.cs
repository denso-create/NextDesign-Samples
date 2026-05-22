// =======================================
// main.cs : このエクステンションのエントリーポイント
// =======================================

// 分割して実装された全ファイルを読み込みます。
#load "updateId.cs"                              // 「IDを更新」機能
#load "deriveTestResults.cs"                     // 「テスト結果モデルを導出」機能
#load "countTestResults.cs"                      // 「テスト結果を集計」機能
#load "searchImpactedComponentsAndInterfaces.cs" // 「IFの影響箇所を抽出」機能
#load "deriveSoftwareRequirements.cs"            // 「ソフトウェア要求モデルを導出」機能