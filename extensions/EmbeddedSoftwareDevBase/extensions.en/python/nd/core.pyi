# ============================================================
# This file was auto-generated. Do not edit directly.
# ------------------------------------------------------------
# Source DLL   : NextDesign.Core.dll
# Version      : 5.0.0.10306
# Generated at : 2026-03-11 09:56:28
# ============================================================

from typing import Any, Callable, Dict, Iterable, Iterator, List, overload
from enum import IntEnum, IntFlag

class CoreExtensionObjectConverter:
    """
    Next Designの内部オブジェクトをエクステンションのオブジェクトへ変換するコンバータークラスです
    """
    ...

class CoreExtensionObjectConverterRegistry:
    """
    エクステンションオブジェクトに関するコールバックを登録します。
    （Next Designアプリケーションが利用する内部用のインターフェースです。ユーザは利用しないで下さい。）
    """
    ...

class IDiff:
    """
    任意のプロジェクト間でのモデル情報の比較操作を提供します。
    """
    @overload
    def ComputeModels(self, target: IProject, old: IProject) -> IModelComparison:
        """
        2-way比較により、指定されたプロジェクト間の差分抽出を実施します。

        Args:
            target (IProject): 比較元になるプロジェクトです。
            old (IProject): 比較先になる、targetより古い情報をもつプロジェクトです。

        """
        ...
    @overload
    def ComputeModels(self, target: IProject, old: IProject, targetModelsUnits: Iterable[IModelUnit]) -> IModelComparison: ...
    def GetComparison(self, project: IProject) -> IModelComparison:
        """
        指定されたプロジェクトの差分情報を取得します。
        指定されたプロジェクトを対象にした、直前のComputeModelsの実行結果を取得します。

        Args:
            project (IProject): 対象のプロジェクトです。

        """
        ...

class IDifference:
    """
    差分情報へのアクセスオブジェクトです。
    """
    @property
    def IsNewItem(self) -> bool:
        """新規要素であるか（比較元にモデルがない）"""
        ...
    @property
    def IsOldItem(self) -> bool:
        """削除要素であるか（比較先にモデルがない）"""
        ...
    @property
    def IsUpdateItem(self) -> bool:
        """更新要素であるか（比較元と比較先で内容が異なる）"""
        ...
    @property
    def IsMoveItem(self) -> bool:
        """移動要素であるか（比較元と比較先で場所が異なる）"""
        ...
    @property
    def Field(self) -> str:
        """更新されたフィールド（IsUpdateItem=trueの場合のみ有効）"""
        ...
    @property
    def OldValue(self) -> Any:
        """古い値（IsUpdateItem=trueの場合のみ有効）"""
        ...
    @property
    def NewValue(self) -> Any:
        """新しい値（IsUpdateItem=trueの場合のみ有効）"""
        ...
    @property
    def OldParent(self) -> Any:
        """古い親要素（IsMoveItem=trueの場合のみ有効）"""
        ...
    @property
    def NewParent(self) -> Any:
        """新しい親要素（IsMoveItem=trueの場合のみ有効）"""
        ...
    @property
    def OldOrder(self) -> int:
        """古い順序（IsMoveItem=trueの場合のみ有効）"""
        ...
    @property
    def NewOrder(self) -> int:
        """新しい順序（IsMoveItem=trueの場合のみ有効）"""
        ...

class IDifferenceCollection:
    """
    差分情報のコレクションです。
    """
    def GetItem(self, index: int) -> IDifference:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IDifference: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IDifferenceEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IDifferenceEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IDifference]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IDifferenceEnumerator:
    """
    差分情報のコレクションの列挙子です。
    """
    ...

class IMatch:
    """
    比較情報へのアクセスオブジェクトです。
    """
    @property
    def Target(self) -> IModel:
        """比較元モデル"""
        ...
    @property
    def Reference(self) -> IModel:
        """比較先モデル"""
        ...
    @property
    def Differences(self) -> IDifferenceCollection:
        """比較対象を比較した結果の差分情報"""
        ...
    @property
    def HasDifference(self) -> bool:
        """比較対象を比較した結果差分があるか"""
        ...

class IMatchCollection:
    """
    比較情報のコレクションです。
    """
    def GetItem(self, index: int) -> IMatch:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMatch: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMatchEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMatchEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMatch]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMatchEnumerator:
    """
    比較情報のコレクションの列挙子です。
    """
    ...

class IModelComparison:
    """
    比較処理単位情報へのアクセスオブジェクトです。
    """
    def GetDifferencedMatches(self) -> IMatchCollection:
        """
        差分を抽出した比較情報を取得します。

        """
        ...
    def GetMatch(self, model: IModel) -> IMatch:
        """
        指定されたモデルの比較情報を取得します。

        Args:
            model (IModel): モデル

        """
        ...
    def RequestRecompute(self, model: IModel) -> None:
        """
        指定されたモデルに対して、差分比較の再実行を要求します。
        このメソッドを呼び出しても、対象モデルの比較はすぐに実行されません。
        実際に比較が実行されるタイミングは、エクステンションによるコマンドやイベントの一連の処理が完了した後です。

        Args:
            model (IModel): 差分比較を再実行する対象モデル

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Matches(self) -> IMatchCollection:
        """すべての比較情報"""
        ...
    @property
    def Differences(self) -> IDifferenceCollection:
        """すべての差分情報"""
        ...
    @property
    def BeforeProject(self) -> IProject:
        """変更前のプロジェクト情報"""
        ...
    @property
    def AfterProject(self) -> IProject:
        """変更後のプロジェクト情報"""
        ...

class IObject:
    """
    モデルオブジェクトを表します。
    """
    def SetId(self, identifier: str) -> None:
        """
        指定された識別子で設定します。

        Args:
            identifier (str): 識別子

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetTag(self, key: str) -> ITag:
        """
        タグ値を取得します。

        Args:
            key (str): タグキー

        Returns:
            ITag: タグ値
        """
        ...
    def GetTagValue(self, tag: str) -> str:
        """
        指定されたタグ名に一致するタグの値を取得します

        Args:
            tag (str): タグ名

        Returns:
            str: 値
        """
        ...
    def HasTags(self, tags: str, op: str) -> bool:
        """
        指定されたタグ名に一致するタグが存在するか確認します。

        Args:
            tags (str): タグ名(カンマ区切りで複数指定が可能)
            op (str): タグ名が複数指定された場合の検証方法(or / and)

        Returns:
            bool: タグが存在する場合は真
        """
        ...
    def SetTag(self, tag: str, value: str) -> None:
        """
        指定されたタグ名／値でタグを設定します。

        Args:
            tag (str): タグ名
            value (str): タグ値（未指定の場合はタグ有無のみで評価するタグを設定します。）

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveTag(self, tag: str) -> None:
        """
        指定されたタグ名に一致するタグを削除します。

        Args:
            tag (str): タグ名

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Id(self) -> str:
        """識別子"""
        ...
    @property
    def Tags(self) -> ITagCollection:
        """タグ一覧"""
        ...

class IRepresentation(IObject):
    """
    表現情報へのアクセスオブジェクトを表します。
    """
    @property
    def ViewDefinition(self) -> IViewDefinition:
        """ビュー定義"""
        ...
    @property
    def ViewDefinitionName(self) -> str:
        """定義名"""
        ...
    @property
    def ModelId(self) -> str:
        """対応するモデル識別子"""
        ...
    @property
    def Model(self) -> IModel:
        """対応するモデル"""
        ...

class IEditor(IRepresentation):
    """
    エディタ情報へのアクセスオブジェクトを表します。
    """
    def GetSelectedElements(self) -> IEditorElementCollection:
        """
        エディタで選択されている要素を取得します。

        Returns:
            IEditorElementCollection: エディタで選択されている要素。
        """
        ...
    @property
    def EditorType(self) -> str:
        """エディタ種類"""
        ...
    @property
    def EditorDefinition(self) -> IEditorDef:
        """エディタのビュー定義"""
        ...

class IConfigurationEditor(IEditor):
    """
    コンフィグレーションエディタ情報へのアクセスオブジェクトを表します。
    """
    ...

class IEditorElement(IRepresentation):
    """
    エディタ要素へのアクセスオブジェクトです。
    """
    def SetSelected(self, selected: bool) -> None:
        """
        この要素の選択状態を切り替えます。

        Args:
            selected (bool): 選択状態

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetValue(self) -> Any:
        """
        このエディタ要素に対応する値を取得します

        Returns:
            Any: このエディタ要素に対応する値。
        """
        ...
    @property
    def ElementDefinition(self) -> IElementDef:
        """このエディタ要素のビュー定義"""
        ...
    @property
    def Editor(self) -> IEditor:
        """この要素を保持するエディタ"""
        ...
    @property
    def Path(self) -> str:
        """このエディタ要素がマッピングしているフィールド（パス）"""
        ...
    @property
    def ElementOwnerRelationship(self) -> IRelationship:
        """この要素が対応するモデルと、この要素の親要素が対応するモデルとの関連"""
        ...
    @property
    def IsSelected(self) -> bool:
        """このノードが選択されているか"""
        ...

class IShape(IEditorElement):
    """
    図形要素情報へのアクセスオブジェクトを表します。
    """
    def SetVisible(self, visible: bool) -> None:
        """
        この図形の表示/非表示を切り替えます。

        Args:
            visible (bool): 表示状態（trueの場合に表示）。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetZOrder(self, zOrder: int) -> None:
        """
        Zオーダーを設定します。

        Args:
            zOrder (int): Zオーダー。
負数を指定した場合、Zオーダーの最前面へ移動します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def BringToFront(self) -> None:
        """
        この図形をZオーダーの最前面へ移動します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SendToBack(self) -> None:
        """
        この図形をZオーダーの最背面に移動します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def BringForward(self) -> None:
        """
        この図形をZオーダーの1つ前面へ移動します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SendBackward(self) -> None:
        """
        この図形をZオーダーの1つ背面へ移動します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Delete(self, deleteModel: bool) -> bool:
        """
        このシェイプを削除します。

        Args:
            deleteModel (bool): true の場合はこのシェイプとこのシェイプに対応するモデルを削除します。
