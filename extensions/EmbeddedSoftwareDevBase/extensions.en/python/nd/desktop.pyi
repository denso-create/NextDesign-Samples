# ============================================================
# This file was auto-generated. Do not edit directly.
# ------------------------------------------------------------
# Source DLL   : NextDesign.Desktop.dll
# Version      : 5.0.0.10306
# Generated at : 2026-03-11 09:56:28
# ============================================================

from typing import Any, Callable, Dict, Iterable, Iterator, List, overload
from enum import IntEnum

from .core import *

class ICommand:
    """
    コマンド定義情報を提供します。
    """
    @property
    def Owner(self) -> IExtensionInfo:
        """オーナ"""
        ...
    @property
    def Id(self) -> str:
        """コマンドの識別子"""
        ...
    @property
    def Title(self) -> str:
        """コマンド名"""
        ...
    @property
    def Description(self) -> str:
        """コマンド説明"""
        ...
    @property
    def ExecFunc(self) -> str:
        """コマンド実行関数名"""
        ...
    @property
    def CanExecFunc(self) -> str:
        """コマンド実行可否評価関数名"""
        ...

class ICommandCollection:
    """
    コマンド定義情報のコレクションです。
    """
    def GetItem(self, index: int) -> ICommand:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ICommand: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ICommandEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ICommandEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ICommand]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IContext:
    """
    コンテキストインタフェース
    """
    def HasProperty(self, name: str) -> bool:
        """
        指定された識別名のプロパティ値があるか

        Args:
            name (str): 識別名

        Returns:
            bool: プロパティ値がある場合は真
        """
        ...
    def GetProperty(self, name: str) -> Any:
        """
        指定された識別名のプロパティ値を取得します

        Args:
            name (str): 識別名

        Returns:
            Any: プロパティ値
        """
        ...
    def SetProperty(self, name: str, value: Any) -> None:
        """
        指定された識別名のプロパティ値を設定します。

        Args:
            name (str): 識別名
            value (Any): プロパティ値

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveProperty(self, name: str) -> None:
        """
        指定された識別子名のプロパティ値を削除します。

        Args:
            name (str): 識別名

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetPropertyNames(self) -> Iterable[str]:
        """
        プロパティの識別名一覧を取得します

        Returns:
            Iterable[str]: プロパティの識別名一覧
        """
        ...
    def GetProperties(self) -> Dict[str, Any]:
        """
        プロパティ一覧を取得します

        Returns:
            Dict[str, Any]: プロパティ一覧
        """
        ...
    def GetResourceString(self, key: str) -> str:
        """
        指定されたリソースキーの文字列を取得します

        Args:
            key (str): リソースキー

        Returns:
            str: リソース文字列
        """
        ...
    def GetResourceString1(self, key: str, param1: Any) -> str:
        """
        指定されたリソースキーの文字列を取得します。
        このときリソースで定義された置換子\"{0}\"は、
        引数で指定されたの文字列表現に置き換わります。

        Args:
            key (str): リソースキー
            param1 (Any): パラメータ1

        Returns:
            str: リソース文字列
        """
        ...
    def GetResourceString2(self, key: str, param1: Any, param2: Any) -> str:
        """
        指定されたリソースキーの文字列を取得します。
        このときリソースで定義された置換子\"{0},{1}\"は、
        それぞれ引数で指定された, の文字列表現に置き換わります。

        Args:
            key (str): リソースキー
            param1 (Any): パラメータ1
            param2 (Any): パラメータ2

        Returns:
            str: リソース文字列
        """
        ...
    def GetResourceString3(self, key: str, param1: Any, param2: Any, param3: Any) -> str:
        """
        指定されたリソースキーの文字列を取得します。
        このときリソースで定義された置換子\"{0},{1},{2}\"は、
        それぞれ引数で指定された, , の文字列表現に置き換わります。

        Args:
            key (str): リソースキー
            param1 (Any): パラメータ1
            param2 (Any): パラメータ2
            param3 (Any): パラメータ3

        Returns:
            str: リソース文字列
        """
        ...
    @property
    def Application(self) -> IApplication:
        """共有変数"""
        ...
    @property
    def App(self) -> IApplication:
        """共有変数"""
        ...
    @property
    def Extension(self) -> IExtensionInfo:
        """現在有効なエクステンション情報"""
        ...
    @property
    def ExtensionInfo(self) -> IExtensionInfo:
        """現在有効なエクステンション情報"""
        ...
    @property
    def ContextOption(self) -> IContextOption:
        """コンテキストオプション
このコンテキストが有効な期間におけるオプション定義"""
        ...

class ICommandContext(IContext):
    """
    コマンド実行コンテキストです。
    """
    @property
    def SenderModel(self) -> IModel:
        """コマンドがモデルに関連づいている場合はそのモデル"""
        ...
    @property
    def Command(self) -> ICommand:
        """現在実行中のコマンド情報"""
        ...
    @property
    def Global(self) -> IContext:
        """エクステンション共有コンテキスト"""
        ...

class ICommandEnumerator:
    """
    コマンド定義情報のコレクションの列挙子です。
    """
    ...

class ICommandManager:
    """
    コマンドマネージャです。
    Extensionで追加登録するコマンド、およびアプリケーションが提供するシステムコマンド
    を管理します。
    """
    def GetCommand(self, commandIdentifier: str) -> ICommand:
        """
        指定された識別子のコマンドを取得します

        Args:
            commandIdentifier (str): コマンド識別子

        Returns:
            ICommand: コマンド
        """
        ...
    def ExecuteCommand(self, commandIdentifier: str, commandParams: ICommandParams) -> None:
        """
        指定された識別子のコマンドを実行します。
        これは、Extensionから別のExtensionを実行する際に使用します。

        Args:
            commandIdentifier (str): コマンド識別子
            commandParams (ICommandParams): コマンドパラメータ

        Returns:
            None: This method does not return a value.
        """
        ...
    def CanExecuteCommand(self, commandIdentifier: str) -> bool:
        """
        指定された識別子のコマンドを実行可能であるか調べます。
        これは、Extensionから別のExtensionを実行する際に、その可否判断に用います。

        Args:
            commandIdentifier (str): コマンド識別子

        Returns:
            bool: 実行可能な場合は真
        """
        ...
    def CreateCommandParams(self) -> ICommandParams:
        """
        コマンドパラメータを作成します。

        Returns:
            ICommandParams: 作成したコマンドパラメータ
        """
        ...
    @property
    def AllCommands(self) -> ICommandCollection:
        """コマンド一覧"""
        ...

class ICommandParams:
    """
    コマンドパラメータを表します。
    """
    def ToArray(self) -> List[Any]:
        """
        パラメータの内容をオブジェクト配列に変換します。

        Returns:
            List[Any]: オブジェクト配列
        """
        ...
    def AddParam(self, value: Any) -> None:
        """
        パラメータに値を追加します。

        Args:
            value (Any): 追加対象

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddParamWithName(self, name: str, value: Any) -> None:
        """
        パラメータに値を追加します。

        Args:
            name (str): 名前
            value (Any): 追加対象

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetByIndex(self, index: int) -> Any:
        """
        指定パラメータの値をインデックスで取得します

        Args:
            index (int): インデックス

        Returns:
            Any: 指定パラメータの値
        """
        ...
    def GetByName(self, name: str) -> Any:
        """
        指定パラメータの値をパラメータ名で取得します

        Args:
            name (str): パラメータ名

        Returns:
            Any: 指定パラメータの値
        """
        ...
    def ToCollection(self) -> Any:
        """
        パラメータの内容をオブジェクトコレクションに変換します。

        Returns:
            Any: オブジェクトコレクション
        """
        ...
    @overload
    def __getitem__(self, index: int) -> Any: ...
    @overload
    def __getitem__(self, name: str) -> Any: ...

class DesktopExtensionObjectConverter:
    """
    Next Designの内部オブジェクトをエクステンションのオブジェクトへ変換するコンバータークラスです
    """
    ...

class DesktopExtensionObjectConverterRegistry:
    """
    エクステンションオブジェクトに関するコールバックを登録します。
    （Next Designアプリケーションが利用する内部用のインターフェースです。ユーザは利用しないで下さい。）
    """
    ...

class IEventParams:
    """
    イベントパラメータです。
    """
    ...

class EventParams(IEventParams):
    """
    イベントパラメータ基底
    """
    def GetDefaultEventName(self) -> str:
        """
        イベントパラメータに対応するイベント名を取得します

        Returns:
            str: イベント名
        """
        ...

class CancelableEventParams(EventParams):
    """
    キャンセル可能なイベントパラメータ基底
    """
    def Cancel(self) -> None:
        """
        イベントのキャンセルを要求する

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Canceled(self) -> bool:
        """イベントがキャンセルされているか"""
        ...

class ConsumableEventParams(EventParams):
    """
    イベント消費可能なイベントパラメータ基底
    """
    def Consume(self) -> None:
        """
        このイベントを消費して、Core側の既定の処理を行わないように要求します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def IsConsume(self) -> bool:
        """このイベントが消費済みであるか"""
        ...

class IEvent:
    """
    イベント情報を提供します。
    """
    @property
    def Area(self) -> str:
        """イベントエリア名"""
        ...
    @property
    def EventName(self) -> str:
        """イベント名"""
        ...
    @property
    def FuncName(self) -> str:
        """ハンドラ関数名"""
        ...

class IEventContext(IContext):
    """
    イベント実行コンテキストです。
    """
    @property
    def Global(self) -> IContext:
        """エクステンション共有コンテキスト"""
        ...
    @property
    def Event(self) -> IEvent:
        """現在実行中のイベント情報"""
        ...

class IModelDictionary:
    """
    モデルIDをキーとするモデルの辞書インターフェースです。
    """
    def Contains(self, model: IModel) -> bool:
        """
        指定したモデルが辞書に含まれているか

        Args:
            model (IModel): モデル

        Returns:
            bool: 含まれている場合はtrue
        """
        ...
    def ContainsById(self, modelId: str) -> bool:
        """
        指定したモデルIDに対するモデルが辞書に含まれているか

        Args:
            modelId (str): モデルID

        Returns:
            bool: 含まれている場合はtrue
        """
        ...
    def GetByClass(self, className: str) -> IModelCollection:
        """
        指定したクラスに対するモデルを取得します

        Args:
            className (str): クラス名

        Returns:
            IModelCollection: モデルの一覧
        """
        ...
    def GetByClasses(self, classNames: List[str]) -> IModelCollection:
        """
        指定したクラス群に対するモデルを取得します

        Args:
            classNames (List[str]): クラス名一覧

        Returns:
            IModelCollection: モデルの一覧
        """
        ...
    def ToList(self) -> IModelCollection:
        """
        辞書で管理しているモデルの一覧を取得します

        Returns:
            IModelCollection: モデルの一覧
        """
        ...

class IExecuteEventParams:
    """
    コマンドイベントの共通パラメータです。
    """
    @property
    def TargetCommandName(self) -> str:
        """イベント発生源のコマンド名"""
        ...

class AfterExecuteEventParams(CancelableEventParams, IExecuteEventParams):
    """
    コマンド実行後イベント
    """
    @property
    def Command(self) -> str:
        """コマンド識別子"""
        ...
    @property
    def Parameters(self) -> Any:
        """パラメータ"""
        ...
    @property
    def TargetCommandName(self) -> str:
        """イベント発生源のコマンド"""
        ...

class AfterStartEventParams(EventParams):
    """
    アプリケーション実行後イベント
    """
    ...

class BeforeExecuteEventParams(CancelableEventParams, IExecuteEventParams):
    """
    コマンド実行前イベント
    """
    @property
    def Command(self) -> str:
        """コマンド識別子"""
        ...
    @property
    def Parameters(self) -> Any:
        """パラメータ"""
        ...
    @property
    def TargetCommandName(self) -> str:
        """イベント発生源のコマンド名"""
        ...

class BeforeQuitEventParams(CancelableEventParams):
    """
    アプリケーション実行前イベント
    """
    ...

