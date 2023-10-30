using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using NextDesign.Core;
using NextDesign.Desktop;

namespace ExcelExtension
{
    /// <summary>
    /// Next Design のモデル構造を操作するクラス
    /// </summary>
    public class SoftwareStructureModelHandler
    {
        /// <summary>
        /// Next Design に読み込んだデータを書き込みます。
        /// </summary>
        public IModel AddStructuredModel(IModel model, string childrenFieldName, ModelDto dto)
        {
            // -------------------------------------
            // Next Design にデータを追加します。
            // -------------------------------------
            var addedModel = model.AddNewModel(childrenFieldName, dto.ClassName);

            // -------------------------------------
            // データの項目値を設定します。
            // -------------------------------------
            addedModel.SetField("Name", dto.Name);
            addedModel.SetField("Responsibility", dto.Responsibility);

            // -------------------------------------
            // 続けて、下位階層のデータを追加します。
            // -------------------------------------
            foreach (var child in dto.Children)
            {
                AddStructuredModel(addedModel, dto.ChildrenFieldName, child);
            }

            return addedModel;
        }

        /// <summary>
        /// ソフト構造のモデル構造からデータを収集します。
        /// </summary>
        public ModelDto FetchStructuredModel(IModel model)
        {
            // -------------------------------------
            // ソフト構造からデータを収集します。
            // -------------------------------------
            var modelDto = ModelDto.CreateSoftwareStructureDto();
            modelDto.Name = model.Name;
            modelDto.ClassDisplayName = model.Metaclass.DisplayName;
            modelDto.ChildrenFieldDisplayName = model.Metaclass.GetField(modelDto.ChildrenFieldName).DisplayName;
            modelDto.ChildrenClassName = model.Metaclass.GetField(modelDto.ChildrenFieldName).TypeClass.Name;
            modelDto.ChildrenClassDisplayName = model.Metaclass.GetField(modelDto.ChildrenFieldName).TypeClass.DisplayName;

            // -------------------------------------
            // 第1階層のレイヤからデータを収集します。
            // -------------------------------------
            var layers = model.GetFieldValues(modelDto.ChildrenFieldName);
            foreach (var layer in layers)
            {
                var layerDto = ModelDto.CreateLayerDto();
                layerDto.Name = layer.Name;
                layerDto.Responsibility = layer.GetFieldString("Responsibility");
                layerDto.ClassDisplayName = layer.Metaclass.DisplayName;
                layerDto.ChildrenFieldDisplayName = layer.Metaclass.GetField(layerDto.ChildrenFieldName).DisplayName;
                layerDto.ChildrenClassName = layer.Metaclass.GetField(layerDto.ChildrenFieldName).TypeClass.Name;
                layerDto.ChildrenClassDisplayName = layer.Metaclass.GetField(layerDto.ChildrenFieldName).TypeClass.DisplayName;
                modelDto.Children.Add(layerDto);

                // -------------------------------------
                // 第2階層のコンポーネントからデータを収集します。
                // -------------------------------------
                var components = layer.GetFieldValues(layerDto.ChildrenFieldName);
                foreach (var component in components)
                {
                    var componetDto = ModelDto.CreateComponentDto();
                    componetDto.Name = component.Name;
                    componetDto.Responsibility = component.GetFieldString("Responsibility");
                    componetDto.ClassDisplayName = component.Metaclass.DisplayName;
                    componetDto.ChildrenFieldDisplayName = component.Metaclass.GetField(componetDto.ChildrenFieldName).DisplayName;
                    componetDto.ChildrenClassName = component.Metaclass.GetField(componetDto.ChildrenFieldName).TypeClass.Name;
                    componetDto.ChildrenClassDisplayName = component.Metaclass.GetField(componetDto.ChildrenFieldName).TypeClass.DisplayName;
                    layerDto.Children.Add(componetDto);
                }
            }

            return modelDto;
        }
    }
}