マッピング対象がフィールドのシェイプは、モデルを削除せずシェイプのみ削除することはできません。

        Returns:
            bool: 削除できた場合は true、それ以外はfalse。
        """
        ...
    @property
    def Style(self) -> IShapeStyle:
        """この図形のスタイルを取得します。"""
        ...
    @property
    def IsVisible(self) -> bool:
        """この図形の表示状態を取得します。"""
        ...
    @property
    def ZOrder(self) -> int:
        """Zオーダーを取得します。"""
        ...

class IConnector(IShape):
    """
    コネクタ図形要素情報へのアクセスオブジェクトを表します。
    """
    def GetBends(self) -> Iterable[Any]:
        """
        コネクタのベンドを取得します。
        ベンドは、コネクタの接続元(StartPoint)から接続先(EndPoint)の方向にその位置(座標)を順番に列挙します。
        ベントが存在しない場合は、空の列挙を返します。

        Returns:
            Iterable[Any]: ベンド座標の列挙。
        """
        ...
    def AddBend(self, x: int, y: int) -> None:
        """
        コネクタに指定した座標でベンドを追加します。

        Args:
            x (int): ベンドの X 座標。
            y (int): ベンドの Y 座標。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddBends(self, points: Iterable[Any]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearBends(self) -> None:
        """
        コネクタのベンドをクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetLineType(self, lineTypeString: str) -> None:
        """
        コネクタの線の種類を設定します。

        Args:
            lineTypeString (str): 線の種類。
以下のいずれかの値を指定できます。
- \"Straight\" : 直線
- \"Orthogonal\" : 折れ線
- \"Bezier1Dimension\" : 1次ベジェ曲線
- \"Bezier2Dimension\" : 2次ベジェ曲線

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def StartPoint(self) -> INode:
        """コネクタ始点に接続されたノード"""
        ...
    @property
    def EndPoint(self) -> INode:
        """コネクタ終点に接続されたノード"""
        ...
    @property
    def LineType(self) -> str:
        """コネクタの線の種類を取得します。
線の種類は以下の通りです。
- \"Straight\" : 直線
- \"Orthogonal\" : 折れ線
- \"Bezier1Dimension\" : 1次ベジェ曲線
- \"Bezier2Dimension\" : 2次ベジェ曲線
- \"Tree\" : ツリー (※ツリーダイアグラムのコネクタの場合のみ)"""
        ...

class IConnectorCollection:
    """
    コネクタ図形要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> IConnector:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IConnector: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IConnectorEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IConnectorEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IConnector]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IConnectorEnumerator:
    """
    コネクタ図形要素情報のコレクションの列挙子です。
    """
    ...

class ICustomEditor(IEditor):
    """
    カスタムエディタ情報へのアクセスオブジェクトを表します。
    """
    @property
    def CustomEditorTypeId(self) -> str:
        """カスタムエディタの種類識別子"""
        ...
    @property
    def Settings(self) -> ICustomEditorSettings:
        """エディタ固有の設定情報"""
        ...

class ICustomEditorSettings:
    """
    カスタムエディタ固有の設定情報へのアクセスオブジェクトを表します。
    """
    def SetValue(self, key: str, value: Any, encrypt: bool) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def GetValue(self, key: str, decrypt: bool) -> Any: ...
    def RemoveValue(self, key: str) -> None:
        """
        指定されたキーの設定情報を削除します。

        Args:
            key (str): キー

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearAll(self) -> None:
        """
        全ての設定情報をクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Keys(self) -> Iterable[str]:
        """設定情報のキーの列挙"""
        ...

class ISequenceShape(IShape):
    """
    シーケンス図のシェイプの共通インターフェースです。
    """
    ...

class ISequenceNodeShape(ISequenceShape):
    """
    シーケンス図のノード図形へのアクセスオブジェクトの基底インタフェースを表します。
    """
    @property
    def Location(self) -> Any:
        """位置（ダイアグラム座標）を取得します。"""
        ...
    @property
    def LocationX(self) -> float:
        """X位置（ダイアグラム座標）を取得します。"""
        ...
    @property
    def LocationY(self) -> float:
        """Y位置（ダイアグラム座標）を取得します。"""
        ...
    @property
    def Size(self) -> Any:
        """サイズを取得します。"""
        ...
    @property
    def Width(self) -> float:
        """幅を取得します。"""
        ...
    @property
    def Height(self) -> float:
        """高さを取得します。"""
        ...

class IDestructionShape(ISequenceNodeShape):
    """
    シーケンス図の破棄図形へのアクセスオブジェクトを表します。
    """
    @property
    def Lifeline(self) -> ILifelineShape:
        """ライフラインを取得します。"""
        ...

class IDestructionShapeCollection:
    """
    シーケンス図の破棄図形のコレクションです。
    """
    def GetItem(self, index: int) -> IDestructionShape:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IDestructionShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IDestructionShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IDestructionShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IDestructionShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IDestructionShapeEnumerator:
    """
    シーケンス図の破棄図形のコレクションの列挙子を定義します。
    """
    ...

class IDiagram(IEditor):
    """
    ダイアグラムエディタ情報へのアクセスオブジェクトを表します。
    """
    def GetShapeById(self, shapeIdentifier: str) -> IShape:
        """
        指定された識別子のシェイプを取得します。

        Args:
            shapeIdentifier (str): シェイプの識別子。

        Returns:
            IShape: シェイプ。
        """
        ...
    def GetShapesByModel(self, model: IModel) -> IShapeCollection:
        """
        指定されたモデルに対応するシェイプを取得します。

        Args:
            model (IModel): モデル。

        Returns:
            IShapeCollection: シェイプの列挙。
        """
        ...
    def GetChildNodes(self, node: INode) -> INodeCollection:
        """
        指定されたノードの子ノードを取得します。

        Args:
            node (INode): ノード。

        Returns:
            INodeCollection: 子ノードの列挙。
        """
        ...
    def GetConnectorByNode(self, node: INode) -> IConnectorCollection:
        """
        指定されたノードに接続されているコネクタを取得します。

        Args:
            node (INode): ノード。

        Returns:
            IConnectorCollection: コネクタの列挙。
        """
        ...
    def GetSelectedShapes(self) -> IShapeCollection:
        """
        エディタで選択されているシェイプを取得します。

        Returns:
            IShapeCollection: 選択されているシェイプ。
        """
        ...
    def CanAddNodeShape(self, model: IModel) -> bool:
        """
        指定したモデルに対応するノードシェイプを追加できるか調べます。

        Args:
            model (IModel): モデル。

        Returns:
            bool: ノードシェイプを追加できる場合は true、それ以外は false。
        """
        ...
    def AddNodeShape(self, model: IModel, shapeDef: IElementDef) -> INode:
        """
        指定されたモデルに対応するノードシェイプを追加します。
        ただし、対応するノードシェイプが既に非表示で存在する場合は、そのシェイプを表示します。

        Args:
            model (IModel): 追加するノードシェイプが表現するモデル。
            shapeDef (IElementDef): 追加するノードシェイプのエディタ要素定義。

        Returns:
            INode: 作成されたノード。非表示ノードを表示した場合は、表示したノード。
        """
        ...
    def ShowShape(self, shape: IShape) -> None:
        """
        指定されたシェイプを表示します。

        Args:
            shape (IShape): 表示するシェイプ。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ShowShapes(self, shapes: Iterable[IShape]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def HideShape(self, shape: IShape) -> None:
        """
        指定されたシェイプを非表示にします。
        マッピング対象がクラスのシェイプを指定した場合、削除します。

        Args:
            shape (IShape): 非表示にするシェイプ。

        Returns:
            None: This method does not return a value.
        """
        ...
    def HideShapes(self, shapes: Iterable[IShape]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def MoveToCanvas(self, shape: INode) -> None:
        """
        指定されたノードシェイプを表示上ダイアグラムが親となるように移動します。
        この時、ノードシェイプが対応するモデルの構造は変更しません。
        なお、指定するノードシェイプは次の条件をすべて満たしている必要があります。条件を満たさないノードシェイプが指定された場合は何も行いません。
        - ポートシェイプでない
        - マッピング対象がフィールドでない。

        Args:
            shape (INode): ノードシェイプ。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def MoveToCanvas(self, nodes: Iterable[INode]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Relocate(self) -> None:
        """
        全てのノードを再配置します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Relocate(self, targets: Iterable[INode]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Reroute(self, avoidOverlap: bool) -> None:
        """
        このダイアグラム上の全てのコネクタの経路を再計算します。
        経路計算の対象に、直交折れ線を含む場合、avoidOverlap に false を指定して
        経路計算を簡略することで計算処理を高速化することができる。

        Args:
            avoidOverlap (bool): コネクタ同士の重なりを回避するか。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Reroute(self, avoidOverlap: bool, connectors: Iterable[IConnector]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Shapes(self) -> IShapeCollection:
        """シェイプ一覧を取得します。"""
        ...
    @property
    def Nodes(self) -> INodeCollection:
        """ノードシェイプ一覧を取得します。"""
        ...
    @property
    def Connectors(self) -> IConnectorCollection:
        """コネクタシェイプ一覧を取得します。"""
        ...
    @property
    def DisplayedShapes(self) -> IShapeCollection:
        """表示中のシェイプ一覧を取得します。"""
        ...

class IEditorCollection:
    """
    エディタ情報のコレクションです。
    """
    def GetItem(self, index: int) -> IEditor:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IEditor: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IEditorEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IEditorEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IEditor]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IEditorElementCollection:
    """
    エディタ情報へのアクセスオブジェクトのコレクションです。
    """
    def GetItem(self, index: int) -> IEditorElement:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IEditorElement: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IEditorElementEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IEditorElementEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IEditorElement]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IEditorElementEnumerator:
    """
    エディタ要素のコレクションの列挙子を定義します
    """
    ...

class IEditorEnumerator:
    """
    エディタ情報のコレクションの列挙子です。
    """
    ...

class IMessagePortShape(ISequenceNodeShape):
    """
    シーケンス図のメッセージ端点となる図形へのアクセスオブジェクトを表します。
    """
    @property
    def SendMessages(self) -> IMessageShapeCollection:
        """送信メッセージを取得します。"""
        ...
    @property
    def ReceiveMessages(self) -> IMessageShapeCollection:
        """受信メッセージを取得します。"""
        ...

class IExecutionSpecificationShape(IMessagePortShape):
    """
    シーケンス図の実行仕様図形へのアクセスオブジェクトを表します。
    """
    @property
    def Lifeline(self) -> ILifelineShape:
        """ライフラインを取得します。"""
        ...
    @property
    def Activator(self) -> IMessageShape:
        """起動メッセージを取得します。"""
        ...
    @property
    def Reply(self) -> IMessageShape:
        """応答メッセージを取得します。"""
        ...
    @property
    def Length(self) -> float:
        """実行仕様の矩形の長さを取得します。"""
        ...

class IExecutionSpecificationShapeCollection:
    """
    シーケンス図の実行仕様図形のコレクションです。
    """
    def GetItem(self, index: int) -> IExecutionSpecificationShape:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IExecutionSpecificationShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IExecutionSpecificationShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IExecutionSpecificationShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IExecutionSpecificationShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IExecutionSpecificationShapeEnumerator:
    """
    シーケンス図の実行仕様図形のコレクションの列挙子です。
    """
    ...

class IForm(IEditor):
    """
    フォームエディタ情報へのアクセスオブジェクトを表します。
    """
    def GetSelectedControls(self) -> IFormElementCollection:
        """
        エディタで選択されているフォーム要素を取得します。
        選択されたフォーム要素が存在しない場合は空のコレクションを返します。

        """
        ...
    @property
    def Elements(self) -> IFormElementCollection:
        """フォーム要素一覧"""
        ...
    @property
    def RootControl(self) -> IFormElement:
        """フォームのルートコントロール"""
        ...

class IFormElement(IEditorElement):
    """
    フォーム要素情報へのアクセスオブジェクトを表します。
    """
    @property
    def ControlType(self) -> str:
        """このフォーム要素の種類を取得します。
\"TextBox\" : テキストボックス
\"RichTextBox\" : リッチテキストボックス
\"CheckBox\" : チェックボックス
\"ComboBox\" : コンボボックス
\"List\" : リスト
\"Grid\" : グリッド
\"ModelReferenceControl\" : モデル参照コントロール
\"EntityControl\" : エンティティコントロール
\"GroupControl\" : グループコントロール
\"GridRow\" : グリッド行"""
        ...
    @property
    def Controls(self) -> IFormElementCollection:
        """フォーム子要素一覧"""
        ...

class IFormElementCollection:
    """
    フォーム要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> IFormElement:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IFormElement: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IFormElementEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IFormElementEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IFormElement]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IFormElementEnumerator:
    """
    フォーム要素情報のコレクションの列挙子です。
    """
    ...

class IFragmentShape(ISequenceNodeShape):
    """
    シーケンス図の複合フラグメント図形へのアクセスオブジェクトです。
    """
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...
    @property
    def Lifelines(self) -> ILifelineShapeCollection:
        """フラグメントに属するライフラインを取得します。"""
        ...
    @property
    def Messages(self) -> IMessageShapeCollection:
        """フラグメントに属するメッセージを取得します。
メッセージの起点がフラグメントの矩形内に含まれるメッセージを取得します。"""
        ...
    @property
    def Operands(self) -> IOperandShapeCollection:
        """フラグメントに属するオペランドを取得します。"""
        ...

class IFragmentShapeCollection:
    """
    シーケンス図の複合フラグメント図形のコレクションです。
    """
    def GetItem(self, index: int) -> IFragmentShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IFragmentShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IFragmentShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IFragmentShapeEnumerator: コレクションを反復処理する列挙子。
        """
        ...
    def __iter__(self) -> Iterator[IFragmentShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IFragmentShapeEnumerator:
    """
    シーケンス図の複合フラグメント図形のコレクションの列挙子です。
    """
    ...

class IFrameShape(IMessagePortShape):
    """
    シーケンス図のフレーム図形へのアクセスオブジェクトを表します。
    """
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...

class IGrid(IFormElement):
    """
    フォームのグリッドへのアクセスインタフェースです。
    """
    def GetSelectedRows(self) -> IGridRowCollection:
        """
        このグリッドで選択された行を取得します。
        選択された行が存在しない場合は空のコレクションを返します。

        """
        ...
    @property
    def Columns(self) -> IGridColumnCollection:
        """グリッドの列情報"""
        ...
    @property
    def Rows(self) -> IGridRowCollection:
        """グリッドの行情報"""
        ...

class IGridCell:
    """
    フォームグリッド行のセルへのアクセスインタフェースです。
    """
    def GetValue(self) -> Any:
        """
        このセルの値を取得します。
        このメソッドの呼び出しは、this.Model.GetField(this.Path) と等価になります。

        """
        ...
    @property
    def Column(self) -> IGridColumn:
        """列情報"""
        ...
    @property
    def Model(self) -> IModel:
        """モデル
このセルの属するグリッド行（IGridRow）のModelと等価になります。"""
        ...
    @property
    def Path(self) -> str:
        """パス
Column.Path と等価になります。"""
        ...

class IGridCellCollection:
    """
    フォームグリッド行のセルのコレクションです。
    """
    def GetItem(self, index: int) -> IGridCell:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IGridCell: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IGridCellEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IGridCellEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IGridCell]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IGridCellEnumerator:
    """
    フォームグリッド行のコレクションの列挙子です。
    """
    ...

class IGridColumn:
    """
    フォームのグリッド列へのアクセスインタフェースです。
    """
    @property
    def Path(self) -> str:
        """フィールド（パス）"""
        ...
    @property
    def DataTypeName(self) -> str:
        """列データ型名
bool型 : \"Boolean\"
int型 : \"Integer\"
double型 : \"Double\"
文字列型 : \"String\"
リッチテキスト型 : \"RichText\"
列挙型 : IEnumの完全修飾名 （例：\"Package1.SubPackage1.UsecaseKind\"）
クラス型（モデル参照） : IClassの完全修飾名 （例：\"Package1.SubPackage1.Usecase\"）"""
        ...

class IGridColumnCollection:
    """
    グリッド列のコレクションです。
    """
    def GetItem(self, index: int) -> IGridColumn:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IGridColumn: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IGridColumnEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IGridColumnEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IGridColumn]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IGridColumnEnumerator:
    """
    グリッド列のコレクションの列挙子です。
    """
    ...

class IGridRow(IFormElement):
    """
    フォームのグリッド行へのアクセスインタフェースです。
    """
    def GetSelectedCells(self) -> IGridCellCollection:
        """
        このグリッド行で選択されているセルを取得します。
        選択されたセルが存在しない場合は空のコレクションを返します。

        """
        ...
    @property
    def Cells(self) -> IGridCellCollection:
        """このグリッド行のセル"""
        ...

class IGridRowCollection:
    """
    グリッド行のコレクションです。
    """
    def GetItem(self, index: int) -> IGridRow:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IGridRow: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IGridRowEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IGridRowEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IGridRow]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IGridRowEnumerator:
    """
    グリッド行のコレクションの列挙子です。
    """
    ...

class IInteractionUseShape(ISequenceNodeShape):
    """
    シーケンス図の相互作用利用図形へのアクセスオブジェクトです。
    """
    @property
    def Lifelines(self) -> ILifelineShapeCollection:
        """相互作用利用に属するライフラインを取得します。"""
        ...
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...

class IInteractionUseShapeCollection:
    """
    シーケンス図の相互作用利用図形のコレクションです。
    """
    def GetItem(self, index: int) -> IInteractionUseShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IInteractionUseShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IInteractionUseShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IInteractionUseShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IInteractionUseShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IInteractionUseShapeEnumerator:
    """
    シーケンス図の相互作用利用図形のコレクションの列挙子です。
    """
    ...

class ILifelineShape(ISequenceNodeShape):
    """
    シーケンス図のライフライン図形へのアクセスオブジェクトを表します。
    """
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...
    @property
    def ExecutionSpecifications(self) -> IExecutionSpecificationShapeCollection:
        """実行仕様を取得します。"""
        ...
    @property
    def Destruction(self) -> IDestructionShape:
        """破棄を取得します。"""
        ...
    @property
    def TimelineLength(self) -> float:
        """タイムライン（生存線）の長さを取得します。"""
        ...
    @property
    def TypeModel(self) -> IModel:
        """型にマッピングされたモデルを取得します。"""
        ...
    @property
    def Figure(self) -> str:
        """ライフラインの図形を取得します。"""
        ...

class ILifelineShapeCollection:
    """
    シーケンス図のライフライン図形のコレクションです。
    """
    def GetItem(self, index: int) -> ILifelineShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス

        Returns:
            ILifelineShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ILifelineShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            ILifelineShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ILifelineShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class ILifelineShapeEnumerator:
    """
    シーケンス図のライフライン図形のコレクションの列挙子です。
    """
    ...

class IMessageEndShape(IMessagePortShape):
    """
    シーケンス図のメッセージ端図形へのアクセスオブジェクトを表します。
    """
    @property
    def Message(self) -> IMessageShape:
        """送信または受信メッセージを取得します。"""
        ...

class IMessageEndShapeCollection:
    """
    シーケンス図のメッセージ端図形のコレクションです。
    """
    def GetItem(self, index: int) -> IMessageEndShape:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMessageEndShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMessageEndShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMessageEndShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMessageEndShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMessageEndShapeEnumerator:
    """
    シーケンス図のメッセージ端図形のコレクションの列挙子です。
    """
    ...

class ISequenceConnectorShape(ISequenceShape):
    """
    シーケンス図のコネクタ図形へのアクセスオブジェクトの基底インタフェースを表します。
    """
    @property
    def Source(self) -> ISequenceShape:
        """コネクタの接続元シェイプを取得します。"""
        ...
    @property
    def Target(self) -> ISequenceShape:
        """コネクタの接続先シェイプを取得します。"""
        ...

class IMessageShape(ISequenceConnectorShape):
    """
    シーケンス図のメッセージ図形へのアクセスオブジェクトを表します。
    """
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...
    @property
    def SendPort(self) -> IMessagePortShape:
        """メッセージ送信元ポートを取得します。"""
        ...
    @property
    def Sender(self) -> ILifelineShape:
        """メッセージ送信元ライフラインを取得します。
ライフラインからの送信メッセージでない場合は null を返します。"""
        ...
    @property
    def ReceivePort(self) -> IMessagePortShape:
        """メッセージ受信先ポートを取得します。"""
        ...
    @property
    def Receiver(self) -> ILifelineShape:
        """メッセージ受信先ライフラインを取得します。
ライフラインへの受信メッセージでない場合は null を返します。"""
        ...
    @property
    def TypeModel(self) -> IModel:
        """型にマッピングされたモデルを取得します。"""
        ...
    @property
    def SourceY(self) -> float:
        """メッセージの起点のY座標を取得します。
メッセージの起点は、送信元となるシェイプとの接続点です。"""
        ...
    @property
    def TargetY(self) -> float:
        """メッセージの終点のY座標を取得します。
メッセージの終点は、受信先となるシェイプとの接続点です。"""
        ...
    @property
    def SelfloopBendsX(self) -> float:
        """自己接続メッセージにおけるベンド位置のX座標を取得します。
自己接続メッセージでない場合は、常に0が返ります。
自己接続メッセージは、送信元と受信先のライフラインが同一となるメッセージです。
ベンド位置は、該当メッセージにおける最初の折れ線のポイントとなります。"""
        ...

class IMessageShapeCollection:
    """
    シーケンス図のメッセージ図形のコレクションです。
    """
    def GetItem(self, index: int) -> IMessageShape:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMessageShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMessageShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMessageShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMessageShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMessageShapeEnumerator:
    """
    シーケンス図のメッセージ図形のコレクションの列挙子です。
    """
    ...

class INode(IShape):
    """
    ノード図形要素情報へのアクセスオブジェクトを表します。
    """
    def SetLocation(self, point: Any) -> None:
        """
        この図形の位置を変更します。

        Args:
            point (Any): 位置

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetLocationAt(self, x: float, y: float) -> None:
        """
        この図形の位置を変更します。

        Args:
            x (float): X座標
            y (float): Y座標

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetSize(self, size: Any) -> None:
        """
        この図形のサイズを変更します。

        Args:
            size (Any): サイズ

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetSizeAt(self, w: float, h: float) -> None:
        """
        この図形のサイズを変更します。

        Args:
            w (float): 幅
            h (float): 高さ

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetBounds(self, rect: Any) -> None:
        """
        この図形の位置とサイズを変更します。

        Args:
            rect (Any): 矩形

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetBoundsAt(self, x: float, y: float, w: float, h: float) -> None:
        """
        この図形の位置とサイズを変更します。

        Args:
            x (float): X座標
            y (float): Y座標
            w (float): 幅
            h (float): 高さ

        Returns:
            None: This method does not return a value.
        """
        ...
    def ShowPorts(self) -> None:
        """
        ポートを一括で表示します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def HidePorts(self) -> None:
        """
        ポートを一括で非表示にします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ShowCompositeNodes(self) -> None:
        """
        子ノードを一括で表示します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def HideCompositeNodes(self) -> None:
        """
        子ノードを一括で非表示にします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RelocatePorts(self, orientation: PortOrientation) -> None:
        """
        このノードのポートを再配置します。

        Args:
            orientation (PortOrientation): 再配置するポート方向（辺）

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Location(self) -> Any:
        """位置（ダイアグラム座標）"""
        ...
    @property
    def LocationX(self) -> float:
        """X位置（ダイアグラム座標）"""
        ...
    @property
    def LocationY(self) -> float:
        """Y位置（ダイアグラム座標）"""
        ...
    @property
    def Size(self) -> Any:
        """サイズ"""
        ...
    @property
    def Width(self) -> float:
        """幅"""
        ...
    @property
    def Height(self) -> float:
        """高さ"""
        ...
    @property
    def Ports(self) -> IPortCollection:
        """ポート一覧"""
        ...
    @property
    def CompositeNodes(self) -> INodeCollection:
        """子ノード一覧"""
        ...
    @property
    def NodeStyle(self) -> INodeShapeStyle:
        """ノードシェイプのスタイルを取得します。"""
        ...

class INodeCollection:
    """
    ノード図形要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> INode:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            INode: コレクション要素
        """
        ...
    def GetEnumerator(self) -> INodeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            INodeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[INode]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class INodeEnumerator:
    """
    ノード図形要素情報のコレクションの列挙子です。
    """
    ...

class IShapeStyle:
    """
    シェイプのスタイル情報へのアクセスインタフェースです。
    """
    @property
    def BackColor(self) -> str:
        """背景色"""
        ...
    @property
    def ForeColor(self) -> str:
        """前景色"""
        ...
    @property
    def BorderColor(self) -> str:
        """線色"""
        ...
    @property
    def QuickStyle(self) -> str:
        """クイックスタイル"""
        ...
    @property
    def BorderThickness(self) -> int:
        """線の太さ"""
        ...
    @property
    def BorderStyle(self) -> str:
        """線のスタイル
\"Solid\" : 実線
\"Dot\" : 点線
\"Dash\" : 鎖線
\"DashDot\" : 1点鎖線
\"DashDotDot\" : 2点鎖線"""
        ...

class INodeShapeStyle(IShapeStyle):
    """
    ノードシェイプのスタイル情報へのアクセスインタフェースです。
    """
    def SetImage(self, data: List[int], format: str) -> None:
        """
        このシェイプに画像を設定します。

        Args:
            data (List[int]): 画像データのバイト配列。
            format (str): 入力した画像データのフォーマット。値域は\"png\", \"bmp\", \"jpg\", \"gif\"で大文字小文字は区別しません。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearImage(self) -> None:
        """
        このシェイプの画像をクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Figure(self) -> str:
        """ノードシェイプの図形です。
大文字小文字は区別しません。
値域外の値が指定された場合は図形は表示されません。
nullまたは空文字を指定した場合はビュー定義で指定している図形となります。
シェイプ定義で図形の変更が許可されていない場合は設定しようとしても図形変更されず無視されます。"""
        ...
    @property
    def IsSimplified(self) -> bool:
        """簡易表示であるかを取得・設定します。"""
        ...

class INoteAnchorShape(ISequenceConnectorShape):
    """
    ノートとノートの対象要素を接続するノートアンカー図形情報へのアクセスオブジェクトです。
    """
    @property
    def Note(self) -> INoteShape:
        """アンカーが接続しているノートを取得します。"""
        ...
    @property
    def TargetX(self) -> float:
        """アンカーの終点のX座標を取得します。
アンカーの終点は、アンカーが接続しているシーケンス図要素側の接続点です。"""
        ...
    @property
    def TargetY(self) -> float:
        """アンカーの終点のY座標を取得します。
アンカーの終点は、アンカーが接続しているシーケンス図要素側の接続点です。"""
        ...

class INoteAnchorShapeCollection:
    """
    ノートとノートの対象要素を接続するノートアンカー図形情報のコレクションです。
    """
    def GetItem(self, index: int) -> INoteAnchorShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            INoteAnchorShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> INoteAnchorShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            INoteAnchorShapeEnumerator: コレクションを反復処理する列挙子。
        """
        ...
    def __iter__(self) -> Iterator[INoteAnchorShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class INoteAnchorShapeEnumerator:
    """
    ノートとノートの対象要素を接続するノートアンカー図形情報のコレクションの列挙子です。
    """
    ...

class INoteShape(ISequenceNodeShape):
    """
    ノート図形情報へのアクセスオブジェクトです。
    """
    @property
    def Text(self) -> str:
        """テキストを取得します。"""
        ...
    @property
    def NoteAnchors(self) -> INoteAnchorShapeCollection:
        """接続されているノートアンカーを取得します。"""
        ...

class INoteShapeCollection:
    """
    ノート図形情報のコレクションです。
    """
    def GetItem(self, index: int) -> INoteShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            INoteShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> INoteShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            INoteShapeEnumerator: コレクションを反復処理する列挙子。
        """
        ...
    def __iter__(self) -> Iterator[INoteShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class INoteShapeEnumerator:
    """
    ノート図形情報のコレクションの列挙子です。
    """
    ...

class IOperandShape(ISequenceShape):
    """
    シーケンス図の複合フラグメントのオペランド図形へのアクセスオブジェクトです。
    """
    @property
    def OwnerFragment(self) -> IFragmentShape:
        """このオペランドが属する複合フラグメントを取得します。"""
        ...
    @property
    def Guard(self) -> str:
        """オペランドのガードテキストを取得します。"""
        ...
    @property
    def Position(self) -> float:
        """オペランドの左上のY座標を取得します。"""
        ...
    @property
    def Messages(self) -> IMessageShapeCollection:
        """オペランドに属するメッセージを取得します。
メッセージの起点がオペランドの矩形内に含まれるメッセージを取得します。"""
        ...

class IOperandShapeCollection:
    """
    シーケンス図の複合フラグメントのオペランド図形のコレクションです。
    """
    def GetItem(self, index: int) -> IOperandShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IOperandShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IOperandShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IOperandShapeEnumerator: コレクションを反復処理する列挙子。
        """
        ...
    def __iter__(self) -> Iterator[IOperandShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IOperandShapeEnumerator:
    """
    シーケンス図の複合フラグメントのオペランド図形のコレクションの列挙子です。
    """
    ...

class IPort(INode):
    """
    ポート図形要素情報へのアクセスオブジェクトを表します。
    """
    def CanChangeOrientation(self, orientation: str) -> bool:
        """
        このポートを指定方向に配置できるか調べます。

        Args:
            orientation (str): ポート方向

        Returns:
            bool: 配置できる場合は真を返します。
        """
        ...
    def ChangeOrientation(self, orientation: str) -> None:
        """
        ポート方向を変更します。

        Args:
            orientation (str): ポート方向

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetLocationRatio(self, ratio: float) -> None:
        """
        ポート位置の割合を設定します。

        Args:
            ratio (float): ポート位置の割合(0～1の間のdouble値)

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Orientation(self) -> str:
        """ポート方向"""
        ...
    @property
    def LocationRatio(self) -> float:
        """ポート位置の割合"""
        ...

class IPortCollection:
    """
    ポート図形要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> IPort:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IPort: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IPortEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IPortEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IPort]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IPortEnumerator:
    """
    ポート図形要素情報のコレクションの列挙子です。
    """
    ...

class IRepresentationCollection:
    """
    表現情報のコレクションです。
    """
    def GetItem(self, index: int) -> IRepresentation:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IRepresentation: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IRepresentationEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IRepresentationEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IRepresentation]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IRepresentationEnumerator:
    """
    表現情報のコレクションの列挙子です。
    """
    ...

class ISequenceDiagram(IEditor):
    """
    シーケンス図（ダイアグラム）情報へのアクセスオブジェクトを表します。
    """
    def GetShapeById(self, shapeIdentifier: str) -> ISequenceShape:
        """
        指定した識別子のシェイプを取得します。

        Args:
            shapeIdentifier (str): シェイプのId。

        Returns:
            ISequenceShape: 指定した識別子のシェイプ。
        """
        ...
    def GetShapesByModel(self, model: IModel) -> ISequenceShapeCollection:
        """
        指定したモデルに対応するシェイプを取得します。

        Args:
            model (IModel): 指定したモデル。

        Returns:
            ISequenceShapeCollection: 指定したモデルに対応するシェイプの一覧。
        """
        ...
    def GetSelectedShapes(self) -> ISequenceShapeCollection:
        """
        エディタで選択されているシェイプを取得します。

        Returns:
            ISequenceShapeCollection: エディタで選択されているシェイプ。
        """
        ...
    @property
    def Shapes(self) -> ISequenceShapeCollection:
        """全てのシェイプの一覧を取得します。"""
        ...
    @property
    def Frame(self) -> IFrameShape:
        """フレームのシェイプを取得します。"""
        ...
    @property
    def Lifelines(self) -> ILifelineShapeCollection:
        """ライフラインのシェイプを取得します。"""
        ...
    @property
    def Messages(self) -> IMessageShapeCollection:
        """メッセージのシェイプを取得します。"""
        ...
    @property
    def ExecutionSpecifications(self) -> IExecutionSpecificationShapeCollection:
        """実行仕様のシェイプを取得します。"""
        ...
    @property
    def Destructions(self) -> IDestructionShapeCollection:
        """破棄のシェイプを取得します。"""
        ...
    @property
    def MessageEnds(self) -> IMessageEndShapeCollection:
        """メッセージ端のシェイプを取得します。"""
        ...
    @property
    def Fragments(self) -> IFragmentShapeCollection:
        """複合フラグメントのシェイプを取得します。"""
        ...
    @property
    def InteractionUses(self) -> IInteractionUseShapeCollection:
        """相互作用利用のシェイプを取得します。"""
        ...
    @property
    def Notes(self) -> INoteShapeCollection:
        """ノートのシェイプを取得します。"""
        ...
    @property
    def NoteAnchors(self) -> INoteAnchorShapeCollection:
        """ノートアンカーのシェイプを取得します。"""
        ...

class ISequenceShapeCollection:
    """
    シーケンス図のシェイプの共通コレクションです。
    """
    def GetItem(self, index: int) -> ISequenceShape:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            ISequenceShape: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> ISequenceShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            ISequenceShapeEnumerator: コレクションを反復処理する列挙子。
        """
        ...
    def __iter__(self) -> Iterator[ISequenceShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class ISequenceShapeEnumerator:
    """
    シーケンス図のシェイプの共通コレクションの列挙子です。
    """
    ...

class IShapeCollection:
    """
    図形要素情報のコレクションです。
    """
    def GetItem(self, index: int) -> IShape:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IShape: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IShapeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IShapeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IShape]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IShapeEnumerator:
    """
    図形要素情報のコレクションの列挙子です。
    """
    ...

class ITreeGrid(IEditor):
    """
    ツリーグリッド情報へのアクセスオブジェクトです。
    """
    def GetSelectedNodes(self, excludeSelectedChildren: bool) -> ITreeGridNodeCollection:
        """
        選択されているツリーノードを取得します。

        Args:
            excludeSelectedChildren (bool): このパラメータに真を指定すると、ツリーノードの親要素が選択されている場合は子要素の選択状態に関わらず除外されます。

        Returns:
            ITreeGridNodeCollection: 選択されているツリーノード
        """
        ...
    @property
    def Columns(self) -> ITreeGridColumnCollection:
        """表示列情報"""
        ...
    @property
    def FixedColumnIndex(self) -> int:
        """固定列のインデックス"""
        ...
    @property
    def ShowSingleLine(self) -> bool:
        """要素を1行分の高さで表示するか"""
        ...
    @property
    def Root(self) -> ITreeGridNode:
        """ツリーグリッドの基点のツリーノード"""
        ...

class ITreeGridCell:
    """
    ツリーグリッドのノードのセルアクセスオブジェクトを表します。
    """
    def GetValue(self) -> Any:
        """
        このセルの値を取得します。
        このメソッドの呼び出しは、this.Model.GetField(this.Path) と等価になります。

        """
        ...
    @property
    def Column(self) -> ITreeGridColumn:
        """列情報"""
        ...
    @property
    def Model(self) -> IModel:
        """モデル"""
        ...
    @property
    def Path(self) -> str:
        """パス"""
        ...

class ITreeGridCellCollection:
    """
    ツリーグリッドノードのセルのコレクションです。
    """
    def GetItem(self, index: int) -> ITreeGridCell:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITreeGridCell: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITreeGridCellEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITreeGridCellEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITreeGridCell]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITreeGridCellEnumerator:
    """
    ツリーグリッドのノードのセルのコレクションの列挙子です。
    """
    ...

class ITreeGridColumn:
    """
    ツリーグリッドの列情報へのアクセスオブジェクトです。
    """
    @property
    def DisplayName(self) -> str:
        """表示名
例：\"名前\""""
        ...
    @property
    def Path(self) -> str:
        """フィールド（パス）
例：\"Name\", \"MainActor.Name\""""
        ...
    @property
    def ShowColumn(self) -> bool:
        """この列を表示するか"""
        ...
    @property
    def Width(self) -> float:
        """列幅"""
        ...
    @property
    def Order(self) -> int:
        """列の表示順序"""
        ...
    @property
    def IsFixed(self) -> bool:
        """この列が固定列であるか"""
        ...
    @property
    def DataTypeName(self) -> str:
        """列データ型名
bool型 : \"Boolean\"
int型 : \"Integer\"
double型 : \"Double\"
文字列型 : \"String\"
リッチテキスト型 : \"RichText\"
列挙型 : IEnumの完全修飾名 （例：\"Package1.SubPackage1.UsecaseKind\"）
クラス型（モデル参照） : IClassの完全修飾名 （例：\"Package1.SubPackage1.Usecase\"）
これは実験的な実装です。一般の開発者は使わないでください。"""
        ...

class ITreeGridColumnCollection:
    """
    ツリーグリッド列情報のコレクションです。
    """
    def GetItem(self, index: int) -> ITreeGridColumn:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITreeGridColumn: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITreeGridColumnEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITreeGridColumnEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITreeGridColumn]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITreeGridColumnEnumerator:
    """
    ツリーグリッドの列情報のコレクションの列挙子です。
    """
    ...

class ITreeGridNode(IEditorElement):
    """
    ツリーグリッドのノード情報へのアクセスオブジェクトを表します。
    """
    def IsCellSelected(self, column: ITreeGridColumn) -> bool:
        """
        このノードで指定された列のセルが選択されているか調べます。

        Args:
            column (ITreeGridColumn): 列情報

        """
        ...
    def IsCellSelectedAt(self, index: int) -> bool:
        """
        このノードで指定されたインデックスのセルが選択されているか調べます。

        Args:
            index (int): 列インデックス（0以上、列数未満）

        """
        ...
    def HasCellValue(self, column: ITreeGridColumn) -> bool:
        """
        このノードで指定された列のセルの値が存在するか調べます。

        Args:
            column (ITreeGridColumn): 列情報

        Returns:
            bool: セルの値が存在する場合は真
        """
        ...
    def HasCellValueAt(self, index: int) -> bool:
        """
        このノードで指定された列のセルの値が存在するか調べます。

        Args:
            index (int): 列インデックス（0以上、列数未満）

        """
        ...
    def GetCellValue(self, column: ITreeGridColumn) -> Any:
        """
        このノードで指定された列のセルの値を取得します。
        セルの値が存在しない場合はnullを返します。

        Args:
            column (ITreeGridColumn): 列情報

        """
        ...
    def GetCellValueAt(self, index: int) -> Any:
        """
        このノードで指定されたインデックスのセルの値を取得します。
        セルの値が存在しない場合はnullを返します。

        Args:
            index (int): 列インデックス（0以上、列数未満）

        """
        ...
    def GetCellValueString(self, column: ITreeGridColumn) -> str:
        """
        このノードで指定された列のセルの値を文字列形式で取得します。
        セルの値が存在しない場合は空の文字列を返します。

        Args:
            column (ITreeGridColumn): 列情報

        """
        ...
    def GetCellValueStringAt(self, index: int) -> str:
        """
        このノードで指定されたインデックスのセルの値を文字列形式で取得します。
        セルの値が存在しない場合は空の文字列を返します。

        Args:
            index (int): 列インデックス（0以上、列数未満）

        """
        ...
    def GetCellDisplayValues(self) -> List[str]:
        """
        このノードのすべてのセル表示文字列を取得します。
        値が存在しないセルは空の文字列を返します。

        """
        ...
    def GetSelectedCells(self) -> ITreeGridCellCollection:
        """
        このノードで選択されているセルを取得します。

        Returns:
            ITreeGridCellCollection: 選択されているセル
        """
        ...
    @property
    def Parent(self) -> ITreeGridNode:
        """ツリーの親ノード"""
        ...
    @property
    def Children(self) -> ITreeGridNodeCollection:
        """ツリーの子ノード"""
        ...
    @property
    def IsExpanded(self) -> bool:
        """このノードが展開されているか"""
        ...
    @property
    def Cells(self) -> ITreeGridCellCollection:
        """このノードのセル"""
        ...