class IEditorEventParams:
    """
    ナビゲータイベントの共通パラメータです。
    """
    @property
    def TargetEditorName(self) -> str:
        """イベント発生源のエディタ名"""
        ...

class EditorOnHideEventParams(EventParams, IEditorEventParams):
    """
    エディタ非表示イベント
    """
    @property
    def Editor(self) -> IEditor:
        """エディタ"""
        ...
    @property
    def TargetEditorName(self) -> str:
        """イベント発生源のエディタ名"""
        ...

class EditorOnShowEventParams(EventParams, IEditorEventParams):
    """
    エディタ表示イベント
    """
    @property
    def Editor(self) -> IEditor:
        """エディタ"""
        ...
    @property
    def TargetEditorName(self) -> str:
        """イベント発生源のエディタ名"""
        ...

class EditorSelectionChangedEventParams(EventParams, IEditorEventParams):
    """
    エディタ内モデル選択イベント
    """
    @property
    def Editor(self) -> IEditor:
        """エディタ"""
        ...
    @property
    def SelectedItem(self) -> IRepresentation:
        """選択モデル"""
        ...
    @property
    def TargetEditorName(self) -> str:
        """イベント発生源のエディタ名"""
        ...

class IInformationEventParams:
    """
    情報ビューの共通パラメータです。
    """
    @property
    def Name(self) -> str:
        """情報ビューの種類"""
        ...

class IModelEditedEventParams:
    """
    モデル変更イベントのパラメータです。
    """
    @property
    def Models(self) -> IModelDictionary:
        """変更されたモデルのディクショナリ"""
        ...

class IModelEventParams:
    """
    モデルイベントの共通パラメータです。
    """
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class INavigatorEventParams:
    """
    ナビゲータイベントの共通パラメータです。
    """
    @property
    def TargetNavigatorName(self) -> str:
        """イベント発生源のナビゲータ名"""
        ...

class InformationOnDoubleClickEventParams(ConsumableEventParams, IInformationEventParams):
    """
    情報ビューダブルクリックイベント
    """
    @property
    def Name(self) -> str:
        """情報ビューの種類
\"Error\" | \"SearchResult\" | \"Output\""""
        ...
    @property
    def InfoView(self) -> IInfoView:
        """情報ビューへのアクセスオブジェクト"""
        ...
    @property
    def Item(self) -> Any:
        """ダブルクリックされた要素"""
        ...
    @property
    def Entry(self) -> IInfoEntry:
        """ダブルクリックされた要素"""
        ...
    @property
    def Model(self) -> IModel:
        """ダブルクリックされた要素が関連するモデル"""
        ...

class InformationOnHideEventParams(EventParams, IInformationEventParams):
    """
    情報ビュー非表示イベント
    """
    @property
    def Name(self) -> str:
        """情報ビューの種類"""
        ...

class InformationOnShowEventParams(EventParams, IInformationEventParams):
    """
    情報ビュー表示イベント
    """
    @property
    def Name(self) -> str:
        """情報ビューの種類"""
        ...

class InformationSelectionChangedEventParams(EventParams, IInformationEventParams):
    """
    情報ビュー要素選択イベント
    """
    @property
    def Name(self) -> str:
        """情報ビューの種類"""
        ...

class ModelAfterChangeOrderEventParams(CancelableEventParams, IModelEventParams):
    """
    モデル順序変更後イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def NewIndex(self) -> int:
        """新しい位置"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelAfterChangeOwnerEventParams(CancelableEventParams, IModelEventParams):
    """
    モデルオーナー変更後イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def NewOwner(self) -> IModel:
        """新しい親"""
        ...
    @property
    def Field(self) -> str:
        """移動先のフィールド"""
        ...
    @property
    def NewIndex(self) -> int:
        """移動先のフィールド位置"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelAfterNewEventParams(CancelableEventParams, IModelEventParams):
    """
    モデル追加後イベント
    """
    @property
    def Owner(self) -> IModel:
        """作成する親オブジェクト"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def Index(self) -> int:
        """作成先のフィールド内のインデックス（コレクションでない場合は0）"""
        ...
    @property
    def NewModel(self) -> IModel:
        """作成したモデル"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelAfterNewRelationEventParams(CancelableEventParams, IModelEventParams):
    """
    関連追加後イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def Index(self) -> int:
        """インデックス（コレクションでない場合は0）"""
        ...
    @property
    def RelatingTo(self) -> IModel:
        """新しい関連先"""
        ...
    @property
    def OppositeField(self) -> str:
        """新しい関連先側のフィールド"""
        ...
    @property
    def OppositeIndex(self) -> int:
        """新しい関連先側のインデックス（コレクションでない場合は0）"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelBeforeChangeOrderEventParams(CancelableEventParams, IModelEventParams):
    """
    モデル順序変更前イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def OldIndex(self) -> int:
        """移動前の位置"""
        ...
    @property
    def NewIndex(self) -> int:
        """新しい位置"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelBeforeChangeOwnerEventParams(CancelableEventParams, IModelEventParams):
    """
    モデルオーナー変更前イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def NewOwner(self) -> IModel:
        """新しい親"""
        ...
    @property
    def Field(self) -> str:
        """移動先のフィールド"""
        ...
    @property
    def NewIndex(self) -> int:
        """移動先のフィールド位置"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelBeforeDeleteEventParams(CancelableEventParams, IModelEventParams):
    """
    モデル削除前イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelBeforeNewEventParams(CancelableEventParams, IModelEventParams):
    """
    モデル追加前イベント
    """
    @property
    def Owner(self) -> IModel:
        """作成する親オブジェクト"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def Index(self) -> int:
        """作成先のフィールド内のインデックス（コレクションでない場合は0）"""
        ...
    @property
    def ClassName(self) -> str:
        """作成するクラス名"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelBeforeNewRelationEventParams(CancelableEventParams, IModelEventParams):
    """
    関連追加前イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def Field(self) -> str:
        """対象フィールド"""
        ...
    @property
    def Index(self) -> int:
        """インデックス（コレクションでない場合は0）"""
        ...
    @property
    def RelatingTo(self) -> IModel:
        """新しい関連先"""
        ...
    @property
    def OppositeField(self) -> str:
        """新しい関連先側のフィールド"""
        ...
    @property
    def OppositeIndex(self) -> int:
        """新しい関連先側のインデックス（コレクションでない場合は0）"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelEditedEventParams(EventParams, IModelEditedEventParams):
    """
    モデル変更イベントのパラメータ
    """
    @property
    def Models(self) -> IModelDictionary:
        """モデルIDをキーとするモデルの辞書"""
        ...

class ModelFieldChangedEventParams(CancelableEventParams, IModelEventParams):
    """
    フィールド値変更後イベント
    """
    @property
    def Model(self) -> IModel:
        """変更のあったモデル"""
        ...
    @property
    def Field(self) -> str:
        """変更のあったフィールド"""
        ...
    @property
    def Index(self) -> int:
        """インデックス（コレクションでない場合は0）"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelOnErrorEventParams(EventParams, IModelEventParams):
    """
    エラー追加時イベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelOnValidateEventParams(EventParams, IModelEventParams):
    """
    モデルバリデートイベント
    """
    @property
    def Model(self) -> IModel:
        """対象モデル"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelSelectionChangedEventParams(EventParams, IModelEventParams):
    """
    モデル選択イベントパラメータ
    """
    @property
    def SelectedItem(self) -> IModel:
        """選択されたモデル"""
        ...
    @property
    def ViewType(self) -> str:
        """ビュータイプ"""
        ...
    @property
    def TargetClassName(self) -> str:
        """イベント発生源のクラスの名前"""
        ...
    @property
    def TargetClassFullName(self) -> str:
        """イベント発生源のクラスの完全修飾型名"""
        ...

class ModelUndoRedoEventParams(EventParams, IModelEditedEventParams):
    """
    アンドゥ・リドゥイベントのパラメータ
    """
    @property
    def Models(self) -> IModelDictionary:
        """モデルIDをキーとするモデルの辞書"""
        ...

class NavigatorOnHideEventParams(EventParams, INavigatorEventParams):
    """
    ナビゲータ非表示イベント
    """
    @property
    def Name(self) -> str:
        """ナビゲータの種類"""
        ...
    @property
    def TargetNavigatorName(self) -> str:
        """イベント発生源のナビゲータ名"""
        ...

class NavigatorOnShowEventParams(EventParams, INavigatorEventParams):
    """
    ナビゲータ表示イベント
    """
    @property
    def Name(self) -> str:
        """ナビゲータの種類"""
        ...
    @property
    def TargetNavigatorName(self) -> str:
        """イベント発生源のナビゲータ名"""
        ...

class NavigatorSelectionChangedEventParams(EventParams, INavigatorEventParams):
    """
    ナビゲータ内モデル選択イベント
    """
    @property
    def Name(self) -> str:
        """ナビゲータの種類"""
        ...
    @property
    def TargetNavigatorName(self) -> str:
        """イベント発生源のナビゲータ名"""
        ...

class PageAfterChangeEventParams(EventParams):
    """
    ページ変更後イベント
    """
    ...

class PageBeforeChangeEventParams(CancelableEventParams):
    """
    ページ変更前イベント
    スタートページからの変更、およびスタートページへの変更の場合はページ変更前イベントのキャンセルを無視します。
    無視した場合は情報ペインの出力タブに上記を伝えるメッセージを表示します。
    出力のカテゴリは\"システム\"です。
    """
    ...

class ProjectAfterCloseEventParams(EventParams):
    """
    プロジェクトクローズ後イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectAfterModelUnitLoadEventParams(EventParams):
    """
    モデルユニットの追加ロード後イベントの引数です。
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def ModelUnits(self) -> IModelUnitCollection:
        """追加ロードに成功したモデルファイルのコレクション"""
        ...

class ProjectAfterNewEventParams(EventParams):
    """
    プロジェクト新規作成後イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...

class ProjectAfterOpenEventParams(EventParams):
    """
    プロジェクトオープン後イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectAfterReloadEventParams(EventParams):
    """
    プロジェクトリロード後イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectAfterSaveEventParams(EventParams):
    """
    プロジェクト保存後イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectBeforeCloseEventParams(CancelableEventParams):
    """
    プロジェクト閉じる前イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...

class ProjectBeforeOpenEventParams(CancelableEventParams):
    """
    プロジェクト開く前イベント
    """
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectBeforeReloadEventParams(CancelableEventParams):
    """
    プロジェクトリロード前イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class ProjectBeforeSaveEventParams(CancelableEventParams):
    """
    プロジェクト保存前イベント
    """
    @property
    def Project(self) -> IProject:
        """プロジェクト"""
        ...
    @property
    def Filename(self) -> str:
        """ファイル名"""
        ...

class EditorAccessMode(IntEnum):
    """
    エディタ情報アクセスモードです。
    """
    None = 0  # 設定なし（既定） 上位スコープのコンテキストオプションに従います。
    ActivateValueOnly = 1  # アプリケーションでアクティブなエディタ情報のみ詳細情報を取得できます。 このモードを指定した場合、非アクティブなエディタ情報の詳細に関しては情報の鮮度を保証しません。
    GetInactiveValue = 2  # アプリケーションで非アクティブなエディタ情報においても詳細情報を取得できます。 このモードを指定した場合、非アクティブなエディタにおいても内部構造を解析するため エディタAPIの応答に解析時間が加算されます。

