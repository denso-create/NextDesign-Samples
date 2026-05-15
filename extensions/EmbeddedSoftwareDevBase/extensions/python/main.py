"""main.py : このエクステンションのエントリーポイント"""

from nd import * # NextDesign APIのインテリセンス情報を読み込みます。

# 分割して実装された全ファイルを読み込みます。
from update_id import update_id # 「IDを更新」機能
from derive_test_results import derive_test_results # 「テスト結果モデルを導出」機能
from count_test_results import count_test_results # 「テスト結果を集計」機能
from search_impacted_components_and_interfaces import search_impacted_components_and_interfaces # 「IFの影響箇所を抽出」機能
from derive_software_requirements import derive_software_requirements # 「ソフトウェア要求モデルを導出」機能