class ITreeGridNodeCollection:
    """
    ツリーグリッドのノード情報のコレクションです。
    """
    def GetItem(self, index: int) -> ITreeGridNode:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITreeGridNode: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITreeGridNodeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITreeGridNodeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITreeGridNode]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITreeGridNodeEnumerator:
    """
    ツリーグリッドのノード情報のコレクションの列挙子です。
    """
    ...

class PortOrientation(IntFlag):
    """
    ポート位置の列挙
    （[Flag] 値）
    """
    Top = 1  # 上側
    Bottom = 2  # 下側
    Left = 4  # 左側
    Right = 8  # 右側
    All = 15  # 全て

class IModel(IObject):
    """
    モデル情報へのアクセスオブジェクトを表します。
    """
    @overload
    def Is(self, className: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したクラスのインスタンスであるか調べます。

        Args:
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラスのインスタンスの場合は true、それ以外は false。
        """
        ...
    @overload
    def Is(self, scope: IPackage, className: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したクラスのインスタンスであるか調べます。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラスのインスタンスの場合は true、それ以外は false。
        """
        ...
    @overload
    def Is(self, targetClass: IClass) -> bool:
        """
        このインスタンスが指定したクラスのインスタンスであるか調べます。

        Args:
            targetClass (IClass): クラス。

        Returns:
            bool: 指定したクラスのインスタンスの場合は true、それ以外は false。
        """
        ...
    @overload
    def IsIn(self, classNames: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したいずれかのクラスのインスタンスであるか調べます。

        Args:
            classNames (str): クラス名（複数のクラスを指定する場合はカンマ区切り）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラスのインスタンスの場合は true、それ以外は false。
        """
        ...
    @overload
    def IsIn(self, scope: IPackage, classNames: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したいずれかのクラスのインスタンスであるか調べます。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            classNames (str): クラス名（複数のクラスを指定する場合はカンマ区切り）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラスのインスタンスの場合は true、それ以外は false。
        """
        ...
    @overload
    def IsIn(self, classNames: Iterable[str], fuzzy: bool) -> bool: ...
    @overload
    def IsIn(self, scope: IPackage, classNames: Iterable[str], fuzzy: bool) -> bool: ...
    @overload
    def IsIn(self, targetClasses: Iterable[IClass]) -> bool: ...
    @overload
    def As(self, className: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したクラス型と互換するか調べます。

        Args:
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラス型と互換する場合は true、それ以外は false。
        """
        ...
    @overload
    def As(self, scope: IPackage, className: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したクラス型と互換するか調べます。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラス型と互換する場合は true、それ以外は false。
        """
        ...
    @overload
    def As(self, targetClass: IClass) -> bool:
        """
        このインスタンスが指定したクラス型と互換するか調べます。

        Args:
            targetClass (IClass): クラス。

        Returns:
            bool: 指定したクラス型と互換する場合は true、それ以外は false。
        """
        ...
    @overload
    def AsIn(self, classNames: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したいずれかのクラス型と互換するか調べます。

        Args:
            classNames (str): クラス名（複数のクラスを指定する場合はカンマ区切り）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラス型と互換する場合は true、それ以外は false。
        """
        ...
    @overload
    def AsIn(self, scope: IPackage, classNames: str, fuzzy: bool) -> bool:
        """
        このインスタンスが指定したいずれかのクラス型と互換するか調べます。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            classNames (str): クラス名（複数のクラスを指定する場合はカンマ区切り）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            bool: 指定したクラス型と互換する場合は true、それ以外は false。
        """
        ...
    @overload
    def AsIn(self, classNames: Iterable[str], fuzzy: bool) -> bool: ...
    @overload
    def AsIn(self, scope: IPackage, classNames: Iterable[str], fuzzy: bool) -> bool: ...
    @overload
    def AsIn(self, targetClasses: Iterable[IClass]) -> bool: ...
    def GetReferenceFieldsOf(self, model: IModel) -> IFieldCollection:
        """
        このインスタンスのクラスが持つ参照フィールドのうち、指定したモデルを格納可能な型の参照フィールドを取得します。

        Args:
            model (IModel): モデル。

        Returns:
            IFieldCollection: モデル型のフィールド一覧。
        """
        ...
    def GetRelatableFieldsOf(self, model: IModel) -> IFieldCollection:
        """
        このインスタンスと指定したモデルを関連づけることができる参照フィールドを取得します。

        Args:
            model (IModel): モデル。

        Returns:
            IFieldCollection: 関連づけ可能なフィールド一覧。
        """
        ...
    def GetRelatingFieldsOf(self, model: IModel) -> IFieldCollection:
        """
        このインスタンスのクラスが持つ全てのフィールドのうち、指定したモデルをフィールド値として格納するものを取得します。

        Args:
            model (IModel): 対象モデル。

        Returns:
            IFieldCollection: 関連づけられたフィールド一覧。
        """
        ...
    def GetOwners(self) -> IModelCollection:
        """
        このインスタンスに対して所有関係で探索できる全ての所有元インスタンスを取得します。

        Returns:
            IModelCollection: 所有元インスタンス。
        """
        ...
    @overload
    def FindOwnerByClass(self, className: str, fuzzy: bool) -> IModel:
        """
        このインスタンスを保持する指定クラスの最初の所有元インスタンスを取得します。
        このインスタンスを所有するインスタンスを親方向へ辿り、最初に見つかった指定クラスのインスタンスを返します。
        最上位の親要素まで探索しても、該当するインスタンスが見つからなかった場合は null を返します。
        なお、クラス名に指定したクラスが見つからない場合はnullを返します。
        また、あいまい一致とするときに、一致するクラスが複数ある場合、一番最初に見つかったクラスのインスタンスを返します。

        Args:
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModel: 所有元インスタンス。
        """
        ...
    @overload
    def FindOwnerByClass(self, scope: IPackage, className: str, fuzzy: bool) -> IModel:
        """
        このインスタンスを保持する指定クラスの最初の所有元インスタンスを取得します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。
        このインスタンスを所有するインスタンスを親方向へ辿り、最初に見つかった指定クラスのインスタンスを返します。
        最上位の親要素まで探索しても、該当するインスタンスが見つからなかった場合は null を返します。
        なお、クラス名に指定したクラスが見つからない場合はnullを返します。
        また、あいまい一致とするときに、一致するクラスが複数ある場合、一番最初に見つかったクラスのインスタンスを返します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModel: 所有元インスタンス。
        """
        ...
    @overload
    def FindOwnerByClass(self, targetClass: IClass) -> IModel:
        """
        このインスタンスを保持する指定クラスの最初の所有元インスタンスを取得します。
        このインスタンスを所有するインスタンスを親方向へ辿り、最初に見つかった指定クラスのインスタンスを返します。
        最上位の親要素まで探索しても、該当するインスタンスが見つからなかった場合は null を返します。

        Args:
            targetClass (IClass): クラス。

        Returns:
            IModel: 所有元インスタンス。
        """
        ...
    def GetOwnerRelationship(self) -> IRelationship:
        """
        このモデルの所有元モデルとの関連を取得します。
        このモデルの所有元モデルが存在しない場合は null を返します。

        Returns:
            IRelationship: 所有元モデルとの関連
        """
        ...
    def GetOwnerField(self) -> IField:
        """
        このモデルの所有元モデルがこのモデルを保持するフィールドを取得します。
        このモデルの所有元モデルが存在しない場合は null を返します。

        Returns:
            IField: 所有元モデルがこのモデルを保持するフィールド
        """
        ...
    def GetChildren(self) -> IModelCollection:
        """
        このインスタンスの直接の所有関係にあるインスタンスを取得します。

        Returns:
            IModelCollection: 直接の所有関係にあるインスタンス。
        """
        ...
    def GetAllChildren(self) -> IModelCollection:
        """
        このインスタンスから所有関係の深さ優先探索で探索できるすべてのインスタンスを取得します。

        Returns:
            IModelCollection: このインスタンスを基点として所有関係にあるすべてのインスタンス。
        """
        ...
    def FindChildrenByTag(self, tag: str, value: str, recursive: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定したタグが付与されたインスタンスを取得します。

        Args:
            tag (str): モデルのタグ名。
            value (str): タグ値。
            recursive (bool): 所有関係を再帰的に探索するか。

        Returns:
            IModelCollection: 所有関係にある指定されたタグが付与されたインスタンスの一覧。
        """
        ...
    @overload
    def FindChildrenByClass(self, className: str, recursive: bool, fuzzy: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定したクラスのインスタンスを検索します。

        Args:
            className (str): クラス名。
            recursive (bool): 所有関係を再帰的に探索するか。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 所有関係にある指定されたクラスのインスタンス。
        """
        ...
    @overload
    def FindChildrenByClass(self, scope: IPackage, className: str, recursive: bool, fuzzy: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定したクラスのインスタンスを検索します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            recursive (bool): 所有関係を再帰的に探索するか。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 所有関係にある指定されたクラスのインスタンス。
        """
        ...
    @overload
    def FindChildrenByClass(self, targetClass: IClass, recursive: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定したクラスのインスタンスを検索します。

        Args:
            targetClass (IClass): クラス。
            recursive (bool): 所有関係を再帰的に探索するか。

        Returns:
            IModelCollection: 所有関係にある指定されたクラスのインスタンス。
        """
        ...
    def FindChildrenByClassDisplayName(self, classDisplayName: str, recursive: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定した表示名をもつクラスのインスタンスを検索します。

        Args:
            classDisplayName (str): クラス表示名。
            recursive (bool): 所有関係を再帰的に探索するか。

        Returns:
            IModelCollection: 所有関係にある指定された表示名のクラスのインスタンス。
        """
        ...
    def FindChildrenByClassTag(self, classTag: str, value: str, recursive: bool) -> IModelCollection:
        """
        このインスタンスの所有関係にあるインスタンスのうち指定したタグが付与されたクラスのインスタンスを取得します

        Args:
            classTag (str): クラスのタグ名。
            value (str): タグ値。
            recursive (bool): 所有関係を再帰的に探索するか。

        Returns:
            IModelCollection: 所有関係にある指定されたタグが付与されたクラスのインスタンスの一覧。
        """
        ...
    @overload
    def GetRefRelatedModels(self, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスと参照関係にあるインスタンスを取得します。

        Args:
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 参照関係にあるインスタンス。
        """
        ...
    @overload
    def GetRefRelatedModels(self, scope: IPackage, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスと参照関係にあるインスタンスを取得します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 参照関係にあるインスタンス。
        """
        ...
    @overload
    def GetRefRelatedModels(self, targetClass: IRelationshipClass) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスと参照関係にあるインスタンスを取得します。

        Args:
            targetClass (IRelationshipClass): 関連クラス。

        Returns:
            IModelCollection: 参照関係にあるインスタンス。
        """
        ...
    @overload
    def GetDerivedModels(self, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスから導出したインスタンスを取得します。

        Args:
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 導出したインスタンス。
        """
        ...
    @overload
    def GetDerivedModels(self, scope: IPackage, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスから導出したインスタンスを取得します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 導出したインスタンス。
        """
        ...
    @overload
    def GetDerivedModels(self, targetClass: IRelationshipClass) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスから導出したインスタンスを取得します。

        Args:
            targetClass (IRelationshipClass): 関連クラス。

        Returns:
            IModelCollection: 導出したインスタンス。
        """
        ...
    @overload
    def GetDerivingModels(self, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスの導出元インスタンスを取得します。

        Args:
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 導出元のインスタンス。
        """
        ...
    @overload
    def GetDerivingModels(self, scope: IPackage, className: str, fuzzy: bool) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスの導出元インスタンスを取得します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): 関連クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModelCollection: 導出元のインスタンス。
        """
        ...
    @overload
    def GetDerivingModels(self, targetClass: IRelationshipClass) -> IModelCollection:
        """
        指定した関連クラスにより、このインスタンスの導出元インスタンスを取得します。

        Args:
            targetClass (IRelationshipClass): 関連クラス。

        Returns:
            IModelCollection: 導出元のインスタンス。
        """
        ...
    def FindRelatableModels(self, fieldName: str, scope: IModel) -> IModelCollection:
        """
        このモデルと指定した参照フィールドで関連付けできるモデルを取得します。
        探索範囲の基点モデルが未指定の場合は、プロジェクト全体から探索します。
        探索範囲の基点モデルを指定した場合は、そのモデル要素以下のモデルから関連付け可能なモデルを探索します。
        この場合、取得結果のモデルには関連は含まれません。関連を参照するフィールドの場合は、探索範囲の基点モデルを未指定で呼び出してください。
        なお、指定したフィールドが参照フィールドでない場合は空のコレクションを返します。

        Args:
            fieldName (str): 関連付け対象のフィールド名。null、または空文字列は指定できません。
            scope (IModel): 探索範囲の基点となるモデル。未指定の場合は、プロジェクト全体から探索します。

        Returns:
            IModelCollection: 関連付けできるモデルの一覧。
        """
        ...
    def Count(self, fieldName: str) -> int:
        """
        指定したフィールドの値件数を取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            int: 値件数。
        """
        ...
    @overload
    def GetField(self, fieldName: str) -> Any:
        """
        このインスタンスの指定したフィールドの値を取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            Any: フィールドの値。
        """
        ...
    @overload
    def GetField(self, field: IField) -> Any:
        """
        このインスタンスの指定したフィールドの値を取得します。

        Args:
            field (IField): フィールド。

        Returns:
            Any: フィールドの値。
        """
        ...
    @overload
    def GetFieldAt(self, fieldName: str, index: int) -> Any:
        """
        このインスタンスの指定したフィールドの指定したインデックス位置の値を取得します。

        Args:
            fieldName (str): フィールド名。
            index (int): 位置。

        Returns:
            Any: フィールドの値。
        """
        ...
    @overload
    def GetFieldAt(self, field: IField, index: int) -> Any:
        """
        このインスタンスの指定したフィールドの指定したインデックス位置の値を取得します。

        Args:
            field (IField): フィールド。
            index (int): 位置。

        Returns:
            Any: フィールドの値。
        """
        ...
    def GetFieldString(self, fieldName: str) -> str:
        """
        指定したフィールドの値を文字列形式で取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            str: フィールドの値の文字列表現。
        """
        ...
    def GetFieldStringAt(self, fieldName: str, index: int) -> str:
        """
        指定したフィールドの値を文字列形式で取得します。

        Args:
            fieldName (str): フィールド名。
            index (int): 位置。

        Returns:
            str: フィールドの値の文字列表現。
        """
        ...
    def GetFieldValues(self, fieldName: str) -> IModelCollection:
        """
        指定したフィールドの値コレクションを取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IModelCollection: フィールドの値。
        """
        ...
    def GetFieldValuesByFieldTag(self, fieldTag: str, value: str) -> Iterable[Any]:
        """
        指定したタグが付与されたフィールド値の列挙を取得します。
        指定したタグが付与されたフィールドが複数ある場合はそのすべてのフィールド値を返します。

        Args:
            fieldTag (str): フィールドのタグ名。
            value (str): タグ値。

        Returns:
            Iterable[Any]: フィールド値の列挙。
        """
        ...
    @overload
    def SetField(self, fieldName: str, value: Any) -> None:
        """
        このインスタンスの指定したフィールドに、指定した値を設定します。

        Args:
            fieldName (str): フィールド名。
            value (Any): フィールドの値。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetField(self, field: IField, value: Any) -> None:
        """
        このインスタンスの指定したフィールドに、指定した値を設定します。

        Args:
            field (IField): フィールド。
            value (Any): フィールドの値。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetFieldAt(self, fieldName: str, value: Any, index: int) -> None:
        """
        このインスタンスの指定したフィールドの指定したインデックス位置に、指定した値を設定します。

        Args:
            fieldName (str): フィールド名。
            value (Any): フィールドの値。
            index (int): 位置。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetFieldAt(self, field: IField, value: Any, index: int) -> None:
        """
        このインスタンスの指定したフィールドの指定したインデックス位置に、指定した値を設定します。

        Args:
            field (IField): フィールド。
            value (Any): フィールドの値。
            index (int): 位置。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetInitField(self, fieldName: str) -> None:
        """
        このインスタンスの指定したフィールドの値をクリアして初期値に設定します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddNewModel(self, fieldName: str, className: str, fuzzy: bool) -> IModel:
        """
        このインスタンスの指定したフィールドに指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            fieldName (str): フィールド名。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    @overload
    def AddNewModel(self, field: IField, classToAdd: IClass) -> IModel:
        """
        このインスタンスの指定したフィールドに指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            field (IField): フィールド。
            classToAdd (IClass): クラス。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    @overload
    def AddNewModelAt(self, fieldName: str, className: str, direction: str, index: int, fuzzy: bool) -> IModel:
        """
        このインスタンスの指定したフィールドに、追加位置を指定して指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            fieldName (str): フィールド名。
            className (str): クラス名。
            direction (str): 方向（before | after）。
            index (int): 追加位置。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    @overload
    def AddNewModelAt(self, field: IField, classToAdd: IClass, direction: str, index: int) -> IModel:
        """
        このインスタンスの指定したフィールドに、追加位置を指定して指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            field (IField): フィールド。
            classToAdd (IClass): クラス。
            direction (str): 方向（before | after）。
            index (int): 追加位置。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    @overload
    def AddNewModelTo(self, fieldName: str, className: str, direction: str, target: IModel, fuzzy: bool) -> IModel:
        """
        このインスタンスの指定したフィールドに、追加位置を指定して指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            fieldName (str): フィールド名。
            className (str): クラス名。
            direction (str): 方向（before | after）。
            target (IModel): 追加位置のモデル。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    @overload
    def AddNewModelTo(self, field: IField, classToAdd: IClass, direction: str, target: IModel) -> IModel:
        """
        このインスタンスの指定したフィールドに、追加位置を指定して指定したクラスのインスタンスをフィールド値として追加します。

        Args:
            field (IField): フィールド。
            classToAdd (IClass): クラス。
            direction (str): 方向（before | after）。
            target (IModel): 追加位置のモデル。

        Returns:
            IModel: 追加したモデル。
        """
        ...
    def RemoveField(self, fieldName: str, value: IModel) -> None:
        """
        このインスタンスの指定したフィールドの値を削除します。

        Args:
            fieldName (str): フィールド名。
            value (IModel): フィールドの値。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveFieldAt(self, fieldName: str, index: int) -> None:
        """
        このインスタンスの指定した位置のフィールド値を削除します。

        Args:
            fieldName (str): フィールド名。
            index (int): 位置。

        Returns:
            None: This method does not return a value.
        """
        ...
    def MoveTo(self, newOwner: IModel, fieldName: str, direction: str, index: int) -> None:
        """
        このインスタンスを指定したモデルの子要素となるように移動します。
        移動先の親要素、およびフィールドが、現在の親要素、およびフィールドと同一の場合は、指定フィールドにおける要素の順序を変更します。

        Args:
            newOwner (IModel): 移動先（新しい親）。
            fieldName (str): 移動先のフィールド名。
            direction (str): 方向（first| last| before | after）。
            index (int): 位置。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Take(self, fieldName: str, target: IModel, direction: str, index: int) -> None:
        """
        このインスタンスの指定したフィールドへ指定したモデルを移動します。
        移動対象のモデルの親要素がこのインスタンスとなります。

        Args:
            fieldName (str): 移動先のフィールド名。
            target (IModel): 移動するモデル（新しい子）。
            direction (str): 方向（first| last| before | after）。
            index (int): 位置。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CanRelate(self, fieldName: str, opposite: IModel) -> bool:
        """
        このインスタンスの指定したフィールドで与えられたモデルと関連づけできるか調べます。
        このメソッドでは、フィールドの型だけでなく、以下のフィールド制約についても評価します。
        [評価する制約]
        - パス制約
        - 型制約
        - 多重度上限

        Args:
            fieldName (str): フィールド名。
            opposite (IModel): 関連付けるモデル。

        Returns:
            bool: 関連づけできる場合は真。
        """
        ...
    def CanRelateAny(self, opposite: IModel) -> bool:
        """
        このインスタンスを与えられたモデルと関連づけできるか調べます。
        このインスタンスのいずれかのフィールドで関連づけることができる場合は真を返します。

        Args:
            opposite (IModel): 関連付けるモデル。

        Returns:
            bool: 関連づけできる場合は真。
        """
        ...
    def Relate(self, fieldName: str, opposite: IModel) -> IRelationship:
        """
        このインスタンスの指定したフィールドの末尾で指定したモデルを関連づけて、
        追加した関連インスタンスを返します。

        Args:
            fieldName (str): フィールド名。
            opposite (IModel): 関連付けるモデル。

        Returns:
            IRelationship: 追加したモデル。
        """
        ...
    def RelateAt(self, fieldName: str, opposite: IModel, direction: str, index: int) -> IRelationship:
        """
        このインスタンスの指定したフィールドで、追加位置を指定して指定したモデルを関連づけて、
        追加した関連インスタンスを返します。

        Args:
            fieldName (str): フィールド名。
            opposite (IModel): 関連付けるモデル。
            direction (str): 方向（before | after）。
            index (int): 追加位置。

        Returns:
            IRelationship: 追加したモデル。
        """
        ...
    def RelateWhere(self, opposite: IModel, predicate: Callable) -> IRelationshipCollection: ...
    def RelateAll(self, opposite: IModel) -> IRelationshipCollection:
        """
        このインスタンスの指定したモデルと関連付けが可能な全ての参照フィールドで指定したモデルを関連づけて、
        追加したすべての関連インスタンスのコレクションを返します。
        このメソッドでは、次の制約を満たさないフィールドは関連付け対象から除外されます。
        [評価する制約]
        - パス制約
        - 型制約
        - 多重度上限

        Args:
            opposite (IModel): 関連付けるモデル。

        Returns:
            IRelationshipCollection: 追加した関連一覧。
        """
        ...
    def RelateAllDerivedFrom(self, opposite: IModel) -> IRelationshipCollection:
        """
        このインスタンスの指定したモデルを導出元として関連付けが可能な全てのフィールドで指定したモデルを導出元として関連づけて、
        追加したすべての関連インスタンスのコレクションを返します。
        このメソッドでは、次の制約を満たさないフィールドは関連付け対象から除外されます。
        [評価する制約]
        - パス制約
        - 型制約
        - 多重度上限

        Args:
            opposite (IModel): 関連付けるモデル。

        Returns:
            IRelationshipCollection: 追加した関連一覧。
        """
        ...
    def RelateAllDerivedTo(self, opposite: IModel) -> IRelationshipCollection:
        """
        このインスタンスの指定したモデルを導出先として関連付けが可能な全てのフィールドで指定したモデルを導出先として関連づけて、
        追加したすべての関連インスタンスのコレクションを返します。
        このメソッドでは、次の制約を満たさないフィールドは関連付け対象から除外されます。
        [評価する制約]
        - パス制約
        - 型制約
        - 多重度上限

        Args:
            opposite (IModel): 関連付けるモデル。

        Returns:
            IRelationshipCollection: 追加した関連一覧。
        """
        ...
    def RelateByFieldTag(self, opposite: IModel, fieldTag: str, value: str) -> IRelationshipCollection:
        """
        このインスタンスの指定したタグが付与された参照フィールドで指定したモデルを関連づけて、
        追加したすべての関連インスタンスのコレクションを返します。
        ただし、以下の条件に該当するフィールドへの関連づけは行われず正常終了します。
        ・フィールドの型が与えられたモデルと互換しない場合
        ・フィールドの多重度を超える場合

        Args:
            opposite (IModel): 関連付けるモデル。
            fieldTag (str): フィールドのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 追加した関連一覧。
        """
        ...
    def RelateByClassTag(self, opposite: IModel, classTag: str, value: str) -> IRelationshipCollection:
        """
        このインスタンスの指定したタグが付与された関連クラスによって関連づけ可能な参照フィールドで指定したモデルを関連づけて、
        追加したすべての関連インスタンスのコレクションを返します。
        ただし、以下の条件に該当するフィールドへの関連づけは行われず正常終了します。
        ・フィールドの型が与えられたモデルと互換しない場合
        ・フィールドの多重度を超える場合

        Args:
            opposite (IModel): 関連付けるモデル。
            classTag (str): 関連クラスのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 追加した関連一覧。
        """
        ...
    def UnRelate(self, fieldName: str, opposite: IModel) -> None:
        """
        このインスタンスの指定したフィールドで指定したモデルとの参照関連づけを解除します。
        該当フィールドにおいて、複数の関連づけがある場合は、そのすべての関連付けを解除します。
        また、指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。

        Args:
            fieldName (str): フィールド名。
            opposite (IModel): 関連づけを解除するモデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateWhere(self, opposite: IModel, predicate: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateAll(self, opposite: IModel) -> None:
        """
        このインスタンスの指定したモデルとの全ての参照関連づけを解除します。
        指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。
        また、以下の条件に該当するフィールドへの関連づけも解除されず正常終了します。
        ・プロダクトラインサポート向けフィールドでの関連付け

        Args:
            opposite (IModel): 関連づけを解除するモデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateAllDerivedFrom(self, opposite: IModel) -> None:
        """
        このインスタンスの指定したモデルを導出元とする全ての関連づけを解除します。
        指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。

        Args:
            opposite (IModel): 関連づけを解除するモデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateAllDerivedTo(self, opposite: IModel) -> None:
        """
        このインスタンスの指定したモデルを導出先とする全ての関連づけを解除します。
        指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。

        Args:
            opposite (IModel): 関連づけを解除するモデル。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateByFieldTag(self, opposite: IModel, fieldTag: str, value: str) -> None:
        """
        このインスタンスの指定したタグが付与された参照フィールドで指定したモデルとの関連づけを解除します。
        指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。

        Args:
            opposite (IModel): 関連づけを解除するモデル。
            fieldTag (str): フィールドのタグ名。
            value (str): タグ値。

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnRelateByClassTag(self, opposite: IModel, classTag: str, value: str) -> None:
        """
        このインスタンスの指定したタグが付与された関連クラスによって関連づけ可能な参照フィールドで指定したモデルとの関連づけを解除します。
        指定したモデルとの関連が存在しなかった場合は、何も行われず正常終了します。

        Args:
            opposite (IModel): 関連づけを解除するモデル。
            classTag (str): 関連クラスのタグ名。
            value (str): タグ値。

        Returns:
            None: This method does not return a value.
        """
        ...
    def IsRelatedTo(self, model: IModel) -> bool:
        """
        このインスタンスが指定したモデルと参照関連を持つか調べます。

        Args:
            model (IModel): モデル。

        Returns:
            bool: 参照関連を持つ場合は真。
        """
        ...
    def IsRelatedAtFieldTo(self, fieldName: str, model: IModel) -> bool:
        """
        このインスタンスが指定したフィールドで指定したモデルと参照関連を持つか調べます。

        Args:
            fieldName (str): フィールド名。
            model (IModel): モデル。

        Returns:
            bool: 参照関連を持つ場合は真。
        """
        ...
    def GetRelation(self, fieldName: str) -> IRelationship:
        """
        指定したフィールドの関連を取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IRelationship: 関連。
        """
        ...
    def GetRelationAt(self, fieldName: str, index: int) -> IRelationship:
        """
        指定したフィールドの指定位置の関連を取得します。

        Args:
            fieldName (str): フィールド名。
            index (int): 位置。

        Returns:
            IRelationship: 関連。
        """
        ...
    def GetRelations(self, fieldName: str) -> IRelationshipCollection:
        """
        指定したフィールドの関連コレクションを取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsOf(self, opposite: IModel) -> IRelationshipCollection:
        """
        指定したモデルとの全ての関連を取得します。

        Args:
            opposite (IModel): 相手側モデル。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsByFieldOf(self, fieldName: str, opposite: IModel) -> IRelationshipCollection:
        """
        指定したフィールドにおける指定したモデルとの関連を取得します。

        Args:
            fieldName (str): フィールド名。
            opposite (IModel): 相手側モデル。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsByTag(self, fieldName: str, tag: str, value: str) -> IRelationshipCollection:
        """
        指定したフィールドにおける指定したタグが付与された関連を取得します。

        Args:
            fieldName (str): フィールド名。
            tag (str): 関連に付与されているタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 指定されたタグが付与された関連の一覧。
        """
        ...
    def GetRelationsByClassTag(self, classTag: str, value: str) -> IRelationshipCollection:
        """
        このモデルのすべてのフィールドから指定したタグが付与された関連クラスのインスタンスを取得します。

        Args:
            classTag (str): クラスのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 指定されたタグが付与された関連クラスの一覧。
        """
        ...
    def GetRelationsByFieldTag(self, fieldTag: str, value: str) -> IRelationshipCollection:
        """
        指定したタグが付与されたフィールドの関連を取得します。

        Args:
            fieldTag (str): フィールドのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 指定されたタグが付与されたフィールドの関連の一覧。
        """
        ...
    def GetDeriveRelationsOf(self, opposite: IModel) -> IRelationshipCollection:
        """
        指定したモデルとの全ての導出関連を取得します。

        Args:
            opposite (IModel): 相手側モデル。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetDerivedFromRelationsOf(self, opposite: IModel) -> IRelationshipCollection:
        """
        このモデルが指定したモデルから導出した要素であった場合、その全ての導出関連を取得します。
        例えば、このモデルが{要素A}から導出した要素であった場合に、引数に{要素A}を指定することで、その導出関連を取得することができます。

        Args:
            opposite (IModel): 相手側モデル。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetDerivedToRelationsOf(self, opposite: IModel) -> IRelationshipCollection:
        """
        指定したモデルが、このモデルから導出した要素であった場合、その全ての導出関連を取得します。
        例えば、このモデルから導出した{要素B}があった場合に、引数に{要素B}を指定することで、その導出関連を取得することができます。

        Args:
            opposite (IModel): 相手側モデル。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsByFieldTagOf(self, opposite: IModel, fieldTag: str, value: str) -> IRelationshipCollection:
        """
        指定したタグが付与されたフィールドから、指定したモデルとの関連を取得します。

        Args:
            opposite (IModel): 相手側モデル。
            fieldTag (str): フィールドのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsByClassTagOf(self, opposite: IModel, classTag: str, value: str) -> IRelationshipCollection:
        """
        このモデルのすべてのフィールドから指定したタグが付与された関連クラスによって関連づけられた指定したモデルとの関連を取得します。

        Args:
            opposite (IModel): 相手側モデル。
            classTag (str): 関連クラスのタグ名。
            value (str): タグ値。

        Returns:
            IRelationshipCollection: 関連の一覧。
        """
        ...
    def GetRelationsWhere(self, predicate: Callable) -> IRelationshipCollection: ...
    def GetRelationsOfWhere(self, opposite: IModel, predicate: Callable) -> IRelationshipCollection: ...
    @overload
    def SetRichTextField(self, fieldName: str, value: str) -> None:
        """
        指定したリッチテキストフィールドにテキスト値を設定します。

        Args:
            fieldName (str): フィールド名。
            value (str): フィールドのテキスト値。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetRichTextField(self, fieldName: str, value: str, format: str) -> None:
        """
        指定したリッチテキストフィールドのフォーマットに値を設定します。

        Args:
            fieldName (str): フィールド名。
            value (str): フィールドの値。
            format (str): フォーマット(text| html| xaml)、大文字小文字は区別しません。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SetRichTextField(self, fieldName: str, value: str, textValue: str, format: str) -> None:
        """
        指定したリッチテキストフィールドのフォーマットに値を設定し、同時にテキスト値も設定します。

        Args:
            fieldName (str): フィールド名。
            value (str): フィールドの値。
            textValue (str): フィールドのテキスト値。
            format (str): フォーマット(html| xaml)、大文字小文字は区別しません。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetRichTextFieldValues(self, fieldName: str, htmlValue: str, textValue: str) -> None:
        """
        指定したリッチテキストフィールドにHtml値とテキスト値を設定します。

        Args:
            fieldName (str): フィールド名。
            htmlValue (str): フィールドのHtml値。
            textValue (str): フィールドのテキスト値。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetRichTextField(self, fieldName: str, format: str) -> str:
        """
        指定したリッチテキストフィールドのフォーマットの値を取得します。
        指定したフォーマットが見つからない場合はnullを返します。

        Args:
            fieldName (str): フィールド名。
            format (str): フォーマット(text| html| xaml)、大文字小文字は区別しません。

        Returns:
            str: 指定したリッチテキストフィールドのフォーマットの値。
        """
        ...
    def GetRichTextFieldFormats(self, fieldName: str) -> Iterable[str]:
        """
        指定したリッチテキストフィールドの値が設定されているフォーマットの一覧を取得します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            Iterable[str]: 指定したリッチテキストフィールドの値が設定されているフォーマットの一覧。
        """
        ...
    def SetRichTextFieldCustomData(self, fieldName: str, value: str, format: str) -> None:
        """
        指定したリッチテキストフィールドのカスタムフォーマットに値を設定します。

        Args:
            fieldName (str): フィールド名。
            value (str): カスタムデータの値、nullの場合は指定したフォーマットのデータを削除します。
            format (str): カスタムフォーマット名、大文字小文字は区別しません。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetRichTextFieldCustomData(self, fieldName: str, format: str) -> str:
        """
        指定したリッチテキストフィールドのカスタムフォーマットの値を取得します。
        指定したフォーマットが見つからない場合はnullを返します。

        Args:
            fieldName (str): フィールド名。
            format (str): カスタムフォーマット名、大文字小文字は区別しません。

        Returns:
            str: 指定したリッチテキストフィールドのカスタムフォーマットの値。
        """
        ...
    def Delete(self) -> None:
        """
        このインスタンスを削除します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AssignFeature(self, feature: IFeature) -> None:
        """
        このモデルに指定したフィーチャを割り当てます。

        Args:
            feature (IFeature): フィーチャ。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AssignFeatures(self, features: Iterable[IFeature]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def AssignFeatureByName(self, featureName: str) -> None:
        """
        このモデルに指定した名前のフィーチャを割り当てます

        Args:
            featureName (str): フィーチャ名。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AssignFeaturesByName(self, featureNames: str) -> None:
        """
        このモデルに指定した名前のすべてのフィーチャを割り当てます

        Args:
            featureNames (str): フィーチャ名（カンマ区切りで複数指定可）。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetAssignedFeatures(self) -> IFeatureCollection:
        """
        このモデルに割り当てられているすべてのフィーチャを取得します。

        Returns:
            IFeatureCollection: すべてのフィーチャ。
        """
        ...
    def ReleaseAssignedFeature(self, feature: IFeature) -> None:
        """
        指定したフィーチャのこのモデルへの割り当てを解除します。

        Args:
            feature (IFeature): フィーチャ。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ReleaseAssignedFeatures(self, features: Iterable[IFeature]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def ReleaseAssignedFeaturesByName(self, featureNames: str) -> None:
        """
        指定した名前のフィーチャについて、このモデルへの割り当てを解除します。

        Args:
            featureNames (str): フィーチャ名（カンマ区切りで複数指定可能）。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ReleaseAssignedFeatureByName(self, featureName: str) -> None:
        """
        指定した名前のすべてのフィーチャについて、このモデルへの割り当てを解除します。

        Args:
            featureName (str): フィーチャ名。

        Returns:
            None: This method does not return a value.
        """
        ...
    def ReleaseAllAssignedFeatures(self) -> None:
        """
        このモデルに割り当てられたすべてのフィーチャとの割り当てを解除します。
        この呼び出しでフィーチャとの割り当てを解除した場合はプロダクト適用条件式も削除されます。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetProductApplyCondition(self) -> str:
        """
        このモデルのプロダクト適用条件式を取得します。

        Returns:
            str: 適用条件式。
        """
        ...
    def SetProductApplyCondition(self, expression: str) -> None:
        """
        このモデルのプロダクト適用条件式を設定します。
        なお、プロダクト適用条件式内において、このモデルに未割り当てのフィーチャ名を使用していた場合は、自動的にフィーチャが割り当てられます。
        また、条件式で、このモデルに割り当て済みのフィーチャ名が使用されなかった場合は、自動的にフィーチャとの割り当てが解除されます。
        条件式に空の文字列を指定した場合は、全てのフィーチャ割り当てが解除されます。

        Args:
            expression (str): 適用条件式。

        Returns:
            None: This method does not return a value.
        """
        ...
    def IsAppliedItem(self) -> bool:
        """
        このモデルがカレントプロダクトで有効か調べます。

        Returns:
            bool: 有効な場合は真。
        """
        ...
    def IsAppliedItemTo(self, product: IProduct) -> bool:
        """
        このモデルが指定したプロダクトで有効か調べます。

        Args:
            product (IProduct): プロダクト。

        Returns:
            bool: 有効な場合は真。
        """
        ...
    def IsAppliedItemToByName(self, productName: str) -> bool:
        """
        このモデルが指定した名前のプロダクトで有効か調べます。

        Args:
            productName (str): プロダクト名。

        """
        ...
    def AddError(self, fields: str, type: str, title: str, message: str) -> IError:
        """
        このモデルに対するエラー情報を追加します。

        Args:
            fields (str): フィールド。
            type (str): 種類(\"Information\", \"Warning\", \"Error\", \"Summary\")の4種類。
            title (str): タイトル。
            message (str): メッセージ。

        Returns:
            IError: 追加したエラー情報。
        """
        ...
    def GetAllErrorsWithChildren(self) -> IErrorCollection:
        """
        子要素も含めた全エラーの取得します。

        Returns:
            IErrorCollection: エラー情報一覧。
        """
        ...
    def RemoveError(self, target: IError) -> None:
        """
        このモデルに対して追加されているエラー情報を削除します。
        削除対象として指定されたエラー情報が、このモデルに含まれない場合は、何も行われず正常終了します。

        Args:
            target (IError): 削除するエラー情報。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Validate(self) -> None:
        """
        このモデルを検証します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Validate(self, options: ValidationOptions) -> None:
        """
        このモデルを検証します。

        Args:
            options (ValidationOptions): 検証オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CreateAsyncValidationContext(self, options: ValidationOptions) -> IAsyncValidationContext:
        """
        このモデルに対する非同期検証コンテキストを生成します。

        Args:
            options (ValidationOptions): 検証オプション。nullの場合は既定のオプション値を使用します。

        Returns:
            IAsyncValidationContext: 非同期検証コンテキスト。
        """
        ...
    def GetEditors(self) -> IEditorCollection:
        """
        このインスタンスに対応するすべてのエディタを取得します。

        Returns:
            IEditorCollection: エディタの列挙。
        """
        ...
    def GetEditor(self, editorName: str) -> IEditor:
        """
        このインスタンスに対応する指定した名前のエディタを取得します。
        該当するエディタが見つからない場合は、null を返します。

        Args:
            editorName (str): エディタ名。

        Returns:
            IEditor: エディタ。
        """
        ...
    def GetRepresentationsInEditor(self, editor: IEditor) -> IRepresentationCollection:
        """
        指定したエディタ内でこのインスタンスに対応するすべての表現情報を取得します。

        Args:
            editor (IEditor): エディタ。

        Returns:
            IRepresentationCollection: 表現情報の列挙。
        """
        ...
    def NotifyFieldChanged(self, fieldName: str) -> None:
        """
        指定したフィールドの値更新通知を発行します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetObservableFieldValues(self, fieldName: str) -> IObservableModelCollection:
        """
        指定したフィールドの要素増減を検出できるを取得します。
        これは実験的な実装です。一般の開発者は使わないでください。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IObservableModelCollection: 。
        """
        ...
    def GetObservableRelationships(self, fieldName: str) -> IObservableRelationshipCollection:
        """
        指定したフィールドの要素増減を検出できるを取得します。
        これは実験的な実装です。一般の開発者は使わないでください。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IObservableRelationshipCollection: 。
        """
        ...
    def GetChangeableMetaclasses(self) -> IClassCollection:
        """
        このモデルを変換可能なすべてのクラスを取得します。
        変換可能なクラスが存在しない場合は空のコレクションを返します。

        Returns:
            IClassCollection: 変換可能なすべてのクラス。
        """
        ...
    def CanChangeMetaclassTo(self, metaclass: IClass) -> bool:
        """
        このモデルのクラスを指定したクラスに変更できるか判定します。

        Args:
            metaclass (IClass): メタクラス。

        Returns:
            bool: 変更できる場合は true、それ以外は false です。
        """
        ...
    def ChangeMetaclassTo(self, metaclass: IClass) -> None:
        """
        このモデルのクラスを指定したクラスに変更します。

        Args:
            metaclass (IClass): メタクラス。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Name(self) -> str:
        """名前"""
        ...
    @property
    def Description(self) -> str:
        """説明"""
        ...
    @property
    def ClassName(self) -> str:
        """クラス名"""
        ...
    @property
    def Metaclass(self) -> IClass:
        """クラス"""
        ...
    @property
    def Owner(self) -> IModel:
        """このインスタンスを直接所有するインスタンス"""
        ...
    @property
    def OwnerProject(self) -> IProject:
        """このインスタンスを保持するプロジェクト"""
        ...
    @property
    def ModelPath(self) -> str:
        """このインスタンスのモデル階層パス"""
        ...
    @property
    def IsEditable(self) -> bool:
        """このインスタンスが編集可能か"""
        ...
    @property
    def HasError(self) -> bool:
        """このモデルにエラーがあるか"""
        ...
    @property
    def HasErrorWithChildren(self) -> bool:
        """Embedの子要素も含めてエラーがあるか"""
        ...
    @property
    def Errors(self) -> IErrorCollection:
        """このモデルのエラー"""
        ...
    @property
    def IsProxy(self) -> bool:
        """このインスタンスがプロキシ要素か"""
        ...
    @property
    def ModelUnit(self) -> IModelUnit:
        """このモデルを管理するユニット（物理ファイル）情報"""
        ...
    @property
    def IsUnitTopModel(self) -> bool:
        """このモデルがユニットの基点モデルであるか"""
        ...
    @property
    def IsDeleted(self) -> bool:
        """このモデルが削除済みであるか調べます。"""
        ...
    @property
    def IsDeleting(self) -> bool:
        """このモデルが削除中であるか調べます。"""
        ...
    @property
    def IsDirty(self) -> bool:
        """このモデルがダーティー状態であるか調べます。"""
        ...
    @property
    def IsProductLineElement(self) -> bool:
        """このモデルがプロダクトラインのモデルであるか調べます。"""
        ...

class IInteractionElement(IModel):
    """
    相互作用モデル要素情報へのアクセスオブジェクトを表します。
    相互作用を表現する要素に共通の特性です。
    """
    @property
    def Interaction(self) -> IInteraction:
        """この要素の所有者となる相互作用モデルを取得します。"""
        ...

class IDestruction(IInteractionElement):
    """
    破棄情報へのアクセスオブジェクトを表します。
    """
    @property
    def Lifeline(self) -> ILifeline:
        """この破棄を保持するライフライン"""
        ...
    @property
    def DestroyMessage(self) -> IMessage:
        """対応する破棄メッセージを取得します。
この破棄が破棄メッセージに起点に追加された場合に該当するメッセージを返します。
破棄メッセージを起点としない場合は null を返します。"""
        ...

class IMessageSender:
    """
    メッセージの送信元として指定することができる要素であることを表します。
    """
    ...

class IMessageReceiver:
    """
    メッセージの受信先として指定することができる要素であることを表します。
    """
    ...

class IMessagePort(IMessageSender, IMessageReceiver):
    """
    メッセージの接続先要素であることを表します。
    """
    @property
    def SendMessages(self) -> IMessageCollection:
        """送信メッセージの一覧"""
        ...
    @property
    def ReceiveMessages(self) -> IMessageCollection:
        """受信メッセージの一覧"""
        ...

class IExecutionSpecification(IInteractionElement, IMessagePort):
    """
    実行仕様情報へのアクセスオブジェクトを表します。
    """
    @property
    def Lifeline(self) -> ILifeline:
        """この実行仕様を保持するライフライン"""
        ...
    @property
    def IsInitialization(self) -> bool:
        """この実行仕様が初期化区間であるか"""
        ...
    @property
    def IsDestruction(self) -> bool:
        """この実行仕様が破棄区間であるか"""
        ...
    @property
    def ActivateMessage(self) -> IMessage:
        """この実行仕様が受信する起動メッセージを取得します。
起動メッセージが存在しない場合は null を返します。"""
        ...
    @property
    def ReplyMessage(self) -> IMessage:
        """この実行仕様が送信する応答メッセージを取得します。
応答メッセージが存在しない場合は null を返します。"""
        ...

class IExecutionSpecificationCollection:
    """
    実行仕様情報のコレクションです。
    """
    def GetItem(self, index: int) -> IExecutionSpecification:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IExecutionSpecification: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IExecutionSpecificationEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IExecutionSpecificationEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IExecutionSpecification]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IExecutionSpecificationEnumerator:
    """
    実行仕様情報のコレクションの列挙子です。
    """
    ...

class IFrame(IModel, IMessagePort):
    """
    フレーム情報へのアクセスオブジェクトを表します。
    """
    ...

class IInteraction(IModel):
    """
    相互作用モデル情報へのアクセスオブジェクトを表します。
    """
    def GetLifelinesByName(self, name: str) -> ILifelineCollection:
        """
        指定した名前のライフラインを取得します。

        Args:
            name (str): ライフライン名。

        """
        ...
    def GetLifelinesByTypeModel(self, typeModel: IModel) -> ILifelineCollection:
        """
        指定した型モデルにマッピングされたライフラインを取得します。

        Args:
            typeModel (IModel): モデル。

        """
        ...
    def GetMessagesByTypeModel(self, typeModel: IModel) -> IMessageCollection:
        """
        指定した型モデルにマッピングされたメッセージを取得します。

        Args:
            typeModel (IModel): モデル。

        """
        ...
    @property
    def Frame(self) -> IFrame:
        """フレームを取得します。"""
        ...
    @property
    def Lifelines(self) -> ILifelineCollection:
        """ライフラインの一覧を取得します。"""
        ...
    @property
    def Messages(self) -> IMessageCollection:
        """メッセージの一覧を取得します。"""
        ...
    @property
    def MessageEnds(self) -> IMessageEndCollection:
        """メッセージ端の一覧を取得します。"""
        ...
    @property
    def InteractionUses(self) -> IInteractionUseCollection:
        """相互作用利用の一覧を取得します。"""
        ...

class IInteractionUse(IInteractionElement, IMessagePort):
    """
    相互作用利用情報へのアクセスオブジェクトを表します。
    """
    @property
    def CoveredLifelines(self) -> ILifelineCollection:
        """この相互作用利用に属するライフラインを取得します。"""
        ...
    @property
    def RefersTo(self) -> IInteraction:
        """この相互作用利用で参照するインタラクションを取得または設定します。"""
        ...

class IInteractionUseCollection:
    """
    相互作用利用情報のコレクションです。
    """
    def GetItem(self, index: int) -> IInteractionUse:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IInteractionUse: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IInteractionUseEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IInteractionUseEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IInteractionUse]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IInteractionUseEnumerator:
    """
    相互作用利用情報のコレクションの列挙子です。
    """
    ...

class ILifeline(IInteractionElement, IMessageSender, IMessageReceiver):
    """
    ライフライン情報へのアクセスオブジェクトを表します。
    """
    @property
    def TypeModel(self) -> IModel:
        """ライフラインの型にマッピングされたモデル"""
        ...
    @property
    def SendMessages(self) -> IMessageCollection:
        """このライフラインが送信元となるメッセージ一覧"""
        ...
    @property
    def ReceiveMessages(self) -> IMessageCollection:
        """このライフラインが受信先となるメッセージ一覧"""
        ...
    @property
    def ExecutionSpecifications(self) -> IExecutionSpecificationCollection:
        """このライフライン上の実行仕様一覧"""
        ...
    @property
    def Destruction(self) -> IDestruction:
        """このライフライン上の破棄"""
        ...

class ILifelineCollection:
    """
    ライフライン情報のコレクションです。
    """
    def GetItem(self, index: int) -> ILifeline:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ILifeline: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ILifelineEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ILifelineEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ILifeline]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ILifelineEnumerator:
    """
    ライフライン情報のコレクションの列挙子です。
    """
    ...

class IMessage(IInteractionElement):
    """
    メッセージ情報へのアクセスオブジェクトを表します。
    """
    @property
    def TypeModel(self) -> IModel:
        """メッセージの型にマッピングされたモデル"""
        ...
    @property
    def Kind(self) -> str:
        """メッセージの種類
（\"sync\", \"async\", \"create\", \"destroy\", \"reply\"）"""
        ...
    @property
    def IsSynchronous(self) -> bool:
        """このメッセージが同期メッセージであるか"""
        ...
    @property
    def IsAsynchronous(self) -> bool:
        """このメッセージが非同期メッセージであるか"""
        ...
    @property
    def IsReply(self) -> bool:
        """このメッセージが応答メッセージであるか"""
        ...
    @property
    def IsAppearance(self) -> bool:
        """このメッセージが出現メッセージであるか"""
        ...
    @property
    def IsLost(self) -> bool:
        """このメッセージが消失メッセージであるか"""
        ...
    @property
    def SendPort(self) -> IMessagePort:
        """メッセージの送信元ポート"""
        ...
    @property
    def SendPortType(self) -> str:
        """メッセージの送信元ポートの型
（\"ExecutionSpecification\", \"MessageEnd\", \"Frame\"）"""
        ...
    @property
    def Sender(self) -> ILifeline:
        """メッセージの送信元ライフライン"""
        ...
    @property
    def ReceivePort(self) -> IMessagePort:
        """メッセージの受信先ポート"""
        ...
    @property
    def ReceivePortType(self) -> str:
        """メッセージの受信先ポートの型
（\"ExecutionSpecification\", \"MessageEnd\", \"Frame\"）"""
        ...
    @property
    def Receiver(self) -> ILifeline:
        """メッセージの受信先ライフライン"""
        ...
    @property
    def Activator(self) -> IMessage:
        """このメッセージの起動メッセージ
起動メッセージが存在しない場合は null を返します。"""
        ...
    @property
    def Before(self) -> IMessage:
        """このメッセージの先行メッセージ
先行メッセージが存在しない場合は null を返します。"""
        ...
    @property
    def After(self) -> IMessage:
        """このメッセージの後行メッセージ
後行メッセージが存在しない場合は null を返します。"""
        ...
    @property
    def Reply(self) -> IMessage:
        """このメッセージに対応する応答メッセージ
対応する応答メッセージが存在しない場合は null を返します。"""
        ...

class IMessageCollection:
    """
    メッセージ情報のコレクションです。
    """
    def GetItem(self, index: int) -> IMessage:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMessage: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMessageEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMessageEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMessage]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMessageEnd(IInteractionElement, IMessagePort):
    """
    メッセージ端情報へのアクセスオブジェクトを表します。
    """
    @property
    def Message(self) -> IMessage:
        """このメッセージ端が送信、または受信するメッセージ
メッセージが接続されていない場合は null を返します。"""
        ...

class IMessageEndCollection:
    """
    メッセージ端情報のコレクションです。
    """
    def GetItem(self, index: int) -> IMessageEnd:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMessageEnd: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMessageEndEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMessageEndEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMessageEnd]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMessageEndEnumerator:
    """
    メッセージ端情報のコレクションの列挙子です。
    """
    ...

class IMessageEnumerator:
    """
    メッセージ情報のコレクションの列挙子です。
    """
    ...

class IAsyncValidationContext:
    """
    非同期検証のコンテキストです。
    """
    def ValidateAsync(self) -> Any:
        """
        非同期で検証します。

        Returns:
            Any: タスク。
        """
        ...
    def Cancel(self) -> None:
        """
        このコンテキストで実行中の検証をキャンセルします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RegisterOnStart(self, validateAction: Callable) -> IAsyncValidationContext: ...
    def RegisterOnFinish(self, validateAction: Callable) -> IAsyncValidationContext: ...
    def RegisterOnModelValidate(self, validateAction: Callable) -> IAsyncValidationContext: ...
    @property
    def TargetModel(self) -> IModel:
        """検証対象の起点モデルを取得します。"""
        ...
    @property
    def Options(self) -> ValidationOptions:
        """検証オプションを取得します。"""
        ...
    @property
    def State(self) -> str:
        """検証の実行状態を取得します。"""
        ...
    @property
    def Result(self) -> IAsyncValidationResult:
        """検証結果を取得します。"""
        ...
    @property
    def CancellationTokenSource(self) -> Any:
        """キャンセルトークンのソースオブジェクトを取得します。"""
        ...
    @property
    def CancellationToken(self) -> Any:
        """キャンセルトークンを取得します。"""
        ...
    @property
    def IsCancelRequested(self) -> bool:
        """このコンテキストで実行中の検証に対してキャンセルが要求されているか調べます。"""
        ...

class IAsyncValidationResult:
    """
    非同期検証の検証結果を管理します。
    """
    @property
    def IsCanceled(self) -> bool:
        """検証がキャンセルされたかを調べます。"""
        ...
    @property
    def HasErrors(self) -> bool:
        """検証でモデルのエラーを検出したかを調べます。"""
        ...
    @property
    def Errors(self) -> IErrorCollection:
        """検証で検出したエラー一覧を取得します。"""
        ...
    @property
    def Failed(self) -> bool:
        """検証に失敗したかを調べます。"""
        ...

class IModelCollection:
    """
    モデル情報のコレクションです。
    """
    def GetItem(self, index: int) -> IModel:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IModel: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IModelEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IModelEnumerator: 列挙子。
        """
        ...
    def __iter__(self) -> Iterator[IModel]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IModelEnumerator:
    """
    モデル情報のコレクションの列挙子です。
    """
    ...

class IObservableModelCollection(IModelCollection):
    """
    要素の増減に関するイベント通知をサポートするです。
    """
    def __iter__(self) -> Iterator[IModel]:
        ...

class IRelationshipCollection:
    """
    関連情報のコレクションです。
    """
    def GetItem(self, index: int) -> IRelationship:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IRelationship: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IRelationshipEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IRelationshipEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IRelationship]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IObservableRelationshipCollection(IRelationshipCollection):
    """
    関連の増減に関するイベント通知をサポートするです。
    """
    def __iter__(self) -> Iterator[IRelationship]:
        ...

class IRelationship(IModel):
    """
    関連情報へのアクセスオブジェクトを表します。
    """
    @overload
    def Relate(self, source: IModel, target: IModel, sourceIndex: int, targetIndex: int) -> None:
        """
        この関連の関連端を指定されたモデルに置き換えます。

        Args:
            source (IModel): 新しい関連元
            target (IModel): 新しい関連先
            sourceIndex (int): 新しい関連元の位置
            targetIndex (int): 新しい関連先の位置

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def Relate(self, fieldName: str, opposite: IModel) -> IRelationship: ...
    @overload
    def UnRelate(self) -> None:
        """
        この関連による関連づけを解除して、この関連を削除します。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnRelate(self, fieldName: str, opposite: IModel) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Source(self) -> IModel:
        """関連元インスタンス"""
        ...
    @property
    def Target(self) -> IModel:
        """関連先インスタンス"""
        ...
    @property
    def SourceIndex(self) -> int:
        """関連元に対する関連端フィールドにおけるインデックス"""
        ...
    @property
    def TargetIndex(self) -> int:
        """関連先に対する関連端フィールドにおけるインデックス"""
        ...
    @property
    def SourceField(self) -> IField:
        """関連元に対する関連端フィールド。
このフィールドは関連先オブジェクトのフィールドとなります。"""
        ...
    @property
    def TargetField(self) -> IField:
        """関連先に対する関連端フィールド。
このフィールドは関連元オブジェクトのフィールドとなります。"""
        ...
    @property
    def IsEmbedded(self) -> bool:
        """所有関連か"""
        ...
    @property
    def IsReference(self) -> bool:
        """参照関連か"""
        ...
    @property
    def IsDerivation(self) -> bool:
        """導出関連か"""
        ...
    @property
    def IsTwoWay(self) -> bool:
        """双方向関連か"""
        ...

class IRelationshipEnumerator:
    """
    関連情報のコレクションの列挙子です。
    """
    ...

class ModelExtensions:
    """
    に関する拡張メソッド群です。
    """
    ...

class ValidationOptions:
    """
    エラーチェックの検証オプション。
    """
    @property
    def ErrorFilter(self) -> List[str]:
        """検証するエラーコードを取得、または設定します。"""
        ...
    @property
    def ValidateMetamodelConstraints(self) -> bool:
        """メタモデルの整合検証(多重度検証、パス制約検証)を行うかを取得、または設定します。
既定値は true です。"""
        ...
    @property
    def ValidateProductLineConstraints(self) -> bool:
        """プロダクトラインの整合検証(フィーチャ条件式検証、フィーチャ構造の検証、フィーチャ間制約の検証、フィーチャのユニーク検証)を行うかを取得、または設定します。
既定値は true です。"""
        ...
    @property
    def Recursive(self) -> bool:
        """子要素を再帰的に検証するかを取得、または設定します。
既定値は true です。"""
        ...
    @property
    def RaiseValidateEvents(self) -> bool:
        """モデル検証時イベントを発行するかどうかを取得、または設定します。
既定値は true です。"""
        ...

class IConfigurationModel(IModel):
    """
    プロダクトコンフィグレーションモデル対するアクセスオブジェクトを表します。
    """
    def GetProduct(self, name: str) -> IProduct:
        """
        指定された名前のプロダクトを取得します

        Args:
            name (str): プロダクト名

        Returns:
            IProduct: プロダクト
        """
        ...
    def AddNewProduct(self, name: str) -> IProduct:
        """
        新しいプロダクトを追加します。

        Args:
            name (str): プロダクト名

        Returns:
            IProduct: プロダクト
        """
        ...
    def DuplicateProduct(self, sourceProduct: IProduct, name: str) -> IProduct:
        """
        プロダクトを複製します。

        Args:
            sourceProduct (IProduct): 複製元プロダクト
            name (str): プロダクト名

        Returns:
            IProduct: 複製したプロダクト
        """
        ...
    def RemoveProduct(self, name: str) -> None:
        """
        指定された名前のプロダクトを削除します。

        Args:
            name (str): プロダクト名

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def AllProducts(self) -> IProductCollection:
        """全てのプロダクト一覧"""
        ...

class IFeature(IModel):
    """
    プロダクトの特徴（フィーチャ）情報に対するアクセスオブジェクトを表します。
    """
    def AddConstraint(self, target: IFeature, kind: str) -> None:
        """
        指定されたフィーチャとの間に指定した種類の制約関係を追加します。

        Args:
            target (IFeature): 制約先フィーチャ
            kind (str): 制約種類

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveConstraint(self, target: IFeature, kind: str) -> None:
        """
        指定されたフィーチャとの間の指定した種類の制約関係を削除します。

        Args:
            target (IFeature): 制約先フィーチャ
            kind (str): 制約種類

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveAllConstraint(self) -> None:
        """
        このフィーチャのすべての制約関係を削除します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetAssignedModels(self) -> IModelCollection:
        """
        このフィーチャを割り当てているモデル一覧を取得します

        Returns:
            IModelCollection: 割り当てているモデル一覧
        """
        ...
    @property
    def VariationKind(self) -> str:
        """フィーチャの種類（Mandatory, Optional, Alternative, Or）"""
        ...
    @property
    def UniqueName(self) -> str:
        """ユニーク名"""
        ...
    @property
    def IsDefaultSelected(self) -> bool:
        """フィーチャを初期選択状態とするか"""
        ...
    @property
    def SubFeatures(self) -> IFeatureCollection:
        """サブフィーチャ一覧"""
        ...
    @property
    def ParentFeature(self) -> IFeature:
        """親フィーチャ"""
        ...
    @property
    def OwnerModel(self) -> IFeatureModel:
        """このフィーチャを管理するフィーチャモデル"""
        ...

class IFeatureCollection:
    """
    フィーチャのコレクションです。
    """
    def GetItem(self, index: int) -> IFeature:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IFeature: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IFeatureEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        """
        ...
    def __iter__(self) -> Iterator[IFeature]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IFeatureEnumerator:
    """
    フィーチャの列挙子です。
    """
    ...

class IFeatureModel(IModel):
    """
    プロダクトの特徴（フィーチャ）を構造化した管理モデルに対するアクセスオブジェクトを表します。
    """
    def GetFeature(self, name: str) -> IFeature:
        """
        指定された名前のフィーチャを取得します

        Args:
            name (str): フィーチャ名

        Returns:
            IFeature: フィーチャ
        """
        ...
    def AddNewFeature(self, name: str) -> IFeature:
        """
        新しい基点フィーチャを追加します。

        Args:
            name (str): フィーチャ名

        Returns:
            IFeature: フィーチャ
        """
        ...
    def AddNewFeatureAt(self, name: str, kind: str, parentFeature: IFeature) -> IFeature:
        """
        指定されたフィーチャの子要素として新しいフィーチャを追加します。

        Args:
            name (str): フィーチャ名
            kind (str): フィーチャ種類
            parentFeature (IFeature): 親フィーチャ

        Returns:
            IFeature: フィーチャ
        """
        ...
    def RemoveFeature(self, feature: IFeature) -> None:
        """
        指定されたフィーチャを削除します。

        Args:
            feature (IFeature): フィーチャ

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveFeatureByName(self, name: str) -> None:
        """
        指定された名前のフィーチャを削除します。

        Args:
            name (str): フィーチャ名

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddFeatureConstraint(self, source: IFeature, target: IFeature, kind: str) -> None:
        """
        指定されたフィーチャ間に指定した種類の制約関係を追加する

        Args:
            source (IFeature): 制約元フィーチャ
            target (IFeature): 制約先フィーチャ
            kind (str): 制約種類（\"Conflicts\", \"Requires\"）

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveFeatureConstraint(self, feature: IFeature, opposite: IFeature, kind: str) -> None:
        """
        指定されたフィーチャ間の指定した種類の制約関係を削除します。

        Args:
            feature (IFeature): 端点となるフィーチャ
            opposite (IFeature): 相手先のフィーチャ
            kind (str): 制約種類（\"Conflicts\", \"Requires\"）

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetFeatureConstraint(self, source: IFeature, opposite: IFeature, kind: str) -> IRelationship:
        """
        指定されたフィーチャ間の指定した種類の制約関係を取得します

        Args:
            source (IFeature): 制約元フィーチャ
            opposite (IFeature): 制約先フィーチャ
            kind (str): 制約種類（\"Conflicts\", \"Implicit\", \"Requires\"）

        Returns:
            IRelationship: 制約関係
        """
        ...
    @property
    def RootFeatures(self) -> IFeatureCollection:
        """フィーチャツリーの基点となるフィーチャ一覧"""
        ...
    @property
    def AllFeatures(self) -> IFeatureCollection:
        """このモデル以下で保持するすべてのフィーチャ一覧"""
        ...

class IFeatureModelCollection:
    """
    フィーチャモデルのコレクションです。
    """
    def GetItem(self, index: int) -> IFeatureModel:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IFeatureModel: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IFeatureModelEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        """
        ...
    def __iter__(self) -> Iterator[IFeatureModel]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IFeatureModelEnumerator:
    """
    フィーチャモデルの列挙子です。
    """
    ...

class IProduct(IModel):
    """
    プロダクト情報対するアクセスオブジェクトを表します。
    """
    def SelectFeature(self, feature: IFeature) -> bool:
        """
        指定されたフィーチャを選択します。

        Args:
            feature (IFeature): フィーチャ

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    def DeselectFeature(self, feature: IFeature) -> bool:
        """
        指定されたフィーチャを未選択にします。

        Args:
            feature (IFeature): フィーチャ

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    def SelectFeatureByName(self, featureName: str) -> bool:
        """
        指定された名前のフィーチャを選択します。

        Args:
            featureName (str): フィーチャ名

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    def DeselectFeatureByName(self, featureName: str) -> bool:
        """
        指定された名前のフィーチャを未選択にします。

        Args:
            featureName (str): フィーチャ名

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    def SelectFeatures(self, features: Iterable[IFeature]) -> bool: ...
    def DeselectFeatures(self, features: Iterable[IFeature]) -> bool: ...
    def SelectFeaturesByName(self, featureNames: str) -> bool:
        """
        指定された名前のフィーチャ群を選択します。

        Args:
            featureNames (str): フィーチャ名（カンマ区切りで複数指定可）

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    def DeselectFeaturesByName(self, featureNames: str) -> bool:
        """
        指定された名前のフィーチャ群を未選択にします。

        Args:
            featureNames (str): フィーチャ名（カンマ区切りで複数指定可）

        Returns:
            bool: 選択状態が設定できた場合は真
        """
        ...
    @property
    def SelectedFeatures(self) -> IFeatureCollection:
        """このプロダクトで選択されているフィーチャ一覧"""
        ...

class IProductCollection:
    """
    プロダクトのコレクションです。
    """
    def GetItem(self, index: int) -> IProduct:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IProduct: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IProductEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        """
        ...
    def __iter__(self) -> Iterator[IProduct]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IProductEnumerator:
    """
    プロダクトの列挙子です。
    """
    ...

class IProductLineModel(IModel):
    """
    プロダクトライン開発支援モデルに対するアクセスオブジェクトを表します。
    """
    def AddNewFeatureModel(self, name: str) -> IFeatureModel:
        """
        新しいフィーチャモデルを追加します。

        Args:
            name (str): フィーチャモデル名

        Returns:
            IFeatureModel: フィーチャモデル
        """
        ...
    def RemoveFeatureModel(self, featureModel: IFeatureModel) -> None:
        """
        指定されたフィーチャモデルを削除します。

        Args:
            featureModel (IFeatureModel): フィーチャモデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveFeatureModelByName(self, featureModelName: str) -> None:
        """
        指定されたフィーチャモデルを削除します。

        Args:
            featureModelName (str): フィーチャモデル名

        Returns:
            None: This method does not return a value.
        """
        ...
    def ApplyProduct(self, product: IProduct, isSetCurrent: bool) -> None:
        """
        指定されたプロダクトを適用します。
        プロダクト適用後に、フィーチャモデル構造や、プロダクト適用条件式を変更した場合は、再度このメソッドを呼び出すことで
        プロダクト適用結果が再計算されます。

        Args:
            product (IProduct): プロダクト、nullを指定した場合は適用プロダクトなしとなります
            isSetCurrent (bool): 指定したプロダクトをカレントプロダクトに設定するか。プロダクトが未指定の場合は無視されます

        Returns:
            None: This method does not return a value.
        """
        ...
    def ApplyProductBy(self, productName: str) -> None:
        """
        指定された名前のプロダクトを適用して、カレントプロダクトに設定します。

        Args:
            productName (str): プロダクト名、適用プロダクトなし（150%モデル）とする場合は、\"$Master\"を指定します

        Returns:
            None: This method does not return a value.
        """
        ...
    def ExportAppliedProject(self, product: IProduct, exportProjectPath: str) -> None:
        """
        指定されたプロダクトを適用したプロジェクトを指定されたパスにエクスポートします。
        エクスポートしたプロジェクトは以下の状態となります。
        - プロファイルはエクスポート元と同一
        - 指定されたプロダクトで有効なモデル要素、エディタのみが存在する
        - プロダクトラインモデル（フィーチャモデル、コンフィグレーションモデル）はなし
        - ユニット分割はなし

        Args:
            product (IProduct): プロダクト、nullは指定できません
            exportProjectPath (str): プロジェクトの出力先のパス（絶対パス）

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def FeatureModels(self) -> IFeatureModelCollection:
        """フィーチャモデル一覧"""
        ...
    @property
    def ConfigurationModel(self) -> IConfigurationModel:
        """コンフィグレーションモデル"""
        ...
    @property
    def CurrentProduct(self) -> IProduct:
        """現在適用状態のプロダクト"""
        ...
    @property
    def ProductAppliedState(self) -> str:
        """現在のプロダクト適用状態。
以下のいずれかの状態文字列を返します。
- SpecifiedProduct : 任意のプロダクトを適用中。適用中のプロダクトは、CurrentProduct で取得できます。
- Master : プロダクト適用なし（150%モデル表示）。この状態の場合、CurrentProduct は null を返します。"""
        ...

class CustomDefinitionDescriptorBase:
    """
    カスタム定義要素のタイプ記述子基底
    """
    @property
    def CustomEditorTypeId(self) -> str:
        """カスタムエディタの種類識別子"""
        ...
    @property
    def DisplayName(self) -> str:
        """表示名"""
        ...
    @property
    def AccessKey(self) -> str:
        """アクセスキー"""
        ...
    @property
    def SmallIcon(self) -> Any:
        """アイコン（小）"""
        ...
    @property
    def LargeIcon(self) -> Any:
        """アイコン（大）"""
        ...
    @property
    def Groups(self) -> Iterable[PropertyGroupDescriptor]:
        """ビュー定義の編集できるプロパティグループ記述子の列挙"""
        ...

class CustomEditorDefinitionDescriptor(CustomDefinitionDescriptorBase):
    """
    カスタムエディタビュー定義のタイプ記述子です。
    """
    @property
    def GroupName(self) -> str:
        """グループ名を取得または設定します。"""
        ...
    @property
    def Elements(self) -> Iterable[CustomElementDefinitionDescriptor]:
        """ビュー要素定義のタイプ記述子の列挙を取得または設定します。"""
        ...

class CustomElementDefinitionDescriptor(CustomDefinitionDescriptorBase):
    """
    カスタムエディタ要素定義のタイプ記述子
    """
    @property
    def ElementTypeId(self) -> str:
        """エディタ要素の種類識別子"""
        ...
    @property
    def AllowMultiple(self) -> bool:
        """同じ種類のエディタ要素の複数定義を許容するか"""
        ...

class PropertyDescriptor:
    """
    プロパティ記述子
    """
    @property
    def Id(self) -> str:
        """プロパティ識別子"""
        ...
    @property
    def DisplayName(self) -> str:
        """プロパティ表示名"""
        ...
    @property
    def Type(self) -> Any:
        """プロパティの種類"""
        ...
    @property
    def DefaultValue(self) -> Any:
        """初期値"""
        ...
    @property
    def AllowedValues(self) -> Iterable[str]:
        """がの場合に候補として提示する選択肢"""
        ...
    @property
    def IsHidden(self) -> bool:
        """非表示とするか"""
        ...
    @property
    def OnValidateCallback(self) -> Callable:
        """値変更時の検証時に呼び出される関数"""
        ...

class PropertyGroupDescriptor:
    """
    プロパティグループ記述子
    """
    @property
    def Id(self) -> str:
        """グループ識別子"""
        ...
    @property
    def DisplayName(self) -> str:
        """グループ表示名"""
        ...
    @property
    def Properties(self) -> Iterable[PropertyDescriptor]:
        """ビュー定義の編集できるプロパティ記述子の列挙"""
        ...

class INamedElement(IObject):
    """
    名前付け可能要素を表します。
    """
    def GetProfileReferencePackage(self) -> IPackage:
        """
        この要素を管理するプロファイル参照パッケージを取得します。
        この要素自身がプロファイル参照パッケージの場合は、この要素自身を取得します。
        この要素が多段でプロファイル参照される要素（プロファイル参照を持つプロファイルをさらにプロファイル参照で追加した要素）である場合は、
        プロファイル参照情報で依存関係があるプロファイルの基点として記録されているパッケージを取得します。
        また、この要素がプロファイル参照パッケージ配下の要素でない場合は、プロファイルのルートパッケージを取得します。
        この動作は、あるプロファイルで定義された要素は、そのプロファイルがどのように参照されていたとしても、
        その要素を定義したプロファイルのルートパッケージに対応するパッケージを返すことになります。

        Returns:
            IPackage: 基点パッケージ。
        """
        ...
    @property
    def Name(self) -> str:
        """名前を取得、または設定します。"""
        ...
    @property
    def Description(self) -> str:
        """説明を取得、または設定します。"""
        ...
    @property
    def DisplayName(self) -> str:
        """表示名を取得、または設定します。"""
        ...
    @property
    def BaseId(self) -> str:
        """ベース識別子を取得します。"""
        ...
    @property
    def IsDisabled(self) -> bool:
        """無効化されているかを取得します。"""
        ...

class IType(INamedElement):
    """
    型を表します。
    """
    ...

class IClass(IType):
    """
    メタクラスを表します。
    """
    def AddSuperClass(self, superClass: IClass) -> None:
        """
        指定したクラスをこのクラスのスーパークラスに追加します。
        指定したクラスが既にこのクラスのスーパークラスに含まれる場合は何も行われません。

        Args:
            superClass (IClass): クラス

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddSuperClasses(self, superClasses: Iterable[IClass]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveSuperClass(self, superClass: IClass) -> None:
        """
        指定したクラスをこのクラスのスーパークラスから削除します。
        指定したクラスがこのクラスのスーパークラスに含まれない場合は何も行われません。
        クラスの継承関係を削除すると継承先クラスのモデルも削除します。

        Args:
            superClass (IClass): クラス

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveSuperClasses(self, superClasses: Iterable[IClass]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def GetAllSuperClasses(self) -> IClassCollection:
        """
        このクラスの全てのスーパークラスを取得します。

        """
        ...
    def GetSubClasses(self) -> IClassCollection:
        """
        このクラスを直接の派生クラスを取得します。

        """
        ...
    def GetAllSubClasses(self) -> IClassCollection:
        """
        このクラスから派生するすべてのクラスを取得します。

        """
        ...
    def IsClassOf(self, someClass: IClass) -> bool:
        """
        指定したクラスがこのクラスと互換するか

        Args:
            someClass (IClass): クラス

        Returns:
            bool: このクラスと互換する場合は真
        """
        ...
    def IsSuperClass(self, someClass: IClass) -> bool:
        """
        このクラスが指定したクラスのスーパークラスか

        Args:
            someClass (IClass): クラス

        Returns:
            bool: スーパークラスの場合は真
        """
        ...
    def Is(self, model: IModel) -> bool:
        """
        指定したモデルがこのクラスのインスタンスであるか

        Args:
            model (IModel): モデル

        Returns:
            bool: このクラスのインスタンスの場合は真
        """
        ...
    def As(self, model: IModel) -> bool:
        """
        指定したモデルがこのクラスと互換するインスタンスであるか

        Args:
            model (IModel): モデル

        Returns:
            bool: このクラスと互換するインスタンスの場合は真
        """
        ...
    def GetFields(self) -> IFieldCollection:
        """
        このインスタンスのフィールドを取得します。

        Returns:
            IFieldCollection: フィールドの列挙
        """
        ...
    def GetField(self, name: str) -> IField:
        """
        このインスタンスの指定されたフィールドを取得します。

        Args:
            name (str): フィールド名

        Returns:
            IField: フィールド
        """
        ...
    def GetFieldsByTag(self, tag: str, value: str) -> IFieldCollection:
        """
        指定されたタグが付与されたこのクラスのフィールドを取得します。

        Args:
            tag (str): タグ名
            value (str): タグ値

        Returns:
            IFieldCollection: 指定されたタグが付与されたフィールドの一覧
        """
        ...
    def GetFieldsByType(self, typeName: str) -> IFieldCollection:
        """
        このクラスの指定された型名のフィールドを取得します。

        Args:
            typeName (str): フィールドの型名
- \"Boolean\" : 真偽値型
- \"Integer\" : 整数型
- \"Double\" : 実数型
- \"String\" : 文字列型
- \"RichText\" : リッチテキスト型
- \"RichContentsDataType\" : リッチコンテンツ型
- その他の任意文字列 : クラス、または列挙の完全修飾名として扱います。

        Returns:
            IFieldCollection: フィールド一覧
        """
        ...
    def GetFieldsOf(self, type: IClass) -> IFieldCollection:
        """
        このクラスの指定された型のフィールドを取得します。

        Args:
            type (IClass): フィールドの型（クラス型）

        Returns:
            IFieldCollection: フィールド一覧
        """
        ...
    def GetEmbeddedFieldsOf(self, type: IClass) -> IFieldCollection:
        """
        このクラスの指定された型の所有フィールドを取得します。

        Args:
            type (IClass): フィールドの型（クラス型）

        Returns:
            IFieldCollection: フィールド一覧
        """
        ...
    def GetReferenceFieldsOf(self, type: IClass) -> IFieldCollection:
        """
        このクラスの指定された型の参照フィールドを取得します。

        Args:
            type (IClass): フィールドの型（クラス型）

        Returns:
            IFieldCollection: フィールド一覧
        """
        ...
    def GetMethods(self) -> IMethodCollection:
        """
        このインスタンスのメソッド（揮発性）を取得します。

        Returns:
            IMethodCollection: メソッド（揮発性）の列挙
        """
        ...
    def GetMethod(self, name: str) -> IMethod:
        """
        このインスタンスの指定されたメソッド（揮発性）を取得します。

        Args:
            name (str): メソッド名

        Returns:
            IMethod: メソッド（揮発性）
        """
        ...
    def GetConstraints(self) -> IConstraintCollection:
        """
        このクラスで定義する制約を取得します。

        Returns:
            IConstraintCollection: 制約の列挙
        """
        ...
    def GetConstraintsByTarget(self, targetIdentifier: str) -> IConstraintCollection:
        """
        このクラスで定義する指定された制約適用対象の要素の制約を取得します。

        Args:
            targetIdentifier (str): 制約適用対象の要素識別子

        Returns:
            IConstraintCollection: 制約の列挙
        """
        ...
    def GetConstraintsByField(self, fieldName: str) -> IConstraintCollection:
        """
        このクラスで定義する指定されたフィールドの制約を取得します。

        Args:
            fieldName (str): 制約適用対象フィールド名

        Returns:
            IConstraintCollection: 制約の列挙
        """
        ...
    def GetConstraintByName(self, name: str) -> IConstraint:
        """
        このクラスで定義する指定された名前の制約を取得します。
        同じ名前の制約が複数ある場合は、最初にみつかった制約を返します。

        Args:
            name (str): 制約名

        Returns:
            IConstraint: 制約
        """
        ...
    @property
    def Owner(self) -> IPackage:
        """パッケージ"""
        ...
    @property
    def FullName(self) -> str:
        """完全修飾名"""
        ...
    @property
    def IsAbstract(self) -> bool:
        """抽象クラスか"""
        ...
    @property
    def Fields(self) -> Dict[str, IField]:
        """フィールド一覧"""
        ...
    @property
    def Methods(self) -> Dict[str, IMethod]:
        """メソッド（揮発性）一覧"""
        ...
    @property
    def DeclaredFields(self) -> IFieldCollection:
        """固有フィールド一覧"""
        ...
    @property
    def SuperClasses(self) -> IClassCollection:
        """スーパークラス一覧"""
        ...

class IClassCollection:
    """
    メタクラスのコレクションです。
    """
    def GetItem(self, index: int) -> IClass:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IClass: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IClassEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IClassEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IClass]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IClassEnumerator:
    """
    メタクラスのコレクションの列挙子です。
    """
    ...

class IConstraint(INamedElement):
    """
    制約を表します。
    """
    def IsSatisfiedWith(self, model: IModel, target: Any) -> bool:
        """
        指定されたモデルを基点に、与えられたオブジェクトがこの制約に合致するか調べます。

        Args:
            model (IModel): 制約評価の基点となるモデル
            target (Any): 制約を評価する対象オブジェクト

        Returns:
            bool: 制約を満たす場合は真
        """
        ...
    @property
    def Key(self) -> str:
        """制約の内容を解釈する方法の種類"""
        ...
    @property
    def Condition(self) -> str:
        """制約の内容を表す文字列"""
        ...
    @property
    def ConstrainedElements(self) -> INamedElementCollection:
        """制約適用対象の要素のコレクション"""
        ...
    @property
    def Scope(self) -> IClass:
        """制約が有効となる範囲"""
        ...

class IConstraintCollection:
    """
    制約のコレクションです。
    """
    def GetItem(self, index: int) -> IConstraint:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IConstraint: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IConstraintEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IConstraintEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IConstraint]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IConstraintEnumerator:
    """
    制約のコレクションの列挙子です。
    """
    ...

class IViewDefinition(INamedElement):
    """
    ビュー定義要素を表します。
    """
    @property
    def ModelClass(self) -> IClass:
        """モデルクラス"""
        ...
    @property
    def ModelClassName(self) -> str:
        """モデルクラス名"""
        ...

class IEditorDef(IViewDefinition):
    """
    エディタ定義を表します。
    """
    def GetElementsByTag(self, tag: str, value: str) -> IElementDefCollection:
        """
        指定されたタグが付与されたエディタ要素定義を取得します

        Args:
            tag (str): タグ名
            value (str): タグ値

        Returns:
            IElementDefCollection: 指定されたタグが付与されたエディタ要素定義の一覧
        """
        ...
    @property
    def Type(self) -> str:
        """エディタ種類"""
        ...
    @property
    def Elements(self) -> IElementDefCollection:
        """エディタ要素定義一覧"""
        ...
    @property
    def ExportDocument(self) -> bool:
        """ドキュメント出力するかを取得または設定します。"""
        ...

class ICustomEditorDefinition(IEditorDef):
    """
    カスタムエディタ定義を表します。
    """
    @property
    def CustomEditorTypeId(self) -> str:
        """カスタムエディタの種類識別子"""
        ...
    @property
    def DefinitionDescriptor(self) -> CustomEditorDefinitionDescriptor:
        """このビュー定義のタイプ記述子"""
        ...
    @property
    def PropertyValues(self) -> Dict[str, Any]:
        """このビュー定義のプロパティ値"""
        ...
    @property
    def CustomElements(self) -> Iterable[ICustomElementDefinition]:
        """カスタムエディタ要素ビュー定義の列挙"""
        ...

class IElementDef(IViewDefinition):
    """
    エディタ要素定義を表します。
    """
    @property
    def Type(self) -> str:
        """エディタ要素種類"""
        ...
    @property
    def Path(self) -> str:
        """パス"""
        ...
    @property
    def ForeColor(self) -> str:
        """前景色"""
        ...
    @property
    def BackColor(self) -> str:
        """背景色"""
        ...
    @property
    def BorderColor(self) -> str:
        """境界色"""
        ...

class ICustomElementDefinition(IElementDef):
    """
    カスタムエディタ要素定義を表します。
    """
    @property
    def ElementTypeId(self) -> str:
        """カスタムエディタ要素の種類識別子"""
        ...
    @property
    def DefinitionDescriptor(self) -> CustomElementDefinitionDescriptor:
        """このビュー定義のタイプ記述子"""
        ...
    @property
    def PropertyValues(self) -> Dict[str, Any]:
        """このビュー定義のプロパティ値"""
        ...

class IEditorDefCollection:
    """
    エディタ定義のコレクションです。
    """
    def GetItem(self, index: int) -> IEditorDef:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IEditorDef: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IEditorDefEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IEditorDefEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IEditorDef]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IEditorDefEnumerator:
    """
    エディタ定義のコレクションの列挙子です。
    """
    ...

class IElementDefCollection:
    """
    エディタ要素定義のコレクションです。
    """
    def GetItem(self, index: int) -> IElementDef:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IElementDef: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IElementDefEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IElementDefEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IElementDef]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IElementDefEnumerator:
    """
    エディタ要素定義のコレクションの列挙子です。
    """
    ...

class IEnum(IType):
    """
    列挙型を表します。
    """
    def Is(self, instance: Any) -> bool:
        """
        指定したオブジェクトが列挙型のインスタンスかどうか調べます。

        Args:
            instance (Any): オブジェクト。

        Returns:
            bool: 列挙型のインスタンスの場合は真。
        """
        ...
    def ValueOf(self, value: int) -> IEnumLiteral:
        """
        Enum値に該当する列挙型リテラルを取得します。

        Args:
            value (int): Enum値。

        Returns:
            IEnumLiteral: Enum値に該当する列挙型リテラル。
        """
        ...
    def NameOf(self, name: str) -> IEnumLiteral:
        """
        リテラル文字列に該当する列挙型リテラルを取得します。

        Args:
            name (str): リテラル文字列。

        Returns:
            IEnumLiteral: リテラル文字列に該当する列挙型リテラル。
        """
        ...
    def GetLiteralsByTag(self, tag: str, value: str) -> IEnumLiteralCollection:
        """
        指定されたタグが付与された列挙型リテラルを取得します。

        Args:
            tag (str): タグ名。
            value (str): タグ値。

        Returns:
            IEnumLiteralCollection: 指定されたタグが付与された列挙型リテラルの一覧。
        """
        ...
    @property
    def Owner(self) -> IPackage:
        """パッケージ"""
        ...
    @property
    def FullName(self) -> str:
        """完全修飾名"""
        ...
    @property
    def Literals(self) -> IEnumLiteralCollection:
        """リテラル一覧"""
        ...

class IEnumCollection:
    """
    列挙型のコレクションです。
    """
    def GetItem(self, index: int) -> IEnum:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IEnum: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IEnumEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IEnumEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IEnum]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IEnumEnumerator:
    """
    列挙型のコレクションの列挙子です。
    """
    ...

class IEnumLiteral(INamedElement):
    """
    列挙型リテラルを表します。
    """
    @property
    def Value(self) -> int:
        """値を取得します。"""
        ...
    @property
    def OwnerEnum(self) -> IEnum:
        """このリテラルを保持している列挙型を取得します。"""
        ...

class IEnumLiteralCollection:
    """
    列挙型リテラルのコレクションです。
    """
    def GetItem(self, index: int) -> IEnumLiteral:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IEnumLiteral: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IEnumLiteralEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IEnumLiteralEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IEnumLiteral]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IEnumLiteralEnumerator:
    """
    列挙型リテラルのコレクションの列挙子です。
    """
    ...

class IField(INamedElement):
    """
    フィールドを表します。
    """
    @property
    def Type(self) -> str:
        """型名を取得します。"""
        ...
    @property
    def TypeClass(self) -> IClass:
        """クラス型を取得します。"""
        ...
    @property
    def TypeEnum(self) -> IEnum:
        """列挙型を取得します。"""
        ...
    @property
    def OwnerClass(self) -> IClass:
        """このフィールドを保持（宣言）しているクラスを取得します。"""
        ...
    @property
    def Category(self) -> str:
        """フィールドのカテゴリを取得または設定します。"""
        ...
    @property
    def LowerBound(self) -> int:
        """多重度（下限）を取得または設定します。"""
        ...
    @property
    def UpperBound(self) -> int:
        """多重度（上限）を取得または設定します。"""
        ...
    @property
    def IsEmbedded(self) -> bool:
        """所有フィールドであるかを取得します。"""
        ...
    @property
    def IsReference(self) -> bool:
        """参照フィールドであるかを取得します。"""
        ...
    @property
    def IsDerivationSource(self) -> bool:
        """導出元フィールドであるかを取得します。"""
        ...
    @property
    def IsDerivationTarget(self) -> bool:
        """導出先フィールドであるかを取得します。"""
        ...
    @property
    def DefaultValue(self) -> Any:
        """デフォルト値を取得または設定します。"""
        ...
    @property
    def RelationshipClass(self) -> IRelationshipClass:
        """関連クラスを取得します。"""
        ...

class IFieldCollection:
    """
    フィールドのコレクションです。
    """
    def GetItem(self, index: int) -> IField:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IField: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IFieldEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IFieldEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IField]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IFieldEnumerator:
    """
    フィールドのコレクションの列挙子です。
    """
    ...