class IApplication:
    """
    共有変数
    """
    def CreateSearch(self) -> ISearch:
        """
        検索オブジェクトを生成します。

        Returns:
            ISearch: 検索オブジェクト
        """
        ...
    def IsFeatureEnabled(self, featureName: str) -> bool:
        """
        現在のエディションにおいて、指定したフィーチャが有効であるか調べます。

        Args:
            featureName (str): フィーチャ識別名

        Returns:
            bool: フィーチャが有効であるか
        """
        ...
    def GetFeatureValue(self, featureName: str, key: str) -> Any:
        """
        現在のエディションにおける、指定したフィーチャの指定したキー（属性）値を取得します。
        指定したフィーチャの有効/無効に関係なく値を取得します。

        Args:
            featureName (str): フィーチャ識別名
            key (str): フィーチャキー（属性）名

        Returns:
            Any: フィーチャ識別名、フィーチャキー名に対応した値
        """
        ...
    def CreateCommandParams(self) -> ICommandParams:
        """
        コマンドパラメータを作成します。

        Returns:
            ICommandParams: 作成したコマンドパラメータ
        """
        ...
    def ExecuteCommand(self, commandIdentifier: str, commandParams: ICommandParams) -> None:
        """
        指定された識別子のコマンドを実行します。
        これは、Extensionから別のExtensionを実行する際に使用します。

        Args:
            commandIdentifier (str): コマンド識別子
            commandParams (ICommandParams): コマンドパラメータ

        Returns:
            None: This method does not return a value.
        """
        ...
    def CreateScriptParams(self) -> IScriptParams:
        """
        スクリプトパラメータを作成します。

        Returns:
            IScriptParams: 作成したスクリプトパラメータ
        """
        ...
    def ExecuteScript(self, scriptPath: str, scriptParams: IScriptParams) -> Any:
        """
        指定したスクリプトファイルを読み込んで実行します。
        指定したスクリプトファイルの拡張子から、スクリプト言語を識別します。
        - \".cs\" または \".csx\" ：CSharpスクリプトとして実行します。
        - \".py\"  ：Pythonスクリプトとして実行します。
        V5.0では、上記以外の拡張子のファイルが指定された場合は、例外をスローします。

        Args:
            scriptPath (str): スクリプトファイルの絶対パス
            scriptParams (IScriptParams): スクリプトパラメータ

        Returns:
            Any: スクリプトの戻り値
        """
        ...
    @overload
    def ExecuteScriptCode(self, code: str, lang: str, scriptParams: IScriptParams) -> Any:
        """
        与えられたスクリプトコードを実行します。

        Args:
            code (str): スクリプトコード。
            lang (str): スクリプト言語。
- \"cs\"：C#
- \"py\"：Python
            scriptParams (IScriptParams): スクリプトパラメータ。

        Returns:
            Any: スクリプトの戻り値
        """
        ...
    @overload
    def ExecuteScriptCode(self, code: str, lang: str, basePath: str, scriptParams: IScriptParams) -> Any:
        """
        与えられたスクリプトコードを実行します。

        Args:
            code (str): スクリプトコード。
            lang (str): スクリプト言語。
- \"cs\"：C#
- \"py\"：Python
            basePath (str): 外部ファイルの探索起点のパス(nullの場合はプロジェクトファイルが格納されているフォルダ)。
            scriptParams (IScriptParams): スクリプトパラメータ。

        Returns:
            Any: スクリプトの戻り値
        """
        ...
    def Restart(self) -> bool:
        """
        アプリケーションを再起動します。

        """
        ...
    def Quit(self) -> None:
        """
        アプリケーションを終了します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ThrowUserException(self, message: str, type: str, showDialog: bool, caption: str, innerInfo: Any) -> None:
        """
        ユーザー例外をスローします。

        Args:
            message (str): 通知ダイアログに表示するメッセージ
            type (str): 通知ダイアログのアイコンの種別（Error | Warning | Information）
            showDialog (bool): 通知ダイアログを表示する場合は真
            caption (str): 通知ダイアログのタイトル
            innerInfo (Any): 例外を発生させた原因の情報

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Workspace(self) -> IWorkspace:
        """ワークスペース"""
        ...
    @property
    def Env(self) -> IEnv:
        """アプリケーション実行環境"""
        ...
    @property
    def Configuration(self) -> IConfiguration:
        """アプリケーション設定情報"""
        ...
    @property
    def Commands(self) -> ICommandManager:
        """コマンドマネージャ"""
        ...
    @property
    def Output(self) -> IOutput:
        """出力"""
        ...
    @property
    def Errors(self) -> IErrors:
        """エラー一覧"""
        ...
    @property
    def Search(self) -> ISearchManager:
        """検索"""
        ...
    @property
    def Window(self) -> IWorkspaceWindow:
        """UI操作オブジェクト"""
        ...
    @property
    def Extensions(self) -> IExtensions:
        """エクステンション管理"""
        ...
    @property
    def Util(self) -> IUtility:
        """汎用ユーティリティオブジェクト"""
        ...
    @property
    def FileUtil(self) -> IFileUtility:
        """ファイル操作ユーティリティオブジェクト"""
        ...
    @property
    def Resources(self) -> IResourceUtility:
        """リソース操作ユーティリティオブジェクト"""
        ...
    @property
    def Diff(self) -> IDiff:
        """差分抽出オブジェクト"""
        ...
    @property
    def CustomUI(self) -> ICustomUIRegistry:
        """カスタムUIレジストリ"""
        ...
    @property
    def DocumentGeneratorCustomization(self) -> Any:
        """ドキュメント生成のカスタマイズ
これは実験的な実装です。一般の開発者は使わないでください。"""
        ...
    @property
    def Version(self) -> str:
        """アプリケーションのバージョン番号"""
        ...
    @property
    def EditionId(self) -> str:
        """エディション識別名"""
        ...
    @property
    def EditionShortName(self) -> str:
        """エディション短縮名"""
        ...

class IConfiguration:
    """
    アプリケーション設定
    """
    ...

class IContextOption:
    """
    コンテキストオプション
    """
    @property
    def PlModelAccessMode(self) -> PlModelAccessMode:
        """コンテキストが有効な期間における、モデル情報の取得・検索APIの振る舞い"""
        ...
    @property
    def SpecifiedProduct(self) -> IProduct:
        """で指定の場合に参照するプロダクト"""
        ...
    @property
    def EditorAccessMode(self) -> EditorAccessMode:
        """コンテキストが有効な期間における、エディタ情報の取得・検索APIの振る舞い"""
        ...

class IEnv:
    """
    アプリケーション実行環境情報を提供します。
    """
    @property
    def Path(self) -> str:
        """アプリケーションの実行ファイルパス"""
        ...
    @property
    def AppName(self) -> str:
        """アプリケーション名"""
        ...
    @property
    def Version(self) -> str:
        """アプリケーションのバージョン"""
        ...
    @property
    def SchemaVersion(self) -> str:
        """アプリケーションのスキーマバージョン"""
        ...
    @property
    def Language(self) -> str:
        """アプリケーションの現在の言語（\"en-US\", \"ja-JP\"）"""
        ...
    @property
    def Locale(self) -> str:
        """アプリケーションの現在のロケール（\"en\", \"ja\"）"""
        ...
    @property
    def MachineId(self) -> str:
        """コンピュータを特定する識別子"""
        ...
    @property
    def ProcessId(self) -> str:
        """実行プロセスを特定する識別子"""
        ...

class IExtensionInfo:
    """
    エクステンション情報を提供します。
    """
    @property
    def Name(self) -> str:
        """名前（識別子）"""
        ...
    @property
    def DisplayName(self) -> str:
        """表示名"""
        ...
    @property
    def Description(self) -> str:
        """説明"""
        ...
    @property
    def ExtensionPath(self) -> str:
        """エクステンションの基点フォルダパス。
マニフェストファイルが格納されているフォルダの絶対パスを取得します。"""
        ...
    @property
    def Icon(self) -> str:
        """アイコン"""
        ...
    @property
    def Version(self) -> str:
        """バージョン"""
        ...
    @property
    def Publisher(self) -> str:
        """提供元"""
        ...
    @property
    def Commands(self) -> ICommandCollection:
        """このエクステンションで宣言したコマンド一覧"""
        ...

class IExtensionInfoCollection:
    """
    エクステンション情報一覧のコレクションです。
    """
    def GetItem(self, index: int) -> IExtensionInfo:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IExtensionInfo: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IExtensionInfoEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IExtensionInfoEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IExtensionInfo]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IExtensionInfoEnumerator:
    """
    エクステンション情報一覧のコレクションの列挙子です。
    """
    ...

class IExtensions:
    """
    エクステンション情報一覧を提供します。
    """
    def GetExtensionInfo(self, extensionIdentifier: str) -> IExtensionInfo:
        """
        指定された識別子のエクステンション情報を取得します

        Args:
            extensionIdentifier (str): エクステンション識別子

        Returns:
            IExtensionInfo: エクステンション情報
        """
        ...
    def ReloadAll(self, reloadManifest: bool) -> None:
        """
        すべてのエクステンションをリロードします。
        をtrueにするとマニフェストを再ロードして、リボンなどのUIも再構築します。
        がfalseの場合は、コード（ソースコード）、
        言語リソースなどのメモリ保持データをクリアして再ロードします。UIは更新しません。

        Args:
            reloadManifest (bool): マニフェストを再ロードするか。未指定の場合はtrue

        Returns:
            None: This method does not return a value.
        """
        ...
    def Reload(self, extensionIdentifier: str, reloadManifest: bool) -> None:
        """
        指定のエクステンションをリロードします。
        をtrueにするとマニフェストを再ロードして、リボンなどのUIも再構築します。
        がfalseの場合は、コード（ソースコード）、
        言語リソースなどのメモリ保持データをクリアして再ロードします。UIは更新しません。

        Args:
            extensionIdentifier (str): リロード対象のエクステンションの識別子
            reloadManifest (bool): マニフェストを再ロードするか。未指定の場合はtrue

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def AllExtensionInfos(self) -> IExtensionInfoCollection:
        """エクステンション情報一覧"""
        ...

class IHost:
    """
    ホスト変数
    """
    @property
    def Context(self) -> IContext:
        """実行コンテキスト"""
        ...
    @property
    def ExtensionInfo(self) -> IExtensionInfo:
        """エクステンション情報"""
        ...
    @property
    def Application(self) -> IApplication:
        """アプリケーション"""
        ...
    @property
    def App(self) -> IApplication:
        """アプリケーション"""
        ...
    @property
    def Version(self) -> str:
        """アプリケーションのバージョン番号"""
        ...
    @property
    def Commands(self) -> ICommandManager:
        """コマンドマネージャ"""
        ...
    @property
    def Extensions(self) -> IExtensions:
        """エクステンション管理"""
        ...
    @property
    def Workspace(self) -> IWorkspace:
        """ワークスペース"""
        ...
    @property
    def Output(self) -> IOutput:
        """出力"""
        ...
    @property
    def Errors(self) -> IErrors:
        """エラー一覧"""
        ...
    @property
    def Search(self) -> ISearchManager:
        """検索オブジェクト"""
        ...
    @property
    def CurrentProject(self) -> IProject:
        """カレントプロジェクト
ワークスペースで現在開いているカレントプロジェクト情報"""
        ...
    @property
    def CurrentProfile(self) -> IProfile:
        """カレントプロファイル
カレントプロジェクトのプロファイル情報"""
        ...
    @property
    def Metamodels(self) -> IMetamodels:
        """メタモデル管理
カレントプロファイルのメタモデル情報"""
        ...
    @property
    def ViewDefinitions(self) -> IViewDefinitions:
        """ビュー定義管理
