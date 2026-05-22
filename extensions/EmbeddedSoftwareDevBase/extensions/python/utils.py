"""汎用ユーティリティ関数群

異なる機能で使いまわせる汎用的な関数を定義します。
"""

from typing import TYPE_CHECKING, List  # 型検査中か否かを表すTYPE_CHECKINGと、型注釈で使う型

# エントリポイントであるmain.py以外でndモジュールをインポートすると実行時にエラーになります。
# そのため、TYPE_CHECKINGを用いて型検査時のみインポートします。
if TYPE_CHECKING:
    from nd import *

def get_selected_models(context: "ICommandContext") -> List["IModel"]:
    """現在のエディタで選択中のモデル取得関数

    Args:
        context: コマンドコンテキスト
    Returns:
        選択中のモデル群（選択されていない場合は空のリスト）
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.CurrentEditorView:
        models = context.App.Window.EditorPage.CurrentEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def get_selected_models_in_main_editor(context: "ICommandContext") -> List["IModel"]:
    """メインエディタで選択中のモデル取得関数

    Args:
        context: コマンドコンテキスト
    Returns:
        メインエディタで選択中のモデル群（選択されていない場合は空のリスト）
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.MainEditorView:
        models = context.App.Window.EditorPage.MainEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def get_selected_models_in_sub_editor(context: "ICommandContext") -> List["IModel"]:
    """サブエディタで選択中のモデル取得関数

    Args:
        context: コマンドコンテキスト
    Returns:
        サブエディタで選択中のモデル群（選択されていない場合は空のリスト）
    """
    models = None
    if context.App.Window.EditorPage and context.App.Window.EditorPage.SubEditorView:
        models = context.App.Window.EditorPage.SubEditorView.SelectedModels

    if models is None:
        return []

    return list(models)

def collect_selected_root_models(
    target_model: "IModel",
    selected_models: List["IModel"],
    target_classes: List[str],
    results: List["IModel"]
) -> None:
    """選択ルートモデル取得関数
    選択されているモデルのうち、祖先に選択されたモデルを持たないものを取得します。
    探索対象モデルから再帰的に探索します。

    Args:
        target_model: 探索対象モデル
        selected_models: 選択モデル群
        target_classes: 対象とするモデルのクラス名
        results: 対象結果格納用リスト
    """
    if target_model in selected_models:
        # 選択中の場合は、結果に追加します。
        results.append(target_model)
    else:
        # 選択中でない場合は、子モデルを再帰的に探索します。
        children = [model for model in target_model.GetChildren() if model.AsIn(classNames=target_classes)]
        for child in children:
            collect_selected_root_models(child, selected_models, target_classes, results)