class IMetamodels:
    """
    メタモデル管理オブジェクトを表します。
    """
    def GetPackage(self, fullName: str) -> IPackage:
        """
        指定した完全修飾名のパッケージを取得します。
        パッケージが見つからない場合は null を返します。

        Args:
            fullName (str): 完全修飾名。

        Returns:
            IPackage: パッケージ。
        """
        ...
    def GetPackageById(self, packageId: str) -> IPackage:
        """
        指定した識別子のパッケージを取得します。

        Args:
            packageId (str): パッケージの識別子。

        Returns:
            IPackage: パッケージ。
        """
        ...
    @overload
    def FindPackagesByName(self, packageName: str) -> IPackageCollection:
        """
        指定した名前のパッケージを探索します。

        Args:
            packageName (str): パッケージ名。

        Returns:
            IPackageCollection: パッケージの一覧。
        """
        ...
    @overload
    def FindPackagesByName(self, scope: IPackage, packageName: str) -> IPackageCollection:
        """
        スコープで指定したパッケージの配下から指定した名前のパッケージを探索します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            packageName (str): パッケージ名。

        Returns:
            IPackageCollection: パッケージの一覧。
        """
        ...
    def FindPackagesByTag(self, tag: str, value: str) -> IPackageCollection:
        """
        指定したタグが付与されたパッケージを検索します。

        Args:
            tag (str): タグ名。
            value (str): タグ値。

        Returns:
            IPackageCollection: 指定されたタグが付与されたパッケージの一覧。
        """
        ...
    @overload
    def GetClass(self, className: str, fuzzy: bool) -> IClass:
        """
        指定した名前のクラスを取得します。

        Args:
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IClass: クラス。
        """
        ...
    @overload
    def GetClass(self, scope: IPackage, className: str, fuzzy: bool) -> IClass:
        """
        スコープで指定したパッケージの配下から指定した名前のクラスを取得します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IClass: クラス。
        """
        ...
    @overload
    def FindClassesByName(self, classNames: str, fuzzy: bool) -> IClassCollection:
        """
        指定したクラス名のクラスを検索します。

        Args:
            classNames (str): クラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IClassCollection: クラスの一覧。
        """
        ...
    @overload
    def FindClassesByName(self, scope: IPackage, classNames: str, fuzzy: bool) -> IClassCollection:
        """
        スコープで指定したパッケージの配下から指定したクラス名のクラスを検索します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            classNames (str): クラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IClassCollection: クラスの一覧。
        """
        ...
    @overload
    def FindClassesByName(self, classNames: Iterable[str], fuzzy: bool) -> IClassCollection: ...
    @overload
    def FindClassesByName(self, scope: IPackage, classNames: Iterable[str], fuzzy: bool) -> IClassCollection: ...
    def FindClassesWithField(self, fieldName: str) -> IClassCollection:
        """
        指定したフィールドをもつクラスを検索します。

        Args:
            fieldName (str): フィールド名。

        Returns:
            IClassCollection: 該当するクラスの一覧。
        """
        ...
    def FindClassesByTag(self, tag: str, value: str) -> IClassCollection:
        """
        指定したタグが付与されたクラスを検索します。

        Args:
            tag (str): タグ名。
            value (str): タグ値。

        Returns:
            IClassCollection: 指定されたタグが付与されたクラスの一覧。
        """
        ...
    def GetSubClasses(self, metaclass: IClass, recursive: bool) -> IClassCollection:
        """
        指定したクラスのサブクラスを取得します。

        Args:
            metaclass (IClass): メタクラス。
            recursive (bool): サブクラスのサブクラスも含めるか。

        Returns:
            IClassCollection: 該当するクラスの一覧。
        """
        ...
    @overload
    def GetEnum(self, enumName: str, fuzzy: bool) -> IEnum:
        """
        指定した名前の列挙型を取得します。

        Args:
            enumName (str): 列挙型名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IEnum: 列挙型。
        """
        ...
    @overload
    def GetEnum(self, scope: IPackage, enumName: str, fuzzy: bool) -> IEnum:
        """
        スコープで指定したパッケージの配下から指定した名前の列挙型を取得します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            enumName (str): 列挙名。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            IEnum: 列挙型。
        """
        ...
    def FindEnumsByTag(self, tag: str, value: str) -> IEnumCollection:
        """
        指定したタグが付与された列挙型を検索します。

        Args:
            tag (str): タグ名。
            value (str): タグ値。

        Returns:
            IEnumCollection: 指定されたタグが付与された列挙型の一覧。
        """
        ...
    def GetTypeById(self, typeId: str) -> Any: ...
    @overload
    def GetTypeByName(self, typeName: str, fuzzy: bool) -> Any: ...
    @overload
    def GetTypeByName(self, scope: IPackage, typeName: str, fuzzy: bool) -> Any: ...
    def NewPackage(self, name: str, parent: IPackage) -> IPackage:
        """
        新しいパッケージを生成します。

        Args:
            name (str): パッケージ名。
            parent (IPackage): 親パッケージ。

        Returns:
            IPackage: 生成したパッケージ。
        """
        ...
    @overload
    def MoveToPackage(self, classNames: str, newOwner: IPackage, fuzzy: bool) -> None:
        """
        指定したクラスを指定したパッケージ管理下に移動します。

        Args:
            classNames (str): クラス名（カンマ区切りで複数指定可能）。
            newOwner (IPackage): 移動先のパッケージ。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def MoveToPackage(self, scope: IPackage, classNames: str, newOwner: IPackage, fuzzy: bool) -> None:
        """
        スコープで指定したパッケージの配下から指定したクラスを指定したパッケージ管理下に移動します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            classNames (str): クラス名（カンマ区切りで複数指定可能）。
            newOwner (IPackage): 移動先のパッケージ。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def MoveToPackage(self, targets: Iterable[IClass], newOwner: IPackage) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def NewClass(self, name: str, owner: IPackage, isAbstract: bool) -> IClass:
        """
        指定したパッケージ内に指定したクラス名で新しいクラスを生成します。

        Args:
            name (str): クラス名。
            owner (IPackage): 所属するパッケージ。
            isAbstract (bool): 抽象型とするか。

        Returns:
            IClass: 生成したクラス。
        """
        ...
    def RemoveClass(self, target: IClass) -> None:
        """
        指定したクラスを削除します。

        Args:
            target (IClass): 削除するクラス。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddProperty(self, owner: IClass, name: str, type: str, multiplicity: str) -> None:
        """
        指定したクラスに新しいプロパティを追加します。

        Args:
            owner (IClass): クラス。
            name (str): プロパティ名。
            type (str): プロパティの型。
            multiplicity (str): 多重度（ZeroOne | One | ZeroToMany | OneToMany）。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveProperty(self, owner: IClass, name: str) -> None:
        """
        指定したクラスのプロパティを削除します。

        Args:
            owner (IClass): クラス。
            name (str): プロパティ名。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Relate(self, name: str, source: IClass, sourceEndName: str, target: IClass, targetEndName: str, multiplicity: str) -> IRelationshipClass:
        """
        指定したクラス間を関連づけます。

        Args:
            name (str): 関連名。
            source (IClass): ソース側のクラス。
            sourceEndName (str): ソース側クラスの参照名。
            target (IClass): ターゲット側のクラス。
            targetEndName (str): ターゲット側クラスの参照名。
            multiplicity (str): 関連多重度（ManyToMany | OneToMany | ManyToOne）。

        Returns:
            IRelationshipClass: 関連クラス。
        """
        ...
    def UnRelate(self, name: str, source: IClass, target: IClass) -> None:
        """
        指定したクラス間の関連づけを削除します。

        Args:
            name (str): 関連名。
            source (IClass): ソース側のクラス。
            target (IClass): ターゲット側のクラス。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddSuperClasses(self, target: IClass, superClassNames: str, fuzzy: bool) -> None:
        """
        指定したクラスのスーパークラスを設定します。

        Args:
            target (IClass): クラス。
            superClassNames (str): スーパークラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddSuperClasses(self, target: IClass, scope: IPackage, superClassNames: str, fuzzy: bool) -> None:
        """
        指定したクラスのスーパークラスを設定します。
        設定するスーパークラスは、スコープで指定したパッケージの配下から探索します。

        Args:
            target (IClass): クラス。
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            superClassNames (str): スーパークラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddSuperClasses(self, target: IClass, superClasses: Iterable[IClass]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RemoveSuperClasses(self, target: IClass, superClassNames: str, fuzzy: bool) -> None:
        """
        指定したクラスのスーパークラスを削除します。
        指定したスーパークラス名の列挙のうち、指定したクラスのスーパークラスに含まれないクラスはスキップされます。
        クラスの継承関係を削除すると継承先クラスのモデルも削除します。

        Args:
            target (IClass): クラス。
            superClassNames (str): スーパークラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RemoveSuperClasses(self, target: IClass, scope: IPackage, superClassNames: str, fuzzy: bool) -> None:
        """
        指定したクラスのスーパークラスを削除します。
        削除するスーパークラスは、スコープで指定したパッケージの配下から探索します。
        指定したスーパークラス名の列挙のうち、指定したクラスのスーパークラスに含まれないクラスはスキップされます。
        クラスの継承関係を削除すると継承先クラスのモデルも削除します。

        Args:
            target (IClass): クラス。
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            superClassNames (str): スーパークラス名（カンマ区切りで複数指定可能）。
            fuzzy (bool): あいまい一致オプション。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RemoveSuperClasses(self, target: IClass, superClasses: Iterable[IClass]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def NewEnum(self, name: str, values: str, owner: IPackage) -> IEnum:
        """
        新しい列挙型を生成します。

        Args:
            name (str): 列挙型名。
            values (str): リテラル名（カンマ区切りで複数指定可能）。
            owner (IPackage): 所属するパッケージ。

        """
        ...
    @overload
    def NewEnum(self, name: str, values: Iterable[str], owner: IPackage) -> IEnum: ...
    def RemoveEnum(self, target: IEnum) -> None:
        """
        指定した列挙型を削除します。

        Args:
            target (IEnum): 削除する列挙型。

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddLiteral(self, owner: IEnum, literal: str) -> None:
        """
        指定した列挙型に、指定したリテラル文字列で新しい列挙型リテラルを追加します。

        Args:
            owner (IEnum): 列挙型。
            literal (str): リテラル文字列。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveLiteral(self, owner: IEnum, literal: str) -> None:
        """
        指定した列挙型の列挙型リテラルを削除します。

        Args:
            owner (IEnum): 列挙型。
            literal (str): 削除対象リテラル文字列。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddPathConstraint(self, name: str, className: str, targetFieldName: str, paths: str) -> IConstraint:
        """
        指定したクラスの指定したフィールドにパス制約を追加します。

        Args:
            name (str): 制約名。
            className (str): 制約の有効範囲となるクラス名。
            targetFieldName (str): 制約の対象フィールド名。
            paths (str): パス文字列（複数パスを指定する場合は';'（セミコロン）で区切り）。

        """
        ...
    @overload
    def AddPathConstraint(self, name: str, scope: IPackage, className: str, targetFieldName: str, paths: str) -> IConstraint:
        """
        指定したクラスの指定したフィールドにパス制約を追加します。
        指定クラスは、スコープで指定したパッケージの配下から探索します。

        Args:
            name (str): 制約名。
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): 制約の有効範囲となるクラス名。
            targetFieldName (str): 制約の対象フィールド名。
            paths (str): パス文字列（複数パスを指定する場合は';'（セミコロン）で区切り）。

        """
        ...
    @overload
    def AddPathConstraint(self, name: str, scope: IClass, targetField: IField, paths: str) -> IConstraint:
        """
        指定したクラスの指定したフィールドにパス制約を追加します。

        Args:
            name (str): 制約名。
            scope (IClass): 制約の有効範囲となるクラス。
            targetField (IField): 制約の対象フィールド。
            paths (str): パス文字列（複数パスを指定する場合は';'（セミコロン）区切り）。

        """
        ...
    @overload
    def RemovePathConstraint(self, className: str, targetFieldName: str) -> None:
        """
        指定したクラスの指定したフィールドのパス制約を削除します。

        Args:
            className (str): 制約の有効範囲となるクラス名。
            targetFieldName (str): 制約の対象フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RemovePathConstraint(self, scope: IPackage, className: str, targetFieldName: str) -> None:
        """
        指定したクラスの指定したフィールドのパス制約を削除します。
        指定クラスは、スコープで指定したパッケージの配下から探索します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): 制約の有効範囲となるクラス名。
            targetFieldName (str): 制約の対象フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RemovePathConstraint(self, scope: IClass, targetField: IField) -> None:
        """
        指定したクラスの指定したフィールドのパス制約を削除します。

        Args:
            scope (IClass): 制約の有効範囲となるクラス。
            targetField (IField): 制約の対象フィールド。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveConstraint(self, constraint: IConstraint) -> None:
        """
        指定した制約を削除します。
        削除する制約。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveConstraints(self, constraints: Iterable[IConstraint]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetFieldCallback(self, className: str, fieldName: str, getter: Callable, counter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetFieldCallback(self, scope: IPackage, className: str, fieldName: str, getter: Callable, counter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetFieldCallback(self, target: IClass, fieldName: str, getter: Callable, counter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterSetFieldCallback(self, className: str, fieldName: str, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterSetFieldCallback(self, scope: IPackage, className: str, fieldName: str, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterSetFieldCallback(self, target: IClass, fieldName: str, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterRelateFieldCallback(self, className: str, fieldName: str, relate: Callable, unrelate: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterRelateFieldCallback(self, scope: IPackage, className: str, fieldName: str, relate: Callable, unrelate: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterRelateFieldCallback(self, target: IClass, fieldName: str, relate: Callable, unrelate: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnregisterFieldCallback(self, className: str, fieldName: str) -> None:
        """
        指定したクラスの指定したフィールドに対する全てのコールバック関数を登録を解除します。

        Args:
            className (str): クラス名（完全修飾名）。
            fieldName (str): フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnregisterFieldCallback(self, scope: IPackage, className: str, fieldName: str) -> None:
        """
        スコープで指定したパッケージの配下の指定したクラスの指定したフィールドに対する全てのコールバック関数を登録を解除します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fieldName (str): フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnregisterFieldCallback(self, target: IClass, fieldName: str) -> None:
        """
        指定したクラスの指定したフィールドに対する全てのコールバック関数を登録を解除します。

        Args:
            target (IClass): クラス。
            fieldName (str): フィールド名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddMethod(self, className: str, methodName: str, methodBody: str) -> None:
        """
        指定されたメタクラスに指定された揮発性メソッドを追加します。

        Args:
            className (str): クラス名。
            methodName (str): メソッド名。
            methodBody (str): メソッド本体名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddMethod(self, classNames: Iterable[str], methodName: str, methodBody: str) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def AllPackages(self) -> IPackageCollection:
        """パッケージ一覧を取得します。"""
        ...
    @property
    def AllClasses(self) -> IClassCollection:
        """クラス一覧を取得します。"""
        ...
    @property
    def AllEnums(self) -> IEnumCollection:
        """列挙型一覧を取得します。"""
        ...

class IMethod:
    """
    メソッドを表します。
    """
    def Invoke(self, _this: IModel, args: IParams) -> Any:
        """
        指定されたモデルでこのメソッドを実行します。

        Args:
            _this (IModel): 対象のモデル
            args (IParams): パラメータ

        Returns:
            Any: メソッド実行結果
        """
        ...

class IMethodCollection:
    """
    メソッドのコレクションです。
    """
    def GetItem(self, index: int) -> IMethod:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IMethod: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IMethodEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IMethodEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IMethod]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IMethodEnumerator:
    """
    メソッドのコレクションの列挙子です。
    """
    ...

class INamedElementCollection:
    """
    名前付け可能要素のコレクションです。
    """
    def GetItem(self, index: int) -> INamedElement:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            INamedElement: コレクション要素
        """
        ...
    def GetEnumerator(self) -> INamedElementEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            INamedElementEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[INamedElement]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class INamedElementEnumerator:
    """
    名前付け可能要素のコレクションの列挙子です。
    """
    ...

class IPackage(INamedElement):
    """
    パッケージを表します。
    """
    def GetAllSubPackages(self) -> IPackageCollection:
        """
        このパッケージを基点にネストする全てのサブパッケージを取得します。
        ※このパッケージは含まれません。

        Returns:
            IPackageCollection: サブパッケージ。
        """
        ...
    def GetOwnerPackages(self) -> IPackageCollection:
        """
        このパッケージを基点に親方向に探索できる全てのパッケージを取得します。
        パッケージの順序は、最も近い親を先頭に、プロファイルのルートパッケージが末尾となります。

        Returns:
            IPackageCollection: パッケージ一覧。
        """
        ...
    def GetAllTypes(self) -> ITypeCollection:
        """
        このパッケージを基点にネストするパッケージを含めて定義されている型の一覧を取得します。
        ※このパッケージが直接管理する型も含まれます。

        Returns:
            ITypeCollection: 型一覧。
        """
        ...
    def GetAllClasses(self) -> IClassCollection:
        """
        このパッケージを基点にネストするパッケージを含めて定義されているクラスの一覧を取得します。
        ※このパッケージが直接管理するクラスも含まれます。

        Returns:
            IClassCollection: クラス一覧。
        """
        ...
    def GetAllEnums(self) -> IEnumCollection:
        """
        このパッケージを基点にネストするパッケージを含めて定義されている列挙型の一覧を取得します。
        ※このパッケージが直接管理する列挙型も含まれます。

        Returns:
            IEnumCollection: 列挙型一覧。
        """
        ...
    def GetTypeByName(self, typeName: str, recursive: bool) -> Any: ...
    @overload
    def GetTypesByName(self, typeNames: str, recursive: bool) -> Iterable[Any]: ...
    @overload
    def GetTypesByName(self, typeNames: Iterable[str], recursive: bool) -> Iterable[Any]: ...
    @property
    def Uri(self) -> str:
        """名前空間を取得します。"""
        ...
    @property
    def FullName(self) -> str:
        """完全修飾名を取得します。"""
        ...
    @property
    def Parent(self) -> IPackage:
        """親パッケージを取得します。"""
        ...
    @property
    def SubPackages(self) -> IPackageCollection:
        """サブパッケージ一覧を取得します。"""
        ...
    @property
    def OwnedTypes(self) -> ITypeCollection:
        """このパッケージが直接管理する型（IClass, IEnum）の一覧を取得します。"""
        ...
    @property
    def OwnedClasses(self) -> IClassCollection:
        """管理クラス一覧を取得します。"""
        ...
    @property
    def OwnedEnums(self) -> IEnumCollection:
        """管理する列挙型の一覧を取得します。"""
        ...
    @property
    def ProfileReference(self) -> IProfileReference:
        """このパッケージが参照しているプロファイル参照情報を取得します。
自身がプロファイル参照パッケージではない場合、 null を返します。"""
        ...

class IPackageCollection:
    """
    パッケージのコレクションです。
    """
    def GetItem(self, index: int) -> IPackage:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IPackage: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IPackageEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IPackageEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IPackage]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IPackageEnumerator:
    """
    パッケージのコレクションの列挙子です。
    """
    ...