カレントプロファイルのビュー定義情報"""
        ...
    @property
    def CurrentModel(self) -> IModel:
        """現在のプロジェクトで選択されているモデル要素"""
        ...
    @property
    def CurrentEditor(self) -> IEditor:
        """現在のエディタ"""
        ...
    @property
    def Window(self) -> IWorkspaceWindow:
        """ウィンドウ"""
        ...
    @property
    def UI(self) -> ICommonUI:
        """共通UIへのアクセス用インタフェース"""
        ...
    @property
    def EditorPage(self) -> IEditorPage:
        """エディタUI"""
        ...
    @property
    def CurrentEditorView(self) -> IEditorView:
        """現在のアクティブエディタ"""
        ...
    @property
    def CurrentNavigator(self) -> INavigator:
        """現在のアクティブナビゲータ"""
        ...
    @property
    def CurrentInfoView(self) -> IInfoView:
        """現在のアクティブな情報ビュー"""
        ...
    @property
    def Util(self) -> IUtility:
        """汎用ユーティリティオブジェクト"""
        ...
    @property
    def FileUtil(self) -> IFileUtility:
        """ファイル操作ユーティリティオブジェクト"""
        ...
    @property
    def Diff(self) -> IDiff:
        """差分抽出オブジェクト"""
        ...
    @property
    def Scm(self) -> IScmManager:
        """構成管理"""
        ...

class PlModelAccessMode(IntEnum):
    """
    プロダクトラインモデル情報アクセスモード
    """
    None = 0  # 設定なし（既定）。 上位スコープのコンテキストオプションに従います。
    AllProduct = 1  # 150%モデル。 すべてのモデル情報の取得・検索が可能です。
    CurrentProduct = 2  # カレントプロダクト。 アプリケーションで指定されたカレントプロダクトで有効なモデル情報のみ取得・検索が可能です。
    SpecifiedProduct = 3  # 指定プロダクト。 別途指定するプロダクトで有効なモデル情報のみ取得・検索が可能です。 プロダクトの指定は、IContextOption.SpecifiedProduct で実施します。

class SubEditorMode(IntEnum):
    """
    サブエディタの表示方法(追従戦略)の種別
    """
    Manual = 0  # 手動
    Detail = 1  # 詳細
    Input = 2  # 入力
    Output = 3  # 出力
    SameAsMain = 4  # メインと同じ
    Custom = 5  # カスタム

class IScriptParams:
    """
    スクリプトパラメータを表します。
    """
    def ToArray(self) -> List[Any]:
        """
        パラメータの内容をオブジェクト配列に変換します。

        Returns:
            List[Any]: オブジェクト配列
        """
        ...
    def AddParam(self, value: Any) -> None:
        """
        パラメータに値を追加します。

        Args:
            value (Any): 追加対象

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddParamWithName(self, name: str, value: Any) -> None:
        """
        パラメータに値を追加します。

        Args:
            name (str): 名前
            value (Any): 追加対象

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetByIndex(self, index: int) -> Any:
        """
        指定パラメータの値をインデックスで取得します

        Args:
            index (int): インデックス

        Returns:
            Any: 指定パラメータの値
        """
        ...
    def GetByName(self, name: str) -> Any:
        """
        指定パラメータの値をパラメータ名で取得します

        Args:
            name (str): パラメータ名

        Returns:
            Any: 指定パラメータの値
        """
        ...
    def ToCollection(self) -> Any:
        """
        パラメータの内容をオブジェクトコレクションに変換します。

        Returns:
            Any: オブジェクトコレクション
        """
        ...
    @overload
    def __getitem__(self, index: int) -> Any: ...
    @overload
    def __getitem__(self, name: str) -> Any: ...

class ICustomUIRegistry:
    """
    カスタムUI管理へのアクセスオブジェクトを表します。
    """
    def RegisterCustomNavigator(self, extensionName: str, descriptor: Any) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RegisterCustomEditor(self, extensionName: str, descriptor: Any) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RegisterCustomInspector(self, extensionName: str, descriptor: Any) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RegisterCustomFinder(self, extensionName: str, descriptor: Any) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRegisterAllCustomUIs(self, extensionName: str) -> None:
        """
        全てのカスタムUIの登録を解除します。

        Args:
            extensionName (str): エクステンション名

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRegisterCustomNavigator(self) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRegisterCustomEditor(self) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRegisterCustomInspector(self) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRegisterCustomFinder(self) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...

class IInfoDisplayStyle:
    """
    エラー情報、検索結果情報の表示スタイルを表します。
    """
    def SetStyleSets(self, viewName: str, styleValues: Dict[str, str]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Name(self) -> str:
        """スタイル名"""
        ...
    @property
    def CardDisplayStyle(self) -> str:
        """カードの表示スタイル
\"None\"：カードを表示しない
\"TitleOnly\"：タイトルのみのカード
\"DetailOnly\"：詳細のみのカード
\"All\"：タイトルと詳細のあるカード（詳細がなければタイトルのみ）
未指定の場合は”All”とする"""
        ...

class IInfoDisplayStyleSet:
    """
    スタイルセット
    """
    def CreateStyle(self, name: str) -> IInfoDisplayStyle:
        """
        指定された名前のスタイルを作成します。該当する名前のスタイルが既に存在する場合は、そのスタイルを返します。

        Args:
            name (str): スタイル名

        Returns:
            IInfoDisplayStyle: 表示スタイル
        """
        ...
    def GetStyle(self, name: str) -> IInfoDisplayStyle:
        """
        指定された名前のスタイルの取得します。

        Args:
            name (str): スタイル名

        Returns:
            IInfoDisplayStyle: 表示スタイル
        """
        ...
    def ClearStyle(self, name: str) -> None:
        """
        指定スタイルのクリアします。

        Args:
            name (str): スタイル名

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearAllStyles(self) -> None:
        """
        全スタイルのクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Styles(self) -> Iterable[IInfoDisplayStyle]:
        """スタイル一覧"""
        ...

class IModelEventDispatcher:
    """
    モデルイベントディスパッチャ
    モデルのプロパティ変更通知を受信するメカニズムを提供します。
    """
    def RegisterPropertyChangedEventHandler(self, observer: Any, modelId: str, handler: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearEventHandler(self, observer: Any) -> None:
        """
        指定されたオブザーバで登録された全てのイベントハンドラの登録を解除します

        Args:
            observer (Any): オブザーバ

        Returns:
            None: This method does not return a value.
        """
        ...

class IOutput:
    """
    出力を表します。
    """
    def WriteLine(self, category: str, message: str) -> None:
        """
        出力の指定されたカテゴリに文字列を追加します。

        Args:
            category (str): カテゴリ
            message (str): 文字列

        Returns:
            None: This method does not return a value.
        """
        ...
    def WriteFormatLine(self, category: str, format: str, *parameter: List[List[Any]]) -> None:
        """
        出力の指定されたカテゴリに指定のフォーマットで文字列を追加します。
        なお、フォーマット文字列の置換についてはC#のString.Formatに準拠します。

        Args:
            category (str): カテゴリ
            format (str): フォーマット
            parameter (List[Any]): 置換オブジェクト

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearAll(self) -> None:
        """
        すべての出力をクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Clear(self, category: str) -> None:
        """
        出力の指定されたカテゴリをクリアします。

        Args:
            category (str): カテゴリ

        Returns:
            None: This method does not return a value.
        """
        ...

class IEditPermissionResult:
    """
    編集権限の取得/解放を要求した際の結果情報です。
    """
    @property
    def Operation(self) -> str:
        """要求内容"""
        ...
    @property
    def SuccessUnits(self) -> IModelUnitCollection:
        """編集権限操作に成功したユニット一覧"""
        ...
    @property
    def FailUnits(self) -> IModelUnitCollection:
        """編集権限操作に失敗したユニット一覧"""
        ...
    @property
    def EditableUnits(self) -> IModelUnitCollection:
        """編集権限が取得できているユニット一覧"""
        ...
    @property
    def UneditableUnits(self) -> IModelUnitCollection:
        """編集権限が取得できていないユニット一覧"""
        ...

class IScmChangePath:
    """
    リビジョンでの変更対象要素情報を表します。
    """
    @property
    def Path(self) -> str: ...
    @property
    def Action(self) -> str: ...

class IScmChangePathCollection:
    """
    リビジョンでの変更対象要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> IScmChangePath:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IScmChangePath: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IScmChangePathEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IScmChangePathEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IScmChangePath]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IScmChangePathEnumerator:
    """
    リビジョンでの変更対象要素情報の列挙子です。
    """
    ...

class IScmManager:
    """
    構成管理マネージャ
    ※SCMリポジトリ操作は将来のバージョンで拡張
    """
    def IsScmItem(self, project: IProject) -> bool:
        """
        指定されたプロジェクトが構成管理システムと連携済みであるか

        Args:
            project (IProject): プロジェクト

        Returns:
            bool: 連携済みの場合は真
        """
        ...
    def IsScmFolder(self, path: str) -> bool:
        """
        指定されたパスが構成管理システムの作業フォルダであるか

        Args:
            path (str): パス

        Returns:
            bool: 構成管理システムの作業フォルダの場合は真
        """
        ...
    def GetRepositorySettings(self) -> IScmRepositorySettingCollection:
        """
        定義済みのすべての構成管理接続設定を取得します

        Returns:
            IScmRepositorySettingCollection: 構成管理接続設定の列挙
        """
        ...
    @overload
    def GetRepositorySetting(self, project: IProject) -> IScmRepositorySetting:
        """
        指定されたプロジェクトに対応する構成管理接続設定を取得します

        Args:
            project (IProject): プロジェクト

        Returns:
            IScmRepositorySetting: 構成管理接続設定
        """
        ...
    @overload
    def GetRepositorySetting(self, name: str) -> IScmRepositorySetting:
        """
        指定された名前の構成管理接続設定を取得します

        Args:
            name (str): 名前

        Returns:
            IScmRepositorySetting: 構成管理接続設定
        """
        ...
    def CreateScmRepositorySetting(self, type: str, name: str, account: str, password: str, url: str, isManaged: bool) -> IScmRepositorySetting:
        """
        指定された接続情報で新しい構成管理接続設定を生成します。

        Args:
            type (str): リポジトリの種類
            name (str): リポジトリ名
            account (str): 接続アカウント名
            password (str): 接続パスワード
            url (str): 接続先URL
            isManaged (bool): Indioの管理対象として登録するか

        Returns:
            IScmRepositorySetting: 構成管理接続設定
        """
        ...
    def GetRemotePath(self, project: IProject, unit: IModelUnit) -> str:
        """
        指定されたプロジェクトで指定されたユニットのリモートパス（リポジトリのパス）を取得します

        Args:
            project (IProject): プロジェクト
            unit (IModelUnit): ユニット

        Returns:
            str: リモートパス（リポジトリのパス）
        """
        ...
    def GetChangedUnits(self, project: IProject) -> IModelUnitCollection:
        """
        指定されたプロジェクトにおいて変更のあったユニットを取得します。
        指定されたプロジェクトが構成管理システムと未連携の場合は空のコレクションを返します。

        Args:
            project (IProject): プロジェクト

        Returns:
            IModelUnitCollection: 変更のあったユニットの一覧
        """
        ...
    def ShareProject(self, project: IProject, setting: IScmRepositorySetting, comment: str, remotePath: str, silent: bool) -> None:
        """
        指定されたプロジェクトを指定された構成管理リポジトリで共有します。

        Args:
            project (IProject): 共有するプロジェクト
            setting (IScmRepositorySetting): 構成管理接続設定（SCM連携済みのフォルダ配下にあるプロジェクトを登録する場合は指定不要）
            comment (str): 初回コミットコメント（SCM連携済みのフォルダ配下にあるプロジェクトを登録する場合は指定不要）
            remotePath (str): リモートパス（nullを指定した場合は、構成管理接続設定のBaseUrlに追加する）
            silent (bool): trueを指定した場合、進捗状況をプログレスバーで表示しません

        Returns:
            None: This method does not return a value.
        """
        ...
    def CheckoutProject(self, projectPath: str, workDir: str, setting: IScmRepositorySetting, autoLoad: bool, silent: bool) -> IProject:
        """
        指定されたプロジェクトパス（リモートリポジトリのパス）のプロジェクトを指定された作業領域にチェックアウトします。

        Args:
            projectPath (str): プロジェクトパス（リモートリポジトリのパス）
            workDir (str): ローカルの作業領域（チェックアウト先）フォルダパス
            setting (IScmRepositorySetting): 構成管理接続設定
            autoLoad (bool): チェックアウト後に自動的にプロジェクトを読み込み、カレントプロジェクトとして設定するか
- trueが指定されている場合、現在のカレントプロジェクトは編集状態を破棄して強制的に閉じられます（既定の動作）
- falseが指定されている場合は、プロジェクトのチェックアウトのみが行われ、プロジェクトは読み込まれません
            silent (bool): trueを指定した場合、進捗状況をプログレスバーで表示しません

        Returns:
            IProject: チェックアウトしたプロジェクト。autoLoadに偽を指定した場合はnullとなります。
        """
        ...
    def UpdateProject(self, project: IProject, units: Iterable[IModelUnit], autoReload: bool, silent: bool) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def CommitProject(self, project: IProject, comment: str, keepLocks: bool, silent: bool) -> None:
        """
        指定されたプロジェクトの変更を確定し、構成管理リポジトリにコミットします。
        指定されたプロジェクトに変更がない場合は何も行われません。
        また、指定されたプロジェクトが構成管理システムと未連携の場合も何も行われません。

        Args:
            project (IProject): プロジェクト
            comment (str): コメント
            keepLocks (bool): ロック状態を維持するか
            silent (bool): trueを指定した場合、進捗状況をプログレスバーで表示しません

        Returns:
            None: This method does not return a value.
        """
        ...
    def CommitUnits(self, project: IProject, units: Iterable[IModelUnit], comment: str, keepLocks: bool, silent: bool) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RevertProject(self, project: IProject, autoReload: bool, silent: bool) -> None:
        """
        指定されたプロジェクトの全てのユニットの変更を破棄します。
        指定されたプロジェクトに変更がない場合は何も行われません。
        また、指定されたプロジェクトが構成管理システムと未連携の場合も何も行われません。

        Args:
            project (IProject): プロジェクト
            autoReload (bool): 更新後に自動的にプロジェクトを読み込み直すか
            silent (bool): trueを指定した場合、進捗状況をプログレスバーで表示しません

        Returns:
            None: This method does not return a value.
        """
        ...
    def RevertUnits(self, project: IProject, units: Iterable[IModelUnit], autoReload: bool, silent: bool) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def GetAllEditPermissions(self, project: IProject) -> IEditPermissionResult:
        """
        指定されたプロジェクトの全てのユニットの編集権限を取得します。
        プロファイルをユニット化している場合は、プロファイルのユニットも対象となります。
        指定されたプロジェクトが構成管理システムと未連携の場合は何も行われません。

        Args:
            project (IProject): プロジェクト

        Returns:
            IEditPermissionResult: 権限取得結果オブジェクト
        """
        ...
    def GetEditPermission(self, project: IProject, unit: IModelUnit) -> IEditPermissionResult:
        """
        指定されたプロジェクトで指定されたユニットの編集権限を取得します。
        指定されたプロジェクトが構成管理システムと未連携の場合は何も行われません。

        Args:
            project (IProject): プロジェクト
            unit (IModelUnit): 権限を取得しますユニット

        Returns:
            IEditPermissionResult: 権限取得結果オブジェクト
        """
        ...
    def GetEditPermissions(self, project: IProject, units: Iterable[IModelUnit]) -> IEditPermissionResult: ...
    def ReleaseAllEditPermissions(self, project: IProject) -> IEditPermissionResult:
        """
        指定されたプロジェクトの全てのユニットの編集権限を解放します。
        プロファイルをユニット化している場合は、プロファイルのユニットも対象となります。
        指定されたプロジェクトが構成管理システムと未連携の場合は何も行われません。

        Args:
            project (IProject): プロジェクト

        Returns:
            IEditPermissionResult: 権限解放結果オブジェクト
        """
        ...
    def ReleaseEditPermission(self, project: IProject, unit: IModelUnit) -> IEditPermissionResult:
        """
        指定されたプロジェクトで指定されたユニットの編集権限を解放します。
        指定されたプロジェクトが構成管理システムと未連携の場合は何も行われません。

        Args:
            project (IProject): プロジェクト
            unit (IModelUnit): 権限を解放するユニット

        Returns:
            IEditPermissionResult: 権限解放結果オブジェクト
        """
        ...
    def ReleaseEditPermissions(self, project: IProject, units: Iterable[IModelUnit]) -> IEditPermissionResult: ...

class IScmRepositorySetting:
    """
    「リポジトリの管理」により登録したリポジトリ接続情報です。
    """
    @property
    def Name(self) -> str:
        """リポジトリ設定名"""
        ...
    @property
    def RepositoryType(self) -> str:
        """リポジトリの種類"""
        ...
    @property
    def BaseUrl(self) -> str:
        """接続URL"""
        ...

class IScmRepositorySettingCollection:
    """
    リポジトリ接続情報のコレクションです。
    """
    def GetItem(self, index: int) -> IScmRepositorySetting:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IScmRepositorySetting: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IScmRepositorySettingEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IScmRepositorySettingEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IScmRepositorySetting]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IScmRepositorySettingEnumerator:
    """
    リポジトリ接続情報の列挙子です。
    """
    ...

class IScmRevision:
    """
    リビジョン情報を表します。
    """
    @property
    def Revision(self) -> str:
        """リビジョン"""
        ...
    @property
    def Actions(self) -> str:
        """変更アクション。
全ての変更対象要素のアクションのサマリです。"""
        ...
    @property
    def Author(self) -> str:
        """更新者"""
        ...
    @property
    def Date(self) -> str:
        """更新日時"""
        ...
    @property
    def Message(self) -> str:
        """メッセージ"""
        ...
    @property
    def ChangePaths(self) -> IScmChangePathCollection:
        """変更対象要素"""
        ...

class ITraceCoverageExcludedModel:
    """
    トレース除外対象モデル情報です。
    """
    def Delete(self) -> None:
        """
        このトレース除外対象のモデル情報を削除します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def ModelId(self) -> str:
        """除外対象のモデルの識別子"""
        ...
    @property
    def Model(self) -> IModel:
        """除外対象のモデル
該当モデルが削除済みの場合は、null を返します。
また、該当モデルがプロキシ化されている場合は、モデルのプロキシ情報を返します。。"""
        ...
    @property
    def Direction(self) -> str:
        """トレースの除外方向
- \"Source\" : 導出元への関連を除外します
- \"Target\" : 導出先への関連を除外します
- \"Both\"   : 導出元、および導出先への関連を除外します"""
        ...
    @property
    def Reason(self) -> str:
        """除外理由"""
        ...

class ITraceCoverageExcludedModelCollection:
    """
    トレース除外対象モデル情報一覧のコレクションです。
    """
    def GetItem(self, index: int) -> ITraceCoverageExcludedModel:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITraceCoverageExcludedModel: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITraceCoverageExcludedModelEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITraceCoverageExcludedModelEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITraceCoverageExcludedModel]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITraceCoverageExcludedModelEnumerator:
    """
    トレース除外対象モデル情報一覧のコレクションの列挙子です。
    """
    ...

class ITraceLane:
    """
    トレース対象のルートオブジェクトを管理する
    レーン（系列）情報へのアクセスインタフェースです。
    """
    def FindNode(self, model: IModel) -> ITraceNode:
        """
        このレーン内の指定されたモデルに対応するノードを検索します。
        モデルフィルタや関連フィルタが適用されている場合、フィルタが適用された状態で検索します。
        該当するノードがレーン内で見つからない場合は null を返します。

        Args:
            model (IModel): 検索結果のモデル。

        Returns:
            ITraceNode: 指定されたモデルに対応するノード。
        """
        ...
    @property
    def ModelId(self) -> str:
        """このレーンの基点に指定しているモデルの識別子"""
        ...
    @property
    def RootModel(self) -> IModel:
        """このレーンの基点モデル
ModelIdで指定されているモデルが見つからない場合は　null を返します。"""
        ...
    @property
    def RootNode(self) -> ITraceNode:
        """このレーンの基点ノード
ModelIdで指定されているモデルが見つからない場合は　null を返します。"""
        ...

class ITraceLaneCollection:
    """
    このノードが含まれるレーン（系列）情報のコレクションです。
    """
    def GetItem(self, index: int) -> ITraceLane:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITraceLane: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITraceLaneEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITraceLaneEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITraceLane]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITraceLaneEnumerator:
    """
    このノードが含まれるレーン（系列）情報のコレクションの列挙子です。
    """
    ...