class IParams:
    """
    メソッドパラメータを表します。
    """
    def AddParam(self, name: str, value: Any) -> None:
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
    @overload
    def __getitem__(self, index: int) -> Any: ...
    @overload
    def __getitem__(self, name: str) -> Any: ...

class IProfile:
    """
    プロファイル情報へのアクセスオブジェクトを表します。
    """
    def GetProfileReferencePackageFor(self, element: INamedElement) -> IPackage:
        """
        指定したプロファイル要素が所属するプロファイル参照パッケージを取得します。
        指定したプロファイル要素がプロファイル参照パッケージに所属していない場合、 プロファイルのルートパッケージを返します。

        Args:
            element (INamedElement): プロファイル要素。

        Returns:
            IPackage: プロファイル参照パッケージ。
        """
        ...
    @property
    def Name(self) -> str:
        """プロファイルの名前を取得、または設定します。"""
        ...
    @property
    def DisplayName(self) -> str:
        """プロファイルの表示名を取得、または設定します。"""
        ...
    @property
    def Description(self) -> str:
        """プロファイルの説明を取得、または設定します。"""
        ...
    @property
    def Version(self) -> str:
        """プロファイルのバージョンを取得、または設定します。"""
        ...
    @property
    def Category(self) -> str:
        """プロファイルのカテゴリを取得、または設定します。"""
        ...
    @property
    def Path(self) -> str:
        """プロファイルのパスを取得します。"""
        ...
    @property
    def Metamodels(self) -> IMetamodels:
        """メタモデル管理を取得します。"""
        ...
    @property
    def ViewDefinitions(self) -> IViewDefinitions:
        """ビュー定義管理を取得します。"""
        ...
    @property
    def ProfileUnit(self) -> IModelUnit:
        """このプロファイルを管理するユニット情報を取得します。"""
        ...
    @property
    def RootPackage(self) -> IPackage:
        """ルートパッケージを取得します。"""
        ...