class ITraceNode:
    """
    トレース対象のモデルに対応するノード情報へのアクセスインタフェースです。
    """
    @property
    def Model(self) -> IModel:
        """トレース対象のモデル"""
        ...
    @property
    def Parent(self) -> ITraceNode:
        """このノードのツリー階層上の親ノード"""
        ...
    @property
    def TraceLane(self) -> ITraceLane:
        """このノードが含まれるレーン（系列）情報"""
        ...
    @property
    def Children(self) -> ITraceNodeCollection:
        """このノードのツリー階層上の子ノードのコレクションを取得します。
モデルフィルタや関連フィルタが適用されている場合、フィルタが適用された状態で返します。"""
        ...
    @property
    def SourceNodes(self) -> ITraceNodeCollection:
        """トレース対象のモデルの導出元(関連先)要素が対応するトレース元レーンのノードのコレクションを取得します。
モデルフィルタや関連フィルタが適用されている場合、フィルタが適用された状態で返します。"""
        ...
    @property
    def TargetNodes(self) -> ITraceNodeCollection:
        """トレース対象のモデルの導出先(関連元)要素が対応するトレース先レーンのノードのコレクションを取得します。
モデルフィルタや関連フィルタが適用されている場合、フィルタが適用された状態で返します。"""
        ...
    @property
    def ExcludedDirection(self) -> str:
        """トレース対象のモデルに設定されたトレース除外の方向
- \"Source\" : 導出元への関連を除外します
- \"Target\" : 導出先への関連を除外します
- \"Both\"   : 導出元、および導出先への関連を除外します
- \"None\"   : 除外しません"""
        ...
    @property
    def Expanded(self) -> bool:
        """トレースビューにおけるツリーの展開状態。
ツリーが展開されている場合は、true を返します。
未展開のノードに対して、展開状態を true に設定した場合、すべての親ノードの展開状態を true に設定します。"""
        ...
    @property
    def IsSelected(self) -> bool:
        """このノードの選択状態"""
        ...

class ITraceNodeCollection:
    """
    トレース対象のモデルに対応するノード情報へのアクセスインタフェースのコレクションです。
    """
    def GetItem(self, index: int) -> ITraceNode:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITraceNode: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITraceNodeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        """
        ...
    def __iter__(self) -> Iterator[ITraceNode]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITraceNodeEnumerator:
    """
    トレース対象のモデルに対応するノード情報へのアクセスインタフェースのコレクションの列挙子です。
    """
    ...

class ITraceView:
    """
    トレースビュー情報へのアクセス用インターフェースです。
    """
    @property
    def Name(self) -> str:
        """ビュー名"""
        ...
    @property
    def Id(self) -> str:
        """識別子"""
        ...
    @property
    def TraceLanes(self) -> ITraceLaneCollection:
        """トレースビューに表示する系列（個別のツリー情報）のコレクション
ビューでのツリー表示順序でコレクションに格納されます。
なお、ビューの種類が Matrix の場合は、要素の1つ目が行、2つ目が列に対応し、それ以外の系列は使用されません。"""
        ...

class ITraceViewCollection:
    """
    トレースビュー情報へのアクセスインタフェースのコレクションです。
    """
    def GetItem(self, index: int) -> ITraceView:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITraceView: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITraceViewEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        """
        ...
    def __iter__(self) -> Iterator[ITraceView]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITraceViewEnumerator:
    """
    トレースビュー情報へのアクセスインタフェースのコレクションの列挙子です。
    """
    ...

class TraceViewType(IntEnum):
    """
    トレースビューの種類
    """
    Tree = 0  # ツリー形式のビュー
    Matrix = 1  # マトリックス形式のビュー

class IUIElement:
    """
    UI要素を表します。
    """
    ...

class ICommonUI(IUIElement):
    """
    共通UIへのアクセス用インタフェースです。
    """
    def ShowConfirmDialog(self, message: str, caption: str) -> bool:
        """
        確認ダイアログを表示します。

        Args:
            message (str): メッセージ
            caption (str): キャプション

        Returns:
            bool: ダイアログの操作結果(OK=true / Cancel=false)
        """
        ...
    def ShowInformationDialog(self, message: str, caption: str) -> None:
        """
        通知ダイアログを表示します。

        Args:
            message (str): メッセージ
            caption (str): キャプション

        Returns:
            None: This method does not return a value.
        """
        ...
    def MessageBox(self, message: str, caption: str) -> None:
        """
        メッセージを表示します。

        Args:
            message (str): メッセージ
            caption (str): キャプション(省略した場合はアプリケーション名を使用します)

        Returns:
            None: This method does not return a value.
        """
        ...
    def ShowMessageBox(self, message: str, caption: str) -> None:
        """
        メッセージを表示します。

        Args:
            message (str): メッセージ
            caption (str): キャプション

        Returns:
            None: This method does not return a value.
        """
        ...
    def ShowOpenFileDialog(self, title: str, filter: str) -> str:
        """
        ファイルを開くダイアログを表示します。

        Args:
            title (str): ダイアログのタイトル
            filter (str): ファイルを選択する際のフィルタ

        Returns:
            str: ダイアログで選択したファイルのパス
        """
        ...
    def ShowSaveFileDialog(self, title: str, filter: str, initialPath: str) -> str:
        """
        保存ダイアログを表示します。

        Args:
            title (str): ダイアログのタイトル
            filter (str): 保存先を選択する際のフィルタ
            initialPath (str): 保存するファイル名

        Returns:
            str: 保存するファイルのパス
        """
        ...
    def ShowSelectFolderDialog(self, title: str, initialPath: str) -> str:
        """
        フォルダを開くダイアログを表示して、ダイアログで選択したフォルダのパスを取得します。
        ダイアログがキャンセルされた場合はnullを返します。

        Args:
            title (str): ダイアログのタイトル
            initialPath (str): 初期選択するフォルダパス

        """
        ...
    def ShowRevisions(self, unit: IModelUnit) -> None:
        """
        カレントプロジェクトの指定されたモデルファイルのリビジョン一覧を表示します。
        モデルファイルが未指定の場合は、カレントプロジェクトのリビジョン一覧を表示します。
        指定されたモデルファイルがカレントプロジェクトの管理下でない、または、
        カレントプロジェクトがSCM連携していない場合は何も行いません。

        Args:
            unit (IModelUnit): ユニット

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectRevision(self, unit: IModelUnit) -> IScmRevision:
        """
        Args:
            unit (IModelUnit): ユニット

        """
        ...

class IEditorPage(IUIElement):
    """
    エディタUIへのアクセス用インターフェースです。
    """
    def IsMainEditor(self, editorView: Any) -> bool:
        """
        指定したカスタムエディタがアクティブタブのメインエディタに表示されているか否かを判定します。

        Args:
            editorView (Any): カスタムエディタ。

        Returns:
            bool: アクティブタブのメインエディタに表示されている場合はtrueを返します。
        """
        ...
    def IsSubEditor(self, editorView: Any) -> bool:
        """
        指定したカスタムエディタがアクティブタブのサブエディタに表示されているか否かを判定します。

        Args:
            editorView (Any): カスタムエディタ。

        Returns:
            bool: アクティブタブのサブエディタに表示されている場合はtrueを返します。
        """
        ...
    @overload
    def SetSubEditorMode(self, subEditorMode: SubEditorMode, displayModel: IModel) -> None:
        """
        アクティブタブのサブエディタの追従戦略を指定します。
        subEditorModeにのManualを指定した場合のみ、displayModelを表示対象モデルとします。
        それ以外の追従戦略指定時はdisplayModelの指定を無視します。
        Manualを指定してdisplayModelが無指定の場合はプロジェクト（Root）を表示対象モデルとします。

        Args:
            subEditorMode (SubEditorMode): サブエディタの表示方法(追従戦略)の種別。
            displayModel (IModel): subEditorModeでManualを指定した場合の表示対象モデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetSubEditorMode(self, subEditorMode: str, displayModel: IModel) -> None:
        """
        アクティブタブのサブエディタの追従戦略を指定します。
        subEditorModeにManualを指定した場合のみ、displayModelを表示対象モデルとします。
        それ以外の追従戦略指定時はdisplayModelの指定を無視します。
        Manualを指定してdisplayModelが無指定の場合はプロジェクト（Root）を表示対象モデルとします。

        Args:
            subEditorMode (str): （Manual | Detail | Input | Output | SameAsMain | Custom.{Id}）
            displayModel (IModel): subEditorModeでManualを指定した場合の表示対象モデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UpdateEditors(self) -> None:
        """
        このエディタページを最新に更新します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def OpenModelInNewTab(self, model: IModel) -> None:
        """
        指定されたモデルを新しいタブで表示します。

        Args:
            model (IModel): 新しいタブで表示するモデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def IsNavigatorPaneVisible(self) -> bool:
        """ナビゲータペイン表示状態を取得または設定します。"""
        ...
    @property
    def IsInformationPaneVisible(self) -> bool:
        """情報ペイン表示状態を取得または設定します。"""
        ...
    @property
    def IsSubEditorVisible(self) -> bool:
        """アクティブタブのサブエディタ表示状態を取得または設定します。"""
        ...
    @property
    def IsInspectorPaneVisible(self) -> bool:
        """インスペクタペイン表示状態を取得または設定します。"""
        ...
    @property
    def IsAgentiqsPaneVisible(self) -> bool:
        """Agentiqsペイン表示状態を取得または設定します。"""
        ...
    @property
    def ActiveInfoWindow(self) -> str:
        """情報ペインのアクティブページを取得または設定します。
（Output | Error | SearchResult）"""
        ...
    @property
    def ActiveNavigator(self) -> str:
        """ナビゲータペインのアクティブなナビゲータを取得または設定します。
（Model | ProductLine | Scm | Project | Profile）"""
        ...
    @property
    def ActivePalette(self) -> str:
        """パレットペインのアクティブなパレットを取得または設定します。
（Editor | Reference | Derive | Feature | ProductSelector | Class）"""
        ...
    @property
    def ActiveInspector(self) -> str:
        """インスペクタペインのアクティブなインスペクタを取得または設定します。"""
        ...
    @property
    def CurrentOutputCategory(self) -> str:
        """情報ペインのOutputのカレントカテゴリを取得または設定します。"""
        ...
    @property
    def IsErrorCardVisible(self) -> bool:
        """エラーカード表示状態を取得または設定します。"""
        ...
    @property
    def IsTraceLineVisible(self) -> bool:
        """エディタ間トレース表示状態を取得または設定します。"""
        ...
    @property
    def IsIndicatorVisible(self) -> bool:
        """インジケータ表示状態を取得または設定します。"""
        ...
    @property
    def IsDiffViewVisible(self) -> bool:
        """差分ビューの表示状態を取得または設定します。"""
        ...
    @property
    def IsDiffHighlightVisible(self) -> bool:
        """変更差分比較モードを取得または設定します。"""
        ...
    @property
    def IsFeatureMarkVisible(self) -> bool:
        """フィーチャーマーク表示状態を取得または設定します。"""
        ...
    @property
    def CurrentModel(self) -> IModel:
        """現在（モデルナビゲータで）選択されているモデルを取得します。"""
        ...
    @property
    def CurrentEditorView(self) -> IEditorView:
        """アクティブタブの現在のアクティブエディタを取得します。"""
        ...
    @property
    def MainEditorView(self) -> IEditorView:
        """アクティブタブの現在のメインエディタを取得します。"""
        ...
    @property
    def SubEditorView(self) -> IEditorView:
        """アクティブタブの現在のサブエディタを取得します。"""
        ...
    @property
    def CurrentNavigator(self) -> INavigator:
        """現在のアクティブナビゲータを取得します。"""
        ...
    @property
    def CurrentInfoView(self) -> IInfoView:
        """現在のアクティブな情報ビューを取得します。"""
        ...
    @property
    def SubEditorMode(self) -> SubEditorMode:
        """アクティブタブのサブエディタの表示方法(追従戦略)の種別を取得します。"""
        ...
    @property
    def SubEditorModeName(self) -> str:
        """アクティブタブのサブエディタの表示方法名を取得します。"""
        ...

class IEditorView(IUIElement):
    """
    メイン・サブエディタUIの共通インターフェースです。
    """
    def SelectViewDefinition(self, viewDefinition: IEditorDef) -> None:
        """
        エディタで表示するビューを切り替えます。
        表示できないビュー定義が指定された場合は、何も行いません。

        Args:
            viewDefinition (IEditorDef): ビュー定義

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectModel(self, model: IModel) -> bool:
        """
        エディタ内で指定されたモデルを選択します。
        モデルがエディタ上に表示されていない場合は何も行いません。

        Args:
            model (IModel): 選択するモデル。

        Returns:
            bool: 要素を選択した場合はtrue、モデルがエディタ上に表示されていない場合はfalseを返します。
        """
        ...
    def GetImage(self) -> Any:
        """
        エディタで表示するビューのビットマップイメージを取得します。
        イメージが取得できなかった場合は null を返します。

        Returns:
            Any: ビットマップイメージ。
        """
        ...
    def SaveImage(self, filePath: str) -> None:
        """
        指定したパスにエディタで表示するビューのビットマップイメージを保存します。
        指定されたファイルパスに既にファイルが存在する場合は、そのファイルを上書きします。
        サポートする保存形式は、PNG、JPEG、GIF、BMP、XPSです。
        どの形式で保存するかは、指定された保存先のファイルパスの拡張子から判断します。
        拡張子から判断できない場合はPNG形式とし、指定されたファイルパスの末尾に\".png\"を付与したファイルパスに保存します。

        Args:
            filePath (str): 保存先のファイルパス。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Editor(self) -> IEditor:
        """エディタ"""
        ...
    @property
    def ViewDefinitions(self) -> IEditorDefCollection:
        """このエディタで選択できるビュー定義の一覧"""
        ...
    @property
    def SelectedModels(self) -> IModelCollection:
        """エディタで選択されているモデル"""
        ...
    @property
    def DiffEditor(self) -> IEditor:
        """差分エディタ"""
        ...
    @property
    def HasDiffEditor(self) -> bool:
        """このエディタビューで差分エディタを保持しているか"""
        ...

class IFinder(IUIElement):
    """
    ファインダUIへのアクセス用インターフェースです。
    """
    def ShowFinder(self, model: IModel, fieldName: str, keyword: str, parentWindow: Any) -> IModelCollection:
        """
        ファインダを表示して選択されたモデルを取得します

        Args:
            model (IModel): 関連付け対象モデル
            fieldName (str): 関連付けるフィールド
            keyword (str): キーワード
            parentWindow (Any): 親ウィンドウ（省略時は、カレントウィンドウ）

        """
        ...

class IInfoView(IUIElement):
    """
    情報ビューUIへのアクセス用インターフェースです。
    """
    def Select(self, item: Any, append: bool) -> None:
        """
        この情報ビューで指定された要素を選択します。

        Args:
            item (Any): 選択する要素
            append (bool): 追加選択するか

        Returns:
            None: This method does not return a value.
        """
        ...
    def ScrollToBottom(self) -> None:
        """
        スクロールバーを末尾までスクロールします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Name(self) -> str:
        """情報ビューの種類
\"Error\" : エラー一覧
\"SearchResult\" : 検索結果一覧
\"Output\" : 出力"""
        ...
    @property
    def Title(self) -> str:
        """情報ビューのタイトル
\"エラー\" | \"検索結果\" | \"出力\""""
        ...
    @property
    def Items(self) -> IInfoEntryCollection:
        """情報ビューの表示内容"""
        ...
    @property
    def SelectedItems(self) -> IInfoEntryCollection:
        """情報ビューの選択要素"""
        ...
    @property
    def IsVisible(self) -> bool:
        """この情報ビューが表示されているか"""
        ...