class IProfileDependency:
    """
    プロファイルの依存情報です。
    """
    @property
    def Name(self) -> str:
        """名前を取得します。"""
        ...
    @property
    def Version(self) -> str:
        """バージョンを取得します。"""
        ...

class IProfileDependencyCollection:
    """
    プロファイルの依存情報のコレクションです。
    """
    def GetItem(self, index: int) -> IProfileDependency:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IProfileDependency: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IProfileDependencyEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IProfileDependencyEnumerator: Enumerator。
        """
        ...
    def __iter__(self) -> Iterator[IProfileDependency]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IProfileDependencyEnumerator:
    """
    プロファイルの依存情報のコレクションの列挙子です。
    """
    ...

class IProfileReference:
    """
    プロファイル参照情報です。
    Name と Version が一致するプロファイル参照は同一として判定されます。
    """
    @property
    def Name(self) -> str:
        """名前を取得します。"""
        ...
    @property
    def DisplayName(self) -> str:
        """表示名を取得します。"""
        ...
    @property
    def Description(self) -> str:
        """説明を取得します。"""
        ...
    @property
    def Version(self) -> str:
        """バージョンを取得します。"""
        ...
    @property
    def Category(self) -> str:
        """カテゴリを取得します。"""
        ...
    @property
    def Dependencies(self) -> IProfileDependencyCollection:
        """依存プロファイルの一覧を取得します。"""
        ...

class IProfileReferenceCollection:
    """
    プロファイル参照情報のコレクションです。
    """
    def GetItem(self, index: int) -> IProfileReference:
        """
        インデックスで指定されたコレクションの要素を取得します。

        Args:
            index (int): インデックス。

        Returns:
            IProfileReference: コレクション要素。
        """
        ...
    def GetEnumerator(self) -> IProfileReferenceEnumerator:
        """
        コレクションを反復処理する列挙子を取得します。

        Returns:
            IProfileReferenceEnumerator: Enumerator。
        """
        ...
    def __iter__(self) -> Iterator[IProfileReference]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します。"""
        ...