class INavigator(IUIElement):
    """
    ナビゲータ
    """
    def Select(self, item: Any, append: bool) -> None:
        """
        このナビゲータで指定された要素を選択します。

        Args:
            item (Any): 選択する要素
            append (bool): 追加選択するか

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Name(self) -> str:
        """ナビゲータの種類"""
        ...
    @property
    def Title(self) -> str:
        """ナビゲータタイトル"""
        ...
    @property
    def BaseType(self) -> str:
        """ナビゲータ形態"""
        ...
    @property
    def Items(self) -> Any:
        """このナビゲータの全ての管理要素"""
        ...
    @property
    def SelectedItems(self) -> Any:
        """ナビゲータで選択されている要素"""
        ...
    @property
    def IsValid(self) -> bool:
        """現在このナビゲータが有効であるか"""
        ...
    @property
    def IsVisible(self) -> bool:
        """現在このナビゲータが表示されているか"""
        ...
    @property
    def MultiSelection(self) -> bool:
        """複数要素を選択可能とできるか"""
        ...

class INavigatorCollection:
    """
    ツリー構造情報のコレクションです。
    """
    def GetItem(self, index: int) -> INavigator:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            INavigator: コレクション要素
        """
        ...
    def GetEnumerator(self) -> INavigatorEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            INavigatorEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[INavigator]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class INavigatorEnumerator:
    """
    ツリー構造情報のコレクションの列挙子です。
    """
    ...

class IStatusbar(IUIElement):
    """
    ステータスバー
    """
    @property
    def Message(self) -> str:
        """メッセージ"""
        ...

class ITracePage(IUIElement):
    """
    トレースUIへのアクセス用インターフェースです。
    """
    def AddTraceView(self, name: str, laneRootModels: Iterable[IModel]) -> ITraceView: ...
    def AddExcludedModel(self, modelId: str, direction: str, reason: str) -> ITraceCoverageExcludedModel:
        """
        新しいトレース除外対象のモデル情報を追加します。
        このメソッドでは、指定された識別子のモデルの存在を確認しません。

        Args:
            modelId (str): モデル識別子
            direction (str): トレースの除外方向
            reason (str): 除外理由

        """
        ...
    def DeleteExcludedModel(self, model: ITraceCoverageExcludedModel) -> None:
        """
        指定されたトレース除外対象のモデル情報を削除します。

        Args:
            model (ITraceCoverageExcludedModel): 削除するトレース除外対象のモデル情報

        Returns:
            None: This method does not return a value.
        """
        ...
    def Update(self) -> None:
        """
        現在表示しているトレースビューを最新の状態に更新します。
        トレース情報はモデルのトレース関係の変更に対してリアルタイムで同期しません。
        モデルのトレース関係に変更があった場合は、このメソッドにより最新の状態に更新することができます。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectNode(self, node: ITraceNode) -> None:
        """
        指定されたノードを選択します。
        現在表示しているトレースビューに、指定されたノードが所属するレーンが存在しない場合は何も行われません。
        なお、現在表示しているトレースビューにすでに選択済みのノードがある場合は次のように動作します。
        - 指定したノードと異なるレーンで選択されていたノードの選択がすべて解除します。
        - 指定したノードと同じレーンで選択されていたノードの選択は維持されます。

        Args:
            node (ITraceNode): 選択するノード

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectCell(self, row: ITraceNode, column: ITraceNode, append: bool) -> None:
        """
        表示しているビューの種別が Matrix の場合、指定されたセルを選択します。
        行、列で指定したノードが、それぞれのレーンに存在しない場合は何も行われません。
        また、レーン上のノードは選択されません。
        なお、表示しているビューの種類が Tree の場合は何も行わない。

        Args:
            row (ITraceNode): 選択するセルの行のノード
            column (ITraceNode): 選択するセルの列のノード
            append (bool): 現在のセル選択状態を維持して追加選択するか

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectNodeByModel(self, lane: ITraceLane, model: IModel) -> None:
        """
        指定されたレーンの指定された全てのモデルに対応するノードを選択します。
        ビューの種別が Matrix の場合は、行または列に対応するレーンを指定することで、
        行または列のモデルに対応するノードを選択することができます。
        現在表示しているトレースビューに、指定されたレーンが存在しない場合、
        または指定されたレーンに指定されたモデルに対応するノードが存在しない場合は何も行われません。
        なお、選択するノードが決定できた場合、現在表示しているトレースビューにすでに選択済みのノードがある場合は次のように動作します。
        - 指定したノードと異なるレーンで選択されていたノードの選択がすべて解除する
        - 指定したノードと同じレーンで選択されていたノードの選択は維持される

        Args:
            lane (ITraceLane): 選択するノードが存在するレーン
            model (IModel): 選択するノードに対応するモデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def SelectNodeByModels(self, lane: ITraceLane, models: Iterable[IModel]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearSelection(self, lane: ITraceLane) -> None:
        """
        指定されたレーンで選択された全てのノードの選択を解除します。
        現在表示しているトレースビューに、指定されたレーンが存在しない場合は何も行われません。

        Args:
            lane (ITraceLane): 選択を解除するレーン

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearAllSelection(self) -> None:
        """
        全てのレーンで選択された全てのノードの選択を解除します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def TraceViews(self) -> ITraceViewCollection:
        """トレースビュー一覧"""
        ...
    @property
    def CurrentView(self) -> ITraceView:
        """現在表示しているトレースビュー"""
        ...
    @property
    def CurrentViewType(self) -> TraceViewType:
        """現在表示しているビューの種別"""
        ...
    @property
    def ExcludedModels(self) -> ITraceCoverageExcludedModelCollection:
        """トレース除外対象のモデル一覧"""
        ...
    @property
    def SelectedNodes(self) -> ITraceNodeCollection:
        """現在のトレースビューで選択されているノード。"""
        ...

class IWorkspaceWindow:
    """
    ユーザインタフェース
    """
    @property
    def CommonUI(self) -> ICommonUI:
        """共通UIへのアクセス用インタフェース"""
        ...
    @property
    def UI(self) -> ICommonUI:
        """共通UIへのアクセス用インタフェース"""
        ...
    @property
    def Statusbar(self) -> IStatusbar:
        """ステータスバーを表すUI要素"""
        ...
    @property
    def EditorPage(self) -> IEditorPage:
        """エディタUIへのアクセスオブジェクトを取得します。"""
        ...
    @property
    def TracePage(self) -> ITracePage:
        """トレースUIへのアクセスオブジェクトを取得します。"""
        ...
    @property
    def ActivePage(self) -> str:
        """現在のアプリケーションでアクティブなページを取得または設定します。
取得する場合の振る舞いは以下です。
- \"Start\" : スタートページ
- \"Editor\" ： エディタページのアクティブタブでトレースドキュメント以外を表示している
- \"Trace\" ： エディタページのアクティブタブでトレースドキュメントを表示している
設定する場合の振る舞いは以下です。
- \"Editor\" ： 固定タブを表示する
- \"Trace\" ： トレースドキュメントタブを表示する"""
        ...
    @property
    def IsInformationPaneVisible(self) -> bool:
        """情報ペイン表示状態"""
        ...
    @property
    def ActiveInfoWindow(self) -> str:
        """情報ペインのアクティブページ
（Output | Error | SearchResult）"""
        ...
    @property
    def CurrentOutputCategory(self) -> str:
        """情報ペインのOutputのカレントカテゴリ"""
        ...
    @property
    def CurrentInfoView(self) -> IInfoView:
        """情報ウィンドウ内の現在アクティブな表示ページ"""
        ...
    @property
    def Finder(self) -> IFinder:
        """ファインダUIへのアクセス用インタフェース"""
        ...

class IFileUtility:
    """
    ファイル操作を提供するユーティリティです。
    """
    def GetFolder(self, filePath: str) -> str:
        """
        指定されたファイルの格納フォルダを取得します。

        Args:
            filePath (str): パス

        Returns:
            str: 生成したフォルダのパス
        """
        ...
    def CreateFolder(self, path: str) -> str:
        """
        指定されたパスのフォルダを生成します。

        Args:
            path (str): パス

        Returns:
            str: 生成したフォルダのパス
        """
        ...
    def CreateTextFile(self, folder: str, fileName: str, extension: str, overwrite: bool) -> str:
        """
        与えられたフォルダに指定された名前、および拡張子のテキストファイルを生成します。

        Args:
            folder (str): フォルダ
            fileName (str): ファイル名
            extension (str): 拡張子
            overwrite (bool): ファイルが存在している場合に強制的に上書きするか

        Returns:
            str: 生成したファイルのパス
        """
        ...
    def WriteAllText(self, file: str, contents: str) -> None:
        """
        指定されたファイルに与えられたテキストを書き出す。

        Args:
            file (str): ファイル
            contents (str): テキスト

        Returns:
            None: This method does not return a value.
        """
        ...

class IIndentableText:
    """
    テキストシーケンス
    """
    @overload
    def AppendLine(self, line: str) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            line (str): 文字列

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    @overload
    def AppendLine(self, format: str, *p: List[List[Any]]) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p (List[Any]): フォーマット置換オブジェクト

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def AppendLine1(self, format: str, p1: Any) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p1 (Any): フォーマット置換オブジェクト1

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def AppendLine2(self, format: str, p1: Any, p2: Any) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p1 (Any): フォーマット置換オブジェクト1
            p2 (Any): フォーマット置換オブジェクト2

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def AppendLine3(self, format: str, p1: Any, p2: Any, p3: Any) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p1 (Any): フォーマット置換オブジェクト1
            p2 (Any): フォーマット置換オブジェクト2
            p3 (Any): フォーマット置換オブジェクト3

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def AppendLine4(self, format: str, p1: Any, p2: Any, p3: Any, p4: Any) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p1 (Any): フォーマット置換オブジェクト1
            p2 (Any): フォーマット置換オブジェクト2
            p3 (Any): フォーマット置換オブジェクト3
            p4 (Any): フォーマット置換オブジェクト4

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def AppendLine5(self, format: str, p1: Any, p2: Any, p3: Any, p4: Any, p5: Any) -> IIndentableText:
        """
        指定された文字列、および改行をこのシーケンスの末尾に追加します。

        Args:
            format (str): 文字列フォーマット
            p1 (Any): フォーマット置換オブジェクト1
            p2 (Any): フォーマット置換オブジェクト2
            p3 (Any): フォーマット置換オブジェクト3
            p4 (Any): フォーマット置換オブジェクト4
            p5 (Any): フォーマット置換オブジェクト5

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def Indent(self) -> IIndentableText:
        """
        インデントレベルを増加します。

        Returns:
            IIndentableText: このシーケンス
        """
        ...
    def Outdent(self) -> IIndentableText:
        """
        インデントレベルを減少します。

        Returns:
            IIndentableText: このシーケンス
        """
        ...

class IResourceUtility:
    """
    リソース操作を提供するユーティリティです。
    """
    def GetIcon(self, path: str) -> Any:
        """
        指定されたパスのアイコンを取得します。

        Args:
            path (str): パス

        Returns:
            Any: アイコン
        """
        ...
    def GetObjectIcon(self, apiObj: IObject) -> Any:
        """
        Args:
            apiObj (IObject): オブジェクト

        """
        ...

class IUtility:
    """
    汎用操作を提供するユーティリティです。
    """
    def NewIndentableText(self, indent: str) -> IIndentableText:
        """
        新しいテキストシーケンスを生成します。

        Returns:
            IIndentableText: テキストシーケンス
        """
        ...
    def Report(self, email: str, title: str, body: str) -> None:
        """
        レポートを送信します。

        Args:
            email (str): メールアドレス
            title (str): タイトル
            body (str): 本文

        Returns:
            None: This method does not return a value.
        """
        ...

class BeforeProjectCloseEventArgs:
    """
    ワークスペース上で、プロジェクトが閉じられようとしていることを通知するイベントパラメータ
    """
    @property
    def Project(self) -> IProject:
        """閉じられるプロジェクト"""
        ...

class CardDisplayLevel(IntEnum):
    """
    カード表示レベル
    """
    None = 0  # 表示なし
    All = 1  # 常に表示
    SelectedOnly = 2  # 選択時のみ表示

class DisplayModeChangedEventArgs:
    """
    表示モードの状態変更イベントパラメータ
    """
    @property
    def PropertyName(self) -> str:
        """変更されたプロパティ名"""
        ...

class IDisplayMode:
    """
    ワークスペースの表示モードの状態
    """
    @property
    def ShowError(self) -> bool:
        """エラー情報を表示するか"""
        ...
    @property
    def ShowSearchResult(self) -> bool:
        """検索結果情報を表示するか"""
        ...
    @property
    def IsToneDowned(self) -> bool:
        """トーンダウン表示するか"""
        ...
    @property
    def CardDisplayLevel(self) -> CardDisplayLevel:
        """カード表示レベル"""
        ...
    @property
    def IsDiffViewVisible(self) -> bool:
        """差分エディタを表示するか"""
        ...
    @property
    def ShowDiff(self) -> bool:
        """差分を表示するか"""
        ...
    @property
    def ShowIndicator(self) -> bool:
        """インジケータを表示するか"""
        ...
    @property
    def ShowFeatureMark(self) -> bool:
        """フィーチャ割り当て済み要素にフィーチャマークを表示するか"""
        ...

class IWorkspace:
    """
    エクステンション向けのワークスペース情報へのアクセスオブジェクトを表します。
    """
    def CreateSearch(self) -> ISearch:
        """
        検索オブジェクトを生成します。

        Returns:
            ISearch: 検索オブジェクト。
        """
        ...
    def NewProject(self, projectName: str, description: str, profilePath: str, isSetCurrent: bool) -> IProject:
        """
        新規プロジェクトを生成します。

        Args:
            projectName (str): プロジェクト名。
            description (str): 説明。
            profilePath (str): プロファイルパス。
            isSetCurrent (bool): 生成したプロジェクトをカレントに設定するか。

        """
        ...
    @overload
    def OpenProject(self, projectPath: str, isSetCurrent: bool, excludeModelFiles: bool) -> IProject:
        """
        指定されたプロジェクトを開きます。

        Args:
            projectPath (str): プロファイルパス。
            isSetCurrent (bool): ロードしたプロジェクトをカレントに設定するか。
            excludeModelFiles (bool): モデルファイルを読み込まずにプロジェクトを開くか (true：読み込まずに開く、false：ロードモードの設定に従って開く)。

        """
        ...
    @overload
    def OpenProject(self, projectPath: str, options: OpenProjectOptions) -> IProject:
        """
        指定されたオプションを適用してプロジェクトを開きます。

        Args:
            projectPath (str): プロジェクトパス。
            options (OpenProjectOptions): オープンプロジェクトオプション。

        """
        ...
    def ReloadProject(self, project: IProject, isSetReadOnly: bool) -> IProject:
        """
        指定されたプロジェクトを再度開きます。
        プロジェクト未指定の場合は、カレントプロジェクトを再度開きます。

        Args:
            project (IProject): プロジェクト。
            isSetReadOnly (bool): 読み取り専用でプロジェクトを開くか。
物理ファイルは読み取り専用に変更せず、メモリ上に展開したプロジェクトを読み取り専用として扱います。

        """
        ...
    def CloseProject(self, project: IProject) -> None:
        """
        指定されたプロジェクトを閉じます。
        プロジェクト未指定の場合は、カレントプロジェクトを閉じます。
        指定されたプロジェクトが現在アプリケーションで開いているカレントのプロジェクトではない場合、プロジェクトが保存されていなくても警告することなく、変更を破棄してプロジェクトを閉じます。

        Args:
            project (IProject): プロジェクト。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CloseCurrentProject(self, forceClose: bool) -> None:
        """
        カレントプロジェクトを閉じます。

        Args:
            forceClose (bool): 強制的にクローズするか。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SaveProject(self, project: IProject, forceOverwrite: bool) -> bool:
        """
        指定されたプロジェクトを永続化します。
        プロジェクト未指定の場合は、カレントプロジェクトを永続化します。

        Args:
            project (IProject): プロジェクト。
            forceOverwrite (bool): 強制的に上書き保存するか。

        """
        ...
    def SaveProjectAs(self, projectPath: str, project: IProject) -> bool:
        """
        指定されたパスで、指定されたプロジェクトを永続化します。
        プロジェクト未指定の場合は、カレントプロジェクトを永続化します。

        Args:
            projectPath (str): プロジェクトパス。
            project (IProject): プロジェクト。

        """
        ...
    def CleanUpProject(self, project: IProject) -> None:
        """
        Args:
            project (IProject): プロジェクト

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetLoadMode(self, project: IProject, units: Iterable[IModelUnit], loadMode: str) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def GetModelUnitByLoadMode(self, project: IProject, loadMode: str) -> Iterable[IModelUnit]:
        """
        指定したロードモードの設定になっているモデルユニットを取得します。

        Args:
            project (IProject): プロジェクト。
            loadMode (str): ロードモード（\"Auto\",\"Manual\"）。

        """
        ...
    @overload
    def LoadModelUnits(self, project: IProject, unitFilePaths: Iterable[str]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def LoadModelUnits(self, project: IProject, units: Iterable[IModelUnit]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def SaveAll(self, project: IProject) -> None:
        """
        最新の状態に基づいてファイルを保存し直します。
        プロジェクトが未指定の場合は、カレントプロジェクトを保存します。

        Args:
            project (IProject): プロジェクト。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CanUndo(self) -> bool:
        """
        編集操作を取り消し可能か調べます。

        Returns:
            bool: 取り消し可能な場合は真。
        """
        ...
    def Undo(self) -> None:
        """
        編集操作を取り消します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CanRedo(self) -> bool:
        """
        取り消した編集操作を再実行可能か調べます。

        Returns:
            bool: 再実行可能な場合は真。
        """
        ...
    def Redo(self) -> None:
        """
        取り消した編集操作を再実行します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearUndo(self) -> None:
        """
        アンドゥスタックをクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def OpenDiff(self, comparison: IModelComparison, titleBefore: str, titleAfter: str, tooltipBefore: str, tooltipAfter: str) -> None:
        """
        指定した差分比較情報から差分比較を表示します。

        Args:
            comparison (IModelComparison): 比較処理単位情報。
            titleBefore (str): 差分ビューのタイトル。省略時は、\"変更前\"となります。
            titleAfter (str): 差分表示時のカレントビューのタイトル。省略時は、\"変更後\"となります。
            tooltipBefore (str): 差分ビューのタイトルのツールチップテキストです。省略時は titleBefore と同じとなります。
            tooltipAfter (str): 差分表示時のカレントビューのタイトルのツールチップテキストです。省略時は titleAfter と同じとなります。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CloseDiff(self) -> None:
        """
        差分比較を終了します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GenerateDocument(self, options: Any) -> Any:
        """
        ドキュメントを生成します。
        モデルナビゲータの選択要素を出力対象の基点モデルとします。

        Args:
            options (Any): ドキュメント生成オプション。

        Returns:
            Any: ドキュメント生成の結果。
        """
        ...
    @property
    def CurrentProject(self) -> IProject:
        """カレントプロジェクト
ワークスペースで現在開いているカレントプロジェクト情報"""
        ...
    @property
    def CurrentModel(self) -> IModel:
        """現在のプロジェクトで選択されているモデル要素"""
        ...
    @property
    def CurrentEditor(self) -> IEditor:
        """現在のエディタ"""
        ...
    @property
    def MainEditor(self) -> IEditor:
        """現在のメインエディタ"""
        ...
    @property
    def SubEditor(self) -> IEditor:
        """現在のサブエディタ"""
        ...
    @property
    def Errors(self) -> IErrors:
        """エラー一覧"""
        ...
    @property
    def Output(self) -> IOutput:
        """出力"""
        ...
    @property
    def Search(self) -> ISearchManager:
        """検索"""
        ...
    @property
    def CurrentProduct(self) -> IProduct:
        """カレントプロジェクトにおいて現在適用状態のプロダクト"""
        ...
    @property
    def ScmManager(self) -> IScmManager:
        """構成管理マネージャ"""
        ...
    @property
    def Scm(self) -> IScmManager:
        """構成管理"""
        ...
    @property
    def InfoDisplayStyleSet(self) -> IInfoDisplayStyleSet:
        """スタイルセットの定義（エラー・検索APIを参照）"""
        ...
    @property
    def ModelEventDispatcher(self) -> IModelEventDispatcher:
        """モデルのイベントディスパッチャ"""
        ...
    @property
    def State(self) -> IWorkspaceState:
        """ワークスペース状態"""
        ...
    @property
    def ProjectAutoReload(self) -> bool:
        """Next Design 以外からプロジェクトの変更を行った際、プロジェクトを自動で再読み込みするかを取得、または設定します。"""
        ...

class IWorkspaceState:
    """
    ワークスペースの状態管理オブジェクトです。
    """
    def SetCurrentModel(self, model: IModel) -> None:
        """
        現在のワークスペースのカレンモデルを設定します。

        Args:
            model (IModel): モデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetActiveEditorSelectedModel(self, model: IModel) -> None:
        """
        アクティブなエディタの選択要素を設定します。

        Args:
            model (IModel): モデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetActiveEditorSelectedModels(self, models: Iterable[IModel]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def SetInspectedObject(self, target: Any) -> None:
        """
        インスペクト対象の要素を設定します。

        Args:
            target (Any): 対象要素

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetInspectedObjects(self, targets: Iterable[Any]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def CurrentModel(self) -> IModel:
        """現在のワークスペースのカレントモデル"""
        ...
    @property
    def ActiveEditorSelectedModel(self) -> IModel:
        """アクティブなエディタの選択要素"""
        ...
    @property
    def ActiveEditorSelectedModels(self) -> Iterable[IModel]:
        """アクティブなエディタの選択要素（複数）"""
        ...
    @property
    def InspectedObject(self) -> Any:
        """インスペクト対象の要素"""
        ...
    @property
    def InspectedObjects(self) -> Iterable[Any]:
        """インスペクト対象の要素（複数）"""
        ...
    @property
    def DisplayMode(self) -> IDisplayMode:
        """表示モード"""
        ...

class OpenProjectOptions:
    """
    ワークスペース上で、プロジェクトが開かれたことを通知するイベントパラメータ
    """
    @property
    def IsSetCurrent(self) -> bool:
        """ロードしたプロジェクトをカレントに設定するかを取得、または設定します。
未指定の場合のデフォルトは true です。"""
        ...
    @property
    def ExcludeModelFiles(self) -> bool:
        """モデルファイルを読み込まずにプロジェクトを開くかを取得、または設定します。
- true：読み込まずに開く
- false：ロードモードの設定に従って開く
未指定の場合のデフォルトは false です。"""
        ...
    @property
    def ReadOnly(self) -> bool:
        """読み取り専用でプロジェクトを開くかを取得、または設定します。
物理ファイルは読み取り専用に変更せず、メモリ上に展開したプロジェクトを読み取り専用として扱います。
未指定の場合のデフォルトは false です。"""
        ...
    @property
    def AddToRecentFiles(self) -> bool:
        """最近使ったファイルに登録するかを取得、または設定します。
未指定の場合のデフォルトは true です。"""
        ...

class ProjectOpenedEventArgs:
    """
    ワークスペース上で、プロジェクトが開かれたことを通知するイベントパラメータ
    """
    @property
    def Project(self) -> IProject:
        """開かれたプロジェクト"""
        ...

class WorkspaceStateChangedEventArgs:
    """
    ワークスペース状態変更イベントパラメータ
    """
    @property
    def PropertyName(self) -> str:
        """変更されたプロパティ名"""
        ...