class IProfileReferenceEnumerator:
    """
    プロファイル参照情報のコレクションの列挙子です。
    """
    ...

class IRelationshipClass(IClass):
    """
    関連クラス情報へのアクセスオブジェクトを表します。
    """
    @property
    def Source(self) -> IClass:
        """関連元クラス"""
        ...
    @property
    def Target(self) -> IClass:
        """関連先クラス"""
        ...
    @property
    def SourceField(self) -> IField:
        """関連元に対する関連端フィールド
このフィールドは、関連先クラスのフィールドとなります。"""
        ...
    @property
    def TargetField(self) -> IField:
        """関連先に対する関連端フィールド
このフィールドは、関連元クラスのフィールドとなります。"""
        ...
    @property
    def IsEmbedded(self) -> bool:
        """所有関連か"""
        ...
    @property
    def IsReference(self) -> bool:
        """参照関連か"""
        ...
    @property
    def IsDerivation(self) -> bool:
        """導出関連か"""
        ...
    @property
    def IsTwoWay(self) -> bool:
        """双方向関連か"""
        ...

class IStyleProperty:
    """
    スタイル属性情報オブジェクトを表します。
    """
    @property
    def Attribute(self) -> StyleAttributes:
        """対象のスタイル属性"""
        ...
    @property
    def OwnerDef(self) -> IElementDef:
        """スタイルのオーナ定義。
ラベル/テキストの場合は、その所有シェイプとなります。
コンパートメントアイテムの場合は、その所有シェイプとなります。"""
        ...
    @property
    def DefinitionValue(self) -> Any:
        """ビュー定義上のスタイル値"""
        ...
    @property
    def CurrentValue(self) -> Any:
        """現在のVIでのスタイル値"""
        ...

class ITag:
    """
    タグを表します。
    """
    @property
    def Key(self) -> str:
        """タグ名"""
        ...
    @property
    def Value(self) -> str:
        """値"""
        ...

class ITagCollection:
    """
    タグのコレクションです。
    """
    def GetItem(self, index: int) -> ITag:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ITag: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITagEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITagEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ITag]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITagEnumerator:
    """
    タグのコレクションの列挙子です。
    """
    ...

class ITypeCollection:
    """
    型のコレクションです。
    """
    def GetItem(self, index: int) -> IType:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IType: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ITypeEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ITypeEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IType]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ITypeEnumerator:
    """
    型のコレクションの列挙子です。
    """
    ...

class IViewDefinitions:
    """
    ビュー定義管理オブジェクトを表します。
    """
    @overload
    def FindEditorDefByClass(self, modelClass: IClass, name: str) -> IEditorDefCollection:
        """
        指定したクラスに定義されたエディタのビュー定義を検索します。

        Args:
            modelClass (IClass): モデルクラス。
            name (str): エディタ名。

        Returns:
            IEditorDefCollection: エディタ定義一覧。
        """
        ...
    @overload
    def FindEditorDefByClass(self, modelClassName: str, fuzzy: bool, editorName: str) -> IEditorDefCollection:
        """
        指定したクラスに定義されたエディタのビュー定義を検索します。

        Args:
            modelClassName (str): モデルクラス名。
            fuzzy (bool): あいまい一致オプション。
            editorName (str): エディタ名。

        Returns:
            IEditorDefCollection: エディタ定義一覧。
        """
        ...
    @overload
    def FindElementDefByClass(self, editor: IEditorDef, modelClass: IClass, name: str) -> IElementDefCollection:
        """
        指定したエディタ定義から指定したモデルクラスに対応するエディタ要素定義を検索します。

        Args:
            editor (IEditorDef): エディタ定義。
            modelClass (IClass): モデルクラス。
            name (str): エディタ要素名。

        Returns:
            IElementDefCollection: エディタ定義一覧。
        """
        ...
    @overload
    def FindElementDefByClass(self, editor: IEditorDef, modelClassName: str, fuzzy: bool, elementName: str) -> IElementDefCollection:
        """
        指定したエディタ定義から指定したモデルクラスに対応するエディタ要素定義を検索します。

        Args:
            editor (IEditorDef): エディタ定義。
            modelClassName (str): モデルクラス名。
            fuzzy (bool): あいまい一致オプション。
            elementName (str): エディタ要素定義名。

        Returns:
            IElementDefCollection: エディタ要素定義一覧。
        """
        ...
    def NewEditorDef(self, name: str, modelClass: IClass, type: str) -> IEditorDef:
        """
        指定したモデルクラスのエディタ定義を生成します。

        Args:
            name (str): エディタ名。
            modelClass (IClass): モデルクラス。
            type (str): エディタ種類。

        Returns:
            IEditorDef: エディタ定義。
        """
        ...
    def NewCustomEditorDef(self, name: str, modelClass: IClass, customEditorTypeId: str) -> ICustomEditorDefinition:
        """
        指定したモデルクラスのカスタムエディタ定義を生成します。

        Args:
            name (str): エディタ名。
            modelClass (IClass): モデルクラス。
            customEditorTypeId (str): カスタムエディタの種類識別子。

        Returns:
            ICustomEditorDefinition: カスタムエディタ定義。
        """
        ...
    def NewElementDef(self, editor: IEditorDef, name: str, modelClass: IClass, type: str, path: str, parent: IElementDef) -> IElementDef:
        """
        指定したモデルクラスのエディタ要素定義を生成します。

        Args:
            editor (IEditorDef): 対象エディタ。
            name (str): エディタ要素名。
            modelClass (IClass): モデルクラス。
            type (str): エディタ要素種類。
            path (str): フィールド。
            parent (IElementDef): 親エディタ要素。

        Returns:
            IElementDef: エディタ要素定義。
        """
        ...
    def NewCustomElementDef(self, editor: ICustomEditorDefinition, name: str, modelClass: IClass, elementTypeId: str, path: str) -> ICustomElementDefinition:
        """
        指定したモデルクラスのカスタムエディタ要素定義を生成します。

        Args:
            editor (ICustomEditorDefinition): 対象カスタムエディタ。
            name (str): エディタ要素名。
            modelClass (IClass): モデルクラス。
            elementTypeId (str): エディタ要素種類識別子。
            path (str): フィールド。

        Returns:
            ICustomElementDefinition: カスタムエディタ要素定義。
        """
        ...
    @overload
    def RegisterGetStyleCallback(self, elementDef: IElementDef, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetStyleCallback(self, editorModelClassName: str, elementModelClassName: str, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetStyleCallback(self, elementDef: IElementDef, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetStyleCallback(self, editorModelClassName: str, elementModelClassName: str, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetTextStyleCallback(self, elementDef: IElementDef, type: TextTypes, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetTextStyleCallback(self, editorModelClassName: str, elementModelClassName: str, type: TextTypes, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetTextStyleCallback(self, elementDef: IElementDef, type: TextTypes, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetTextStyleCallback(self, editorModelClassName: str, elementModelClassName: str, type: TextTypes, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetCompartmentItemTextStyleCallback(self, elementDef: IElementDef, areaPath: str, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetCompartmentItemTextStyleCallback(self, editorModelClassName: str, elementModelClassName: str, areaPath: str, getter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetCompartmentItemTextStyleCallback(self, elementDef: IElementDef, areaPath: str, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterGetCompartmentItemTextStyleCallback(self, editorModelClassName: str, elementModelClassName: str, areaPath: str, getter: Callable, *properties: List[List[StyleAttributes]]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterTextValueCallback(self, elementDef: IElementDef, type: TextTypes, getter: Callable, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterTextValueCallback(self, editorModelClassName: str, elementModelClassName: str, type: TextTypes, getter: Callable, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterCompartmentItemTextValueCallback(self, elementDef: IElementDef, areaPath: str, getter: Callable, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def RegisterCompartmentItemTextValueCallback(self, editorModelClassName: str, elementModelClassName: str, areaPath: str, getter: Callable, setter: Callable) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnregisterStyleCallback(self, elementDef: IElementDef) -> None:
        """
        指定したエディタ要素定義より生成されるエディタ要素の全てのコールバック関数を登録解除します。

        Args:
            elementDef (IElementDef): エディタ要素定義。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def UnregisterStyleCallback(self, editorModelClassName: str, elementModelClassName: str) -> None:
        """
        指定したクラスから特定できるエディタ要素定義より生成されるエディタ要素の全てのコールバック関数を登録解除します。

        Args:
            editorModelClassName (str): エディタのモデルクラス名。
            elementModelClassName (str): エディタ要素のモデルクラス名。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Editors(self) -> IEditorDefCollection:
        """エディタ定義一覧を取得します。"""
        ...

class StyleAttributes(IntEnum):
    """
    設定できるスタイル属性の列挙です。
    """
    Icon = 0  # アイコン
    ShowIcon = 1  # アイコンを表示するか
    BackColor = 2  # 背景色
    ForeColor = 3  # 前景色
    BorderColor = 4  # ボーダー色
    BorderThickness = 5  # ボーダーの厚さ
    BorderStyle = 6  # 線のスタイル
    Figure = 7  # 形状
    Image = 8  # 画像
    ConnectorType = 9  # コネクタの種類
    StartPointFigure = 10  # 開始地点の形状
    EndPointFigure = 11  # 終了地点の形状
    FontSize = 12  # フォントサイズ
    FontFamily = 13  # フォントファミリ
    IsUnderline = 14  # 下線かどうか
    IsItalic = 15  # イタリックかどうか
    IsBold = 16  # ボールドかどうか
    DecorateStrikeThrough = 17  # 取り消し線かどうか

class TextTypes(IntEnum):
    """
    テキスト識別用の列挙です。
    """
    Title = 0  # タイトル
    Body = 1  # ボディ
    Category = 2  # カテゴリ
    Label0 = 3  # ラベル（1件目）
    Label1 = 4  # ラベル（2件目）
    Label2 = 5  # ラベル（3件目）
    Label3 = 6  # ラベル（4件目）
    Label4 = 7  # ラベル（5件目）
    Label5 = 8  # ラベル（6件目）
    Label6 = 9  # ラベル（7件目）
    Label7 = 10  # ラベル（8件目）
    Label8 = 11  # ラベル（9件目）
    Label9 = 12  # ラベル（10件目）

class IModelUnit:
    """
    モデルユニット情報を表します。
    """
    @property
    def Name(self) -> str:
        """ユニット名"""
        ...
    @property
    def Type(self) -> str:
        """ユニット種別 {\"Project\",\"Model\",\"Profile\",\"Library\",\"IndexCache\",\"Unknown\"}"""
        ...
    @property
    def TopElementId(self) -> str:
        """このユニットにおける基点要素の識別子。
基点要素がない場合は null を返します。
通常、基点要素はユニット種別により次の要素となります。
\"Project\" : プロジェクト
\"Model\" : ユニットに分割したモデル
\"Profile\" : プロファイル
上記以外 : なし"""
        ...
    @property
    def UnitPath(self) -> str:
        """ユニットパス。
通常はプロジェクトフォルダからの相対パス、
プロジェクトフォルダ外のユニットの場合は絶対パスとなります。"""
        ...
    @property
    def AbsolutePath(self) -> str:
        """物理ファイルの絶対パス"""
        ...
    @property
    def IsExternalUnit(self) -> bool:
        """このユニットが外部ユニットであるか。
外部ユニットは、参照登録によって追加され、プロジェクトフォルダ外で管理されます。"""
        ...
    @property
    def PhysicalFileExits(self) -> bool:
        """このユニットに対応する物理ファイルが存在するか"""
        ...
    @property
    def IsReadonly(self) -> bool:
        """このユニットが読み取り専用ユニットであるか"""
        ...
    @property
    def Loaded(self) -> bool:
        """このユニットの内容がプロジェクトに読み込み済みであるか"""
        ...
    @property
    def HasLoadError(self) -> bool:
        """このユニットの読み込みエラー有無"""
        ...
    @property
    def ScmStatus(self) -> IScmFileStatus:
        """構成管理状態"""
        ...

class IModelUnitCollection:
    """
    モデルユニット情報コレクションです。
    """
    def GetItem(self, index: int) -> IModelUnit:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IModelUnit: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IModelUnitEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IModelUnitEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IModelUnit]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IModelUnitEnumerator:
    """
    モデルユニット情報の列挙子です。
    """
    ...

class IProject(IModel):
    """
    プロジェクト情報へのアクセスオブジェクトを表します。
    """
    def ImportProfile(self, profilePath: str) -> None:
        """
        指定されたパスのプロファイルをインポートします。

        Args:
            profilePath (str): プロファイルのパス

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddNewRootModel(self, className: str, fuzzy: bool) -> IModel:
        """
        プロジェクトに指定したクラスの新しいモデルを追加します。

        Args:
            className (str): クラス名
            fuzzy (bool): あいまい一致オプション

        Returns:
            IModel: 追加したモデル
        """
        ...
    @overload
    def AddNewRootModel(self, scope: IPackage, className: str, fuzzy: bool) -> IModel:
        """
        プロジェクトに指定したクラスの新しいモデルを追加します。
        指定クラスは、スコープで指定したパッケージ配下から特定します。

        Args:
            scope (IPackage): スコープ(探索範囲の基点となるパッケージ)。
            className (str): クラス名。
            fuzzy (bool): あいまい一致オプション

        Returns:
            IModel: 追加したモデル。
        """
        ...
    def GetModelById(self, identifier: str) -> IModel:
        """
        このプロジェクトから指定された識別子のモデルを取得します。
        指定されたモデルが見つからない場合は null を返します。
        なお、この呼び出しでは、関連は取得できません。
        関連を取得する場合は、を使用してください。

        Args:
            identifier (str): モデルの識別子

        Returns:
            IModel: 指定された識別子のモデル
        """
        ...
    def GetRelationshipById(self, identifier: str) -> IRelationship:
        """
        このプロジェクトから指定された識別子の関連を取得します。
        指定された関連が見つからない場合は null を返します。

        Args:
            identifier (str): 関連の識別子

        Returns:
            IRelationship: 指定された識別子の関連
        """
        ...
    @overload
    def GetModelByPath(self, path: str) -> IModel:
        """
        このプロジェクトから指定されたモデル階層パスのモデルを取得します。
        指定したモデル階層パスのモデルが存在しない場合は null を返します。
        なお、一致するモデル階層パスが複数ある場合、一番最初に見つかったモデルを返します。

        Args:
            path (str): モデル階層パス

        Returns:
            IModel: 指定されたパスのモデル
        """
        ...
    @overload
    def GetModelByPath(self, baseElementId: str, elementPath: str) -> IModel:
        """
        指定されたモデルIdを持つモデルを基点とした、指定された相対パスのモデルを取得します。
        指定したモデル階層パスのモデルが存在しない場合は null を返します。
        なお、一致するモデル階層パスが複数ある場合、一番最初に見つかったモデルを返します。

        Args:
            baseElementId (str): 探索の基点となるモデルId
            elementPath (str): baseElementId で指定したモデルとの相対パス

        Returns:
            IModel: 指定されたパスのモデル
        """
        ...
    def HasUnsavedChanges(self) -> bool:
        """
        未保存の変更があるかを調べます。

        Returns:
            bool: 未保存の変更がある場合は true、それ以外は false です。
        """
        ...
    def CreateProductLineModel(self) -> None:
        """
        このプロジェクトにプロダクトライン開発支援モデルを作成し、プロダクトライン開発可能とします。
        プロダクト開発支援モデルを作成することで、次のモデルが生成されます。
        - プロダクト開発支援モデル
        - 空のフィーチャモデル
        - 空のコンフィグレーションモデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def BeginEdit(self) -> None:
        """
        編集開始を指示します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def EndEdit(self) -> None:
        """
        編集終了を指示します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def BeginUndoTransaction(self, autoCommit: bool) -> IUndoTransaction:
        """
        編集を開始して、アンドゥトランザクションを生成します。
        アンドゥトランザクション内で実施された編集内容は、1回のアンドゥ/リドゥ操作の対象となります。

        Args:
            autoCommit (bool): トランザクション破棄時にCommitを行うか。false時は RollBack が行われます。

        Returns:
            IUndoTransaction: アンドゥトランザクション
        """
        ...
    def GetUndoSuspendScope(self) -> Any:
        """
        アンドゥをサスペンドするスコープを取得します。

        Returns:
            Any: アンドゥをサスペンドするスコープ
        """
        ...
    def Undo(self) -> None:
        """
        直近の編集操作を取り消します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Redo(self) -> None:
        """
        直近で取り消された編集操作を再実行します。

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
    def SuspendModelVerification(self) -> Any:
        """
        モデルの編集可否検証をサスペンドするスコープを取得します。

        Returns:
            Any: モデルの編集可否検証をサスペンドするスコープ
        """
        ...
    def CreateModelAccessPolicy(self) -> IModelAccessPolicy:
        """
        モデルアクセスのポリシーを作成します。

        Returns:
            IModelAccessPolicy: モデルアクセスポリシー
        """
        ...
    def ImportUnitFromJson(self, unitJson: str, owner: IModel, field: str) -> IUnitImportResult:
        """
        モデル情報をユニットファイルのJSON形式でインポートします。
        プロジェクトファイルがsqlite/jsonのどちらであっても動作します。

        Args:
            unitJson (str): ユニットファイル構造のJSON形式
            owner (IModel): インポート先のモデル
ownerが!= nullの場合はfieldの子要素としてTopElementIdのモデルを追加します。
ownerがnullの場合はTopElementIdの値は無視するので自前で他モデルとの所有や参照関連を追加する必要があります。
            field (str): 追加先のフィールド

        """
        ...
    @property
    def Path(self) -> str:
        """プロジェクトのパス"""
        ...
    @property
    def Profile(self) -> IProfile:
        """プロファイル"""
        ...
    @property
    def ProductLineModel(self) -> IProductLineModel:
        """プロダクトライン開発支援モデル"""
        ...
    @property
    def IsProductLineSupported(self) -> bool:
        """このプロジェクトでプロダクトライン開発がサポートされているか"""
        ...
    @property
    def OutputModelPaths(self) -> bool:
        """永続化時に参照先モデルのパスを出力するかを取得、または設定します。"""
        ...
    @property
    def UnitManager(self) -> IProjectUnitManager:
        """プロジェクトユニット情報マネージャ"""
        ...
    @property
    def CanUndo(self) -> bool:
        """アンドゥ操作が実行可能であるか調べます。"""
        ...
    @property
    def CanRedo(self) -> bool:
        """リドゥ操作が実行可能であるか調べます。"""
        ...
    @property
    def EditingCapabilityProviderRegistry(self) -> Any:
        """編集支援機能レジストリを取得します。"""
        ...
    @property
    def DesignModel(self) -> IModel:
        """設計モデルルート (モデルナビゲータのルートモデル) を取得します。"""
        ...

class IProjectUnitManager:
    """
    プロジェクトの物理ファイル構成管理オブジェクトを表します。
    """
    @overload
    def SplitModelUnit(self, model: IModel, unitName: str) -> None:
        """
        指定されたモデルを指定された名前のユニットファイルに分割します。

        Args:
            model (IModel): モデル
            unitName (str): ユニットファイル名

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SplitModelUnit(self, model: IModel, unitName: str, folderPath: str) -> None:
        """
        指定されたモデルを指定された名前のユニットファイルに分割します。
        分割するユニットファイルは、指定されたフォルダへ追加されます。

        Args:
            model (IModel): モデル
            unitName (str): ユニットファイル名
            folderPath (str): 分割先フォルダの相対パス(Modelsフォルダからの相対パス)。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SplitModelUnits(self, models: Iterable[IModel]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def SplitModelUnits(self, models: Iterable[IModel], folderPath: str) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def UnifyModelUnit(self, unit: IModelUnit, deleteUnitFile: bool) -> None:
        """
        指定されたユニットを親ユニットに統合します。

        Args:
            unit (IModelUnit): ユニット
            deleteUnitFile (bool): ユニットファイルを削除するか

        Returns:
            None: This method does not return a value.
        """
        ...
    def UnifyModelUnits(self, units: Iterable[IModelUnit], deleteUnitFile: bool) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def ImportModelUnits(self, unitFilePaths: Iterable[str]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def ImportModelUnits(self, unitFilePaths: Iterable[str], folderPath: str) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def AddExternalUnits(self, unitFilePaths: Iterable[str]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def ExportModelUnit(self, unit: IModelUnit, exportFilePath: str) -> None:
        """
        指定されたモデルユニットを指定したファイルパスでエクスポートします。

        Args:
            unit (IModelUnit): ユニット
            exportFilePath (str): エクスポート先ファイルパス

        Returns:
            None: This method does not return a value.
        """
        ...
    def ExportModelUnits(self, units: Iterable[IModelUnit], exportFolderPath: str) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def ProjectUnit(self) -> IModelUnit:
        """このプロジェクトのユニット（物理ファイル）情報。
プロジェクトを保存していない場合は null を返します。"""
        ...
    @property
    def ModelUnits(self) -> IModelUnitCollection:
        """このプロジェクトで管理するモデルユニット情報。
※プロジェクトユニットは含まれません。
プロジェクトの管理ユニットがない場合は空のコレクションを返します。"""
        ...

class IUndoTransaction:
    """
    アンドゥトランザクションを表します。
    """
    def Commit(self) -> None:
        """
        トランザクションをコミットします。

        Returns:
            None: This method does not return a value.
        """
        ...
    def Rollback(self) -> None:
        """
        トランザクションをロールバックします

        Returns:
            None: This method does not return a value.
        """
        ...

class IUnitImportError:
    """
    JSON形式ユニットインポートのエラー情報です。
    """
    @property
    def Kind(self) -> UnitImportErrorKind:
        """ユニットインポートのエラー種別を取得します。"""
        ...
    @property
    def TargetElementID(self) -> str:
        """インポートした対象のIdを取得します。"""
        ...
    @property
    def TargetElementType(self) -> str:
        """インポートした対象の種別を取得します。"""
        ...
    @property
    def Message(self) -> str:
        """メッセージを取得します。"""
        ...

class IUnitImportResult:
    """
    JSON形式のユニットインポートの結果です。
    """
    @property
    def State(self) -> str:
        """インポート処理のステータスを取得します。"""
        ...
    @property
    def TopElement(self) -> IModel:
        """指定したJSONで定義された最上位要素として取り込まれたモデルを取得します。"""
        ...
    @property
    def ImportedModels(self) -> IModelCollection:
        """指定したJSONからインポートされたエンティティの一覧を取得します。"""
        ...
    @property
    def ImportedRelations(self) -> IRelationshipCollection:
        """指定したJSONからインポートされた関連の一覧を取得します。"""
        ...
    @property
    def ImportedEditors(self) -> IEditorCollection:
        """指定したJSONからインポートされたエディタの一覧を取得します。"""
        ...
    @property
    def Errors(self) -> Iterable[IUnitImportError]:
        """インポート処理におけるエラー情報の一覧を取得します。
読み飛ばされたデータがある場合等にはこの一覧で取得できます。"""
        ...

class ProjectExtensions:
    """
    に関する拡張メソッド群です。
    """
    ...

class UnitImportErrorKind(IntEnum):
    """
    JSON形式のユニットインポートのエラー種別を指定します。
    """
    Error = 0  # エラー。
    Warning = 1  # 警告。
    Info = 2  # 情報。

class IInfoEntry:
    """
    エラー情報/検索結果情報の共通情報です。
    """
    def SetTag(self, tag: str, value: Any) -> None:
        """
        タグを設定できます。

        Args:
            tag (str): タグ。
            value (Any): タグに設定する値。

        Returns:
            None: This method does not return a value.
        """
        ...
    def GetTag(self, tag: str) -> Any:
        """
        タグを取得します。タグが存在しない場合はnullが戻ります。

        Args:
            tag (str): タグ。

        Returns:
            Any: タグに設定した値。
        """
        ...
    def HasTag(self, tag: str) -> bool:
        """
        タグが存在するかどうかを検証します。

        Args:
            tag (str): タグ。

        Returns:
            bool: タグが存在する場合は true 存在しない場合は false を返す。
        """
        ...
    def RemoveTag(self, tag: str) -> None:
        """
        タグを削除します。

        Args:
            tag (str): タグ。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Type(self) -> str:
        """タイプ
[エラーの場合]
\"Information\",\"Warning\",\"Error\",\"Summary\";
[検索結果の場合]
検索種別"""
        ...
    @property
    def Index(self) -> int:
        """エラー/検索対象のフィールドのインデックス（複数フィールドの場合、または、配列でなければ0）"""
        ...
    @property
    def Fields(self) -> str:
        """エラー/検索対象のフィールドを取得します。
複数フィールドが対象となった場合はカンマ区切りになります。"""
        ...
    @property
    def Model(self) -> IModel:
        """エラー/検索対象のモデル"""
        ...
    @property
    def Title(self) -> str:
        """タイトル"""
        ...
    @property
    def Category(self) -> str:
        """カテゴリ"""
        ...
    @property
    def Code(self) -> str:
        """コード"""
        ...
    @property
    def Message(self) -> str:
        """メッセージ"""
        ...
    @property
    def DetailMessage(self) -> str:
        """詳細メッセージ"""
        ...
    @property
    def NavigatingViewName(self) -> str:
        """確認が推奨されるビュー定義名(省略時はデフォルト挙動になります)"""
        ...
    @property
    def NavigatingEditor(self) -> IEditor:
        """確認が推奨されるエディタ(省略時はデフォルト挙動になります)"""
        ...
    @property
    def DisplayStyleName(self) -> str:
        """スタイル名（省略時は既定のスタイルが適用されます）"""
        ...
    @property
    def Tags(self) -> Iterable[Any]:
        """タグ。
タグが未設定の場合は空の列挙を返します。"""
        ...

class IError(IInfoEntry):
    """
    モデル検証によるエラー情報です。
    """
    ...

class IErrorCollection:
    """
    エラー情報のコレクションです。
    """
    def GetItem(self, index: int) -> IError:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IError: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IErrorEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IErrorEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IError]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IErrorEnumerator:
    """
    エラー情報のコレクションの列挙子です。
    """
    ...

class IErrors:
    """
    エラー一覧です。
    """
    def FindErrorByCategory(self, category: str) -> IErrorCollection:
        """
        指定されたカテゴリのエラー情報を検索します

        Args:
            category (str): カテゴリ

        Returns:
            IErrorCollection: エラー情報一覧
        """
        ...
    def FindErrorOfModelByCategory(self, model: IModel, category: str) -> IErrorCollection:
        """
        与えられたモデルの指定されたカテゴリのエラー情報を検索します

        Args:
            model (IModel): モデル
            category (str): カテゴリ

        Returns:
            IErrorCollection: エラー情報一覧
        """
        ...
    def ClearErrors(self) -> None:
        """
        すべてのエラー情報をクリアします

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearErrorsAt(self, model: IModel) -> None:
        """
        指定されたモデルのエラー情報をクリアします

        Args:
            model (IModel): モデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def AddErrors(self, errors: Iterable[IError]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveError(self, error: IError) -> None:
        """
        指定したエラー情報を削除します。
        既に削除済みのエラー情報を指定した場合は何も行いません。

        Args:
            error (IError): エラー情報。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveErrors(self, errors: Iterable[IError]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def AllErrors(self) -> IErrorCollection:
        """すべてのエラー情報"""
        ...
    @property
    def Errors(self) -> IErrorCollection:
        """エラー種別がerrorのエラー情報"""
        ...
    @property
    def Warnings(self) -> IErrorCollection:
        """エラー種別がwarningのエラー情報"""
        ...
    @property
    def Informations(self) -> IErrorCollection:
        """エラー種別がinformationのエラー情報"""
        ...
    @property
    def Summaries(self) -> IErrorCollection:
        """エラー種別がSummaryのエラー情報"""
        ...

class IInfoEntryCollection:
    """
    エラー情報/検索結果情報の共通情報のコレクションです。
    """
    def GetItem(self, index: int) -> IInfoEntry:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            IInfoEntry: コレクション要素
        """
        ...
    def GetEnumerator(self) -> IInfoEntryEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            IInfoEntryEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[IInfoEntry]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class IInfoEntryEnumerator:
    """
    エラー情報/検索結果情報の共通情報のコレクションの列挙子です。
    """
    ...

class ISearch:
    """
    検索サービスです。
    """
    def BeginSearch(self, name: str, type: str, append: bool) -> None:
        """
        検索開始を要求します。

        Args:
            name (str): 検索名
            type (str): 検索種別
            append (bool): 追加検索とするか

        Returns:
            None: This method does not return a value.
        """
        ...
    def EndSearch(self) -> None:
        """
        検索終了を要求します。
        検索結果が確定し、検索結果一覧で取得可能となります。

        Returns:
            None: This method does not return a value.
        """
        ...
    def CancelSearch(self, flush: bool) -> None:
        """
        検索のキャンセルを要求します。

        Args:
            flush (bool): それまでの検索結果を確定するか

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearSearchResult(self) -> None:
        """
        現在の検索結果をクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @overload
    def AddSearchResult(self, item: Any, message: str) -> ISearchResultEntry:
        """
        検索結果を登録します。

        Args:
            item (Any): 検索条件にヒットしたオブジェクト
            message (str): メッセージ

        Returns:
            ISearchResultEntry: 検索結果
        """
        ...
    @overload
    def AddSearchResult(self, model: IModel, fields: str, message: str) -> ISearchResultEntry:
        """
        検索結果を登録します。

        Args:
            model (IModel): 検索条件にヒットしたモデル
            fields (str): 検索条件にヒットしたフィールド名（複数の場合はカンマ区切り）
            message (str): メッセージ

        Returns:
            ISearchResultEntry: 検索結果
        """
        ...
    def AddSearchTarget(self, model: IModel) -> None:
        """
        検索対象を追加します。
        検索対象の情報は検索結果ウィンドウやエディタ、ナビゲータ等で表示されます。

        Args:
            model (IModel): モデル

        Returns:
            None: This method does not return a value.
        """
        ...
    def ClearSearchTarget(self) -> None:
        """
        検索対象をクリアします。

        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def Name(self) -> str:
        """検索名"""
        ...
    @property
    def Type(self) -> str:
        """検索種別"""
        ...
    @property
    def IsSearching(self) -> bool:
        """検索中であるか"""
        ...
    @property
    def IsSearchCanceled(self) -> bool:
        """現在の検索にキャンセル要求が発行されているか"""
        ...
    @property
    def ShowTotalCount(self) -> bool:
        """検索結果の積み上げ値を表示するか"""
        ...
    @property
    def SearchTargets(self) -> IModelCollection:
        """検索対象の一覧"""
        ...

class ISearchManager:
    """
    検索マネージャです。
    """
    def FindResultByModel(self, model: IModel) -> ISearchResultEntryCollection:
        """
        与えられたモデルを対象とした検索結果情報を検索します

        Args:
            model (IModel): モデル

        Returns:
            ISearchResultEntryCollection: 検索結果情報一覧
        """
        ...
    def ClearResults(self) -> None:
        """
        すべての検索結果情報をクリアします

        Returns:
            None: This method does not return a value.
        """
        ...
    def Create(self) -> ISearch:
        """
        検索オブジェクトを生成します。

        Returns:
            ISearch: 検索オブジェクト
        """
        ...
    def RemoveResult(self, entry: ISearchResultEntry) -> None:
        """
        指定した検索結果を削除します。
        既に削除済みの検索結果を指定した場合は何も行いません。

        Args:
            entry (ISearchResultEntry): 検索結果。

        Returns:
            None: This method does not return a value.
        """
        ...
    def RemoveResults(self, entries: Iterable[ISearchResultEntry]) -> None:
        """
        Returns:
            None: This method does not return a value.
        """
        ...
    @property
    def HasSearchResultEntry(self) -> bool:
        """検索結果が登録されているか"""
        ...
    @property
    def AllResults(self) -> ISearchResultEntryCollection:
        """すべての検索結果情報"""
        ...

class ISearchResultEntry(IInfoEntry):
    """
    検索結果情報です。
    検索対象がモデルの場合のみ Model、Fieldの値を取得できます。
    """
    @property
    def Item(self) -> Any:
        """検索オブジェクト"""
        ...

class ISearchResultEntryCollection:
    """
    検索結果情報のコレクションです。
    """
    def GetItem(self, index: int) -> ISearchResultEntry:
        """
        インデックスで指定されたコレクションの要素を取得します

        Args:
            index (int): インデックス

        Returns:
            ISearchResultEntry: コレクション要素
        """
        ...
    def GetEnumerator(self) -> ISearchResultEntryEnumerator:
        """
        コレクションを反復処理する列挙子を取得します

        Returns:
            ISearchResultEntryEnumerator: Enumerator
        """
        ...
    def __iter__(self) -> Iterator[ISearchResultEntry]:
        ...
    @property
    def Count(self) -> int:
        """コレクション内の要素数を取得します"""
        ...

class ISearchResultEntryEnumerator:
    """
    検索結果情報のコレクションの列挙子です。
    """
    ...

class IScmFileStatus:
    """
    物理ファイルの構成管理状態です。
    """
    @property
    def HasLock(self) -> bool:
        """この物理ファイルで構成管理システムの排他ロックを取得しているか。
排他ロックを取得している場合、他のユーザはコミットできません。"""
        ...
    @property
    def LockAccount(self) -> str:
        """この物理ファイルの構成管理システムの排他ロックを取得しているユーザ（アカウント）名"""
        ...
    @property
    def ScmState(self) -> str:
        """この物理ファイルの構成管理システム上のファイル状態
{\"None\":変更なし, \"Add\":追加, \"Update\":更新, \"Delete\":削除, \"Lost\":紛失, \"Conflict\":競合, \"Unmanage\":管理外, \"Ignore\":管理外で無視,
\"Unknown\":不明}"""
        ...

class Guids:
    """
    GUID定義
    """
    ...

class IModelAccessPolicy:
    """
    モデルアクセスポリシーです。
    """
    def SetSpecifiedProductAccess(self, product: IProduct) -> None:
        """
        指定したプロダクトで有効なモデル情報のみ取得・検索を可能に設定します。

        Args:
            product (IProduct): プロダクト

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetAllProductAccess(self) -> None:
        """
        すべてのモデル情報の取得・検索を可能に設定します。

        Returns:
            None: This method does not return a value.
        """
        ...
    def SetAllEditorAccess(self, enabled: bool) -> None:
        """
        全てのエディタの詳細情報を取得可能とするか設定します。
        取得可能に設定した場合、エディタの内部構造を解析するため、エディタAPIの応答に解析時間が加算されます。

        Args:
            enabled (bool): 取得可能とするか

        Returns:
            None: This method does not return a value.
        """
        ...

