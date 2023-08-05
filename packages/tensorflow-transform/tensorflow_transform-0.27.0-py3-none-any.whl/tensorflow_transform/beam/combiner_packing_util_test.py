# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tensorflow_transform.analysis_graph_builder."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# GOOGLE-INITIALIZATION
import mock
import tensorflow as tf
import tensorflow_transform as tft
from tensorflow_transform import impl_helper
from tensorflow_transform import nodes
from tensorflow_transform.beam import analysis_graph_builder
from tensorflow_transform.beam import combiner_packing_util
from tensorflow_transform import test_case

mock = tf.compat.v1.test.mock


def _preprocessing_fn_with_packable_analyzer_single_phase(inputs):
  x, y = inputs['x'], inputs['y']
  x_mean = tft.mean(x, name='x')
  x_centered = x - x_mean
  y_mean = tft.mean(y, name='y')
  y_centered = y - y_mean
  z = inputs['z']
  z_vocab = tft.vocabulary(z, name='z')
  initializer = tf.lookup.TextFileInitializer(
      z_vocab,
      key_dtype=tf.string,
      key_index=tf.lookup.TextFileIndex.WHOLE_LINE,
      value_dtype=tf.int64,
      value_index=tf.lookup.TextFileIndex.LINE_NUMBER)
  table = tf.lookup.StaticHashTable(initializer, default_value=-1)
  z_integerized = table.lookup(z)
  return {'x_centered': x_centered, 'y_centered': y_centered,
          'z_integerized': z_integerized}


_PACKABLE_ANALYZER_SINGLE_PHASE_CASE = dict(
    testcase_name='with_packable_analyzer_single_phase',
    feature_spec={
        'x': tf.io.FixedLenFeature([], tf.float32),
        'y': tf.io.FixedLenFeature([], tf.float32),
        'z': tf.io.FixedLenFeature([], tf.string)
    },
    preprocessing_fn=_preprocessing_fn_with_packable_analyzer_single_phase,
    num_phases=1,
    expected_dot_graph_str_before_packing=r"""digraph G {
directed=True;
node [shape=Mrecord];
"CreateSavedModelForAnalyzerInputs[Phase0]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('z/Reshape', \"Tensor\<shape: [None], \<dtype: 'string'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase0]}"];
"ExtractInputForSavedModel[FlattenedDataset]" [label="{ExtractInputForSavedModel|dataset_key: DatasetKey(key='FlattenedDataset')|label: ExtractInputForSavedModel[FlattenedDataset]}"];
"ApplySavedModel[Phase0]" [label="{ApplySavedModel|phase: 0|label: ApplySavedModel[Phase0]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase0]" -> "ApplySavedModel[Phase0]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase0]";
"TensorSource[x/mean_and_var]" [label="{ExtractFromDict|keys: ('x/mean_and_var/Cast', 'x/mean_and_var/truediv', 'x/mean_and_var/truediv_1', 'x/mean_and_var/zeros')|label: TensorSource[x/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[x/mean_and_var]";
"CacheableCombineAccumulate[x/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[x/mean_and_var]|partitionable: True}"];
"TensorSource[x/mean_and_var]" -> "CacheableCombineAccumulate[x/mean_and_var]";
"CacheableCombineMerge[x/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[x/mean_and_var]}"];
"CacheableCombineAccumulate[x/mean_and_var]" -> "CacheableCombineMerge[x/mean_and_var]";
"ExtractCombineMergeOutputs[x/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[x/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[x/mean_and_var]" -> "ExtractCombineMergeOutputs[x/mean_and_var]";
"CreateTensorBinding[x/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":0 -> "CreateTensorBinding[x/mean_and_var/Placeholder]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":1 -> "CreateTensorBinding[x/mean_and_var/Placeholder_1]";
"TensorSource[y/mean_and_var]" [label="{ExtractFromDict|keys: ('y/mean_and_var/Cast', 'y/mean_and_var/truediv', 'y/mean_and_var/truediv_1', 'y/mean_and_var/zeros')|label: TensorSource[y/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[y/mean_and_var]";
"CacheableCombineAccumulate[y/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[y/mean_and_var]|partitionable: True}"];
"TensorSource[y/mean_and_var]" -> "CacheableCombineAccumulate[y/mean_and_var]";
"CacheableCombineMerge[y/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[y/mean_and_var]}"];
"CacheableCombineAccumulate[y/mean_and_var]" -> "CacheableCombineMerge[y/mean_and_var]";
"ExtractCombineMergeOutputs[y/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[y/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[y/mean_and_var]" -> "ExtractCombineMergeOutputs[y/mean_and_var]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":0 -> "CreateTensorBinding[y/mean_and_var/Placeholder]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":1 -> "CreateTensorBinding[y/mean_and_var/Placeholder_1]";
"TensorSource[z]" [label="{ExtractFromDict|keys: ('z/Reshape',)|label: TensorSource[z]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[z]";
"VocabularyAccumulate[z]" [label="{VocabularyAccumulate|vocab_ordering_type: 1|input_dtype: string|label: VocabularyAccumulate[z]|partitionable: True}"];
"TensorSource[z]" -> "VocabularyAccumulate[z]";
"VocabularyMerge[z]" [label="{VocabularyMerge|vocab_ordering_type: 1|use_adjusted_mutual_info: False|min_diff_from_avg: None|label: VocabularyMerge[z]}"];
"VocabularyAccumulate[z]" -> "VocabularyMerge[z]";
"VocabularyCount[z]" [label="{VocabularyCount|label: VocabularyCount[z]}"];
"VocabularyMerge[z]" -> "VocabularyCount[z]";
"CreateTensorBinding[z/vocab_z_unpruned_vocab_size]" [label="{CreateTensorBinding|tensor: z/vocab_z_unpruned_vocab_size:0|is_asset_filepath: False|label: CreateTensorBinding[z/vocab_z_unpruned_vocab_size]}"];
"VocabularyCount[z]" -> "CreateTensorBinding[z/vocab_z_unpruned_vocab_size]";
"VocabularyPrune[z]" [label="{VocabularyPrune|top_k: None|frequency_threshold: 0|informativeness_threshold: -inf|coverage_top_k: None|coverage_frequency_threshold: 0|coverage_informativeness_threshold: -inf|key_fn: None|filter_newline_characters: True|label: VocabularyPrune[z]}"];
"VocabularyMerge[z]" -> "VocabularyPrune[z]";
"VocabularyOrderAndWrite[z]" [label="{VocabularyOrderAndWrite|vocab_filename: vocab_z|store_frequency: False|input_dtype: string|label: VocabularyOrderAndWrite[z]|fingerprint_shuffle: False|file_format: text}"];
"VocabularyPrune[z]" -> "VocabularyOrderAndWrite[z]";
"CreateTensorBinding[z/Placeholder]" [label="{CreateTensorBinding|tensor: z/Placeholder:0|is_asset_filepath: True|label: CreateTensorBinding[z/Placeholder]}"];
"VocabularyOrderAndWrite[z]" -> "CreateTensorBinding[z/Placeholder]";
CreateSavedModel [label="{CreateSavedModel|table_initializers: 1|output_signature: OrderedDict([('x_centered', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('y_centered', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('z_integerized', \"Tensor\<shape: [None], \<dtype: 'int64'\>\>\")])|label: CreateSavedModel}"];
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[z/vocab_z_unpruned_vocab_size]" -> CreateSavedModel;
"CreateTensorBinding[z/Placeholder]" -> CreateSavedModel;
}
""",
    expected_dot_graph_str_after_packing=r"""digraph G {
directed=True;
node [shape=Mrecord];
"CreateSavedModelForAnalyzerInputs[Phase0]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('z/Reshape', \"Tensor\<shape: [None], \<dtype: 'string'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase0]}"];
"ExtractInputForSavedModel[FlattenedDataset]" [label="{ExtractInputForSavedModel|dataset_key: DatasetKey(key='FlattenedDataset')|label: ExtractInputForSavedModel[FlattenedDataset]}"];
"ApplySavedModel[Phase0]" [label="{ApplySavedModel|phase: 0|label: ApplySavedModel[Phase0]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase0]" -> "ApplySavedModel[Phase0]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase0]";
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" [label="{PackedCombineAccumulate|combiners: [_CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('x/mean_and_var/Cast', 'x/mean_and_var/truediv', 'x/mean_and_var/truediv_1', 'x/mean_and_var/zeros'), label='CacheableCombineAccumulate[x/mean_and_var]'), _CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('y/mean_and_var/Cast', 'y/mean_and_var/truediv', 'y/mean_and_var/truediv_1', 'y/mean_and_var/zeros'), label='CacheableCombineAccumulate[y/mean_and_var]')]|label: PackedCombineAccumulate[ApplySavedModel[Phase0]]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "PackedCombineAccumulate[ApplySavedModel[Phase0]]";
"CacheableCombineAccumulate[x/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[x/mean_and_var]|label: CacheableCombineAccumulate[x/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" -> "CacheableCombineAccumulate[x/mean_and_var]";
"AddKey[CacheableCombineMerge[x/mean_and_var]]" [label="{AddKey|key: CacheableCombineMerge[x/mean_and_var]|label: AddKey[CacheableCombineMerge[x/mean_and_var]]|partitionable: True}"];
"CacheableCombineAccumulate[x/mean_and_var]" -> "AddKey[CacheableCombineMerge[x/mean_and_var]]";
"CacheableCombineAccumulate[y/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[y/mean_and_var]|label: CacheableCombineAccumulate[y/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" -> "CacheableCombineAccumulate[y/mean_and_var]";
"AddKey[CacheableCombineMerge[y/mean_and_var]]" [label="{AddKey|key: CacheableCombineMerge[y/mean_and_var]|label: AddKey[CacheableCombineMerge[y/mean_and_var]]|partitionable: True}"];
"CacheableCombineAccumulate[y/mean_and_var]" -> "AddKey[CacheableCombineMerge[y/mean_and_var]]";
"FlattenInputForPackedCombineMerge[2]" [label="{Flatten|label: FlattenInputForPackedCombineMerge[2]|partitionable: True}"];
"AddKey[CacheableCombineMerge[x/mean_and_var]]" -> "FlattenInputForPackedCombineMerge[2]";
"AddKey[CacheableCombineMerge[y/mean_and_var]]" -> "FlattenInputForPackedCombineMerge[2]";
"PackedCombineMerge[2]" [label="{PackedCombineMerge|combiners: [_CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('CacheableCombineMerge[x/mean_and_var]',), label='CacheableCombineMerge[x/mean_and_var]'), _CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('CacheableCombineMerge[y/mean_and_var]',), label='CacheableCombineMerge[y/mean_and_var]')]|label: PackedCombineMerge[2]}"];
"FlattenInputForPackedCombineMerge[2]" -> "PackedCombineMerge[2]";
"ExtractFromDict[CacheableCombineMerge[y/mean_and_var]]" [label="{ExtractFromDict|keys: CacheableCombineMerge[y/mean_and_var]|label: ExtractFromDict[CacheableCombineMerge[y/mean_and_var]]|partitionable: True}"];
"PackedCombineMerge[2]" -> "ExtractFromDict[CacheableCombineMerge[y/mean_and_var]]";
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[y/mean_and_var]]" [label="{ExtractPackedCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractPackedCombineMergeOutputs[CacheableCombineMerge[y/mean_and_var]]|{<0>0|<1>1}}"];
"ExtractFromDict[CacheableCombineMerge[y/mean_and_var]]" -> "ExtractPackedCombineMergeOutputs[CacheableCombineMerge[y/mean_and_var]]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder]}"];
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[y/mean_and_var]]":0 -> "CreateTensorBinding[y/mean_and_var/Placeholder]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder_1]}"];
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[y/mean_and_var]]":1 -> "CreateTensorBinding[y/mean_and_var/Placeholder_1]";
"TensorSource[z]" [label="{ExtractFromDict|keys: ('z/Reshape',)|label: TensorSource[z]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[z]";
"VocabularyAccumulate[z]" [label="{VocabularyAccumulate|vocab_ordering_type: 1|input_dtype: string|label: VocabularyAccumulate[z]|partitionable: True}"];
"TensorSource[z]" -> "VocabularyAccumulate[z]";
"VocabularyMerge[z]" [label="{VocabularyMerge|vocab_ordering_type: 1|use_adjusted_mutual_info: False|min_diff_from_avg: None|label: VocabularyMerge[z]}"];
"VocabularyAccumulate[z]" -> "VocabularyMerge[z]";
"VocabularyCount[z]" [label="{VocabularyCount|label: VocabularyCount[z]}"];
"VocabularyMerge[z]" -> "VocabularyCount[z]";
"CreateTensorBinding[z/vocab_z_unpruned_vocab_size]" [label="{CreateTensorBinding|tensor: z/vocab_z_unpruned_vocab_size:0|is_asset_filepath: False|label: CreateTensorBinding[z/vocab_z_unpruned_vocab_size]}"];
"VocabularyCount[z]" -> "CreateTensorBinding[z/vocab_z_unpruned_vocab_size]";
"VocabularyPrune[z]" [label="{VocabularyPrune|top_k: None|frequency_threshold: 0|informativeness_threshold: -inf|coverage_top_k: None|coverage_frequency_threshold: 0|coverage_informativeness_threshold: -inf|key_fn: None|filter_newline_characters: True|label: VocabularyPrune[z]}"];
"VocabularyMerge[z]" -> "VocabularyPrune[z]";
"VocabularyOrderAndWrite[z]" [label="{VocabularyOrderAndWrite|vocab_filename: vocab_z|store_frequency: False|input_dtype: string|label: VocabularyOrderAndWrite[z]|fingerprint_shuffle: False|file_format: text}"];
"VocabularyPrune[z]" -> "VocabularyOrderAndWrite[z]";
"CreateTensorBinding[z/Placeholder]" [label="{CreateTensorBinding|tensor: z/Placeholder:0|is_asset_filepath: True|label: CreateTensorBinding[z/Placeholder]}"];
"VocabularyOrderAndWrite[z]" -> "CreateTensorBinding[z/Placeholder]";
"ExtractFromDict[CacheableCombineMerge[x/mean_and_var]]" [label="{ExtractFromDict|keys: CacheableCombineMerge[x/mean_and_var]|label: ExtractFromDict[CacheableCombineMerge[x/mean_and_var]]|partitionable: True}"];
"PackedCombineMerge[2]" -> "ExtractFromDict[CacheableCombineMerge[x/mean_and_var]]";
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[x/mean_and_var]]" [label="{ExtractPackedCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractPackedCombineMergeOutputs[CacheableCombineMerge[x/mean_and_var]]|{<0>0|<1>1}}"];
"ExtractFromDict[CacheableCombineMerge[x/mean_and_var]]" -> "ExtractPackedCombineMergeOutputs[CacheableCombineMerge[x/mean_and_var]]";
"CreateTensorBinding[x/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder]}"];
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[x/mean_and_var]]":0 -> "CreateTensorBinding[x/mean_and_var/Placeholder]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder_1]}"];
"ExtractPackedCombineMergeOutputs[CacheableCombineMerge[x/mean_and_var]]":1 -> "CreateTensorBinding[x/mean_and_var/Placeholder_1]";
CreateSavedModel [label="{CreateSavedModel|table_initializers: 1|output_signature: OrderedDict([('x_centered', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('y_centered', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('z_integerized', \"Tensor\<shape: [None], \<dtype: 'int64'\>\>\")])|label: CreateSavedModel}"];
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[z/vocab_z_unpruned_vocab_size]" -> CreateSavedModel;
"CreateTensorBinding[z/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> CreateSavedModel;
}
""")


def _preprocessing_fn_with_packable_analyzer_two_phases(inputs):
  x, y = inputs['x'], inputs['y']
  x_mean = tft.mean(x, name='x')
  x_square_deviations = tf.square(x - x_mean)
  x_var = tft.mean(x_square_deviations, name='x_square_deviations')
  x_normalized = (x - x_mean) / tf.sqrt(x_var)
  y_mean = tft.mean(y, name='y')
  y_square_deviations = tf.square(y - y_mean)
  y_var = tft.mean(y_square_deviations, name='y_square_deviations')
  y_normalized = (y - y_mean) / tf.sqrt(y_var)
  return {'x_normalized': x_normalized, 'y_normalized': y_normalized}


_PACKABLE_ANALYZER_TWO_PHASES_CASE = dict(
    testcase_name='with_packable_analyzer_two_phases',
    feature_spec={
        'x': tf.io.FixedLenFeature([], tf.float32),
        'y': tf.io.FixedLenFeature([], tf.float32)
    },
    preprocessing_fn=_preprocessing_fn_with_packable_analyzer_two_phases,
    num_phases=2,
    expected_dot_graph_str_before_packing=r"""digraph G {
directed=True;
node [shape=Mrecord];
"CreateSavedModelForAnalyzerInputs[Phase0]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase0]}"];
"ExtractInputForSavedModel[FlattenedDataset]" [label="{ExtractInputForSavedModel|dataset_key: DatasetKey(key='FlattenedDataset')|label: ExtractInputForSavedModel[FlattenedDataset]}"];
"ApplySavedModel[Phase0]" [label="{ApplySavedModel|phase: 0|label: ApplySavedModel[Phase0]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase0]" -> "ApplySavedModel[Phase0]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase0]";
"TensorSource[x/mean_and_var]" [label="{ExtractFromDict|keys: ('x/mean_and_var/Cast', 'x/mean_and_var/truediv', 'x/mean_and_var/truediv_1', 'x/mean_and_var/zeros')|label: TensorSource[x/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[x/mean_and_var]";
"CacheableCombineAccumulate[x/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[x/mean_and_var]|partitionable: True}"];
"TensorSource[x/mean_and_var]" -> "CacheableCombineAccumulate[x/mean_and_var]";
"CacheableCombineMerge[x/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[x/mean_and_var]}"];
"CacheableCombineAccumulate[x/mean_and_var]" -> "CacheableCombineMerge[x/mean_and_var]";
"ExtractCombineMergeOutputs[x/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[x/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[x/mean_and_var]" -> "ExtractCombineMergeOutputs[x/mean_and_var]";
"CreateTensorBinding[x/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":0 -> "CreateTensorBinding[x/mean_and_var/Placeholder]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":1 -> "CreateTensorBinding[x/mean_and_var/Placeholder_1]";
"TensorSource[y/mean_and_var]" [label="{ExtractFromDict|keys: ('y/mean_and_var/Cast', 'y/mean_and_var/truediv', 'y/mean_and_var/truediv_1', 'y/mean_and_var/zeros')|label: TensorSource[y/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "TensorSource[y/mean_and_var]";
"CacheableCombineAccumulate[y/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[y/mean_and_var]|partitionable: True}"];
"TensorSource[y/mean_and_var]" -> "CacheableCombineAccumulate[y/mean_and_var]";
"CacheableCombineMerge[y/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[y/mean_and_var]}"];
"CacheableCombineAccumulate[y/mean_and_var]" -> "CacheableCombineMerge[y/mean_and_var]";
"ExtractCombineMergeOutputs[y/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[y/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[y/mean_and_var]" -> "ExtractCombineMergeOutputs[y/mean_and_var]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":0 -> "CreateTensorBinding[y/mean_and_var/Placeholder]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":1 -> "CreateTensorBinding[y/mean_and_var/Placeholder_1]";
"CreateSavedModelForAnalyzerInputs[Phase1]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x_square_deviations/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase1]}"];
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"ApplySavedModel[Phase1]" [label="{ApplySavedModel|phase: 1|label: ApplySavedModel[Phase1]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase1]" -> "ApplySavedModel[Phase1]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase1]";
"TensorSource[x_square_deviations/mean_and_var]" [label="{ExtractFromDict|keys: ('x_square_deviations/mean_and_var/Cast', 'x_square_deviations/mean_and_var/truediv', 'x_square_deviations/mean_and_var/truediv_1', 'x_square_deviations/mean_and_var/zeros')|label: TensorSource[x_square_deviations/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase1]" -> "TensorSource[x_square_deviations/mean_and_var]";
"CacheableCombineAccumulate[x_square_deviations/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[x_square_deviations/mean_and_var]|partitionable: True}"];
"TensorSource[x_square_deviations/mean_and_var]" -> "CacheableCombineAccumulate[x_square_deviations/mean_and_var]";
"CacheableCombineMerge[x_square_deviations/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[x_square_deviations/mean_and_var]}"];
"CacheableCombineAccumulate[x_square_deviations/mean_and_var]" -> "CacheableCombineMerge[x_square_deviations/mean_and_var]";
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[x_square_deviations/mean_and_var]" -> "ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]";
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x_square_deviations/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]":0 -> "CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]";
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x_square_deviations/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]":1 -> "CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]";
"TensorSource[y_square_deviations/mean_and_var]" [label="{ExtractFromDict|keys: ('y_square_deviations/mean_and_var/Cast', 'y_square_deviations/mean_and_var/truediv', 'y_square_deviations/mean_and_var/truediv_1', 'y_square_deviations/mean_and_var/zeros')|label: TensorSource[y_square_deviations/mean_and_var]|partitionable: True}"];
"ApplySavedModel[Phase1]" -> "TensorSource[y_square_deviations/mean_and_var]";
"CacheableCombineAccumulate[y_square_deviations/mean_and_var]" [label="{CacheableCombineAccumulate|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineAccumulate[y_square_deviations/mean_and_var]|partitionable: True}"];
"TensorSource[y_square_deviations/mean_and_var]" -> "CacheableCombineAccumulate[y_square_deviations/mean_and_var]";
"CacheableCombineMerge[y_square_deviations/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[y_square_deviations/mean_and_var]}"];
"CacheableCombineAccumulate[y_square_deviations/mean_and_var]" -> "CacheableCombineMerge[y_square_deviations/mean_and_var]";
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[y_square_deviations/mean_and_var]" -> "ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]";
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y_square_deviations/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]":0 -> "CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]";
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y_square_deviations/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]":1 -> "CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]";
CreateSavedModel [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x_normalized', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('y_normalized', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\")])|label: CreateSavedModel}"];
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]" -> CreateSavedModel;
}
""",
    expected_dot_graph_str_after_packing=r"""digraph G {
directed=True;
node [shape=Mrecord];
"CreateSavedModelForAnalyzerInputs[Phase0]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase0]}"];
"ExtractInputForSavedModel[FlattenedDataset]" [label="{ExtractInputForSavedModel|dataset_key: DatasetKey(key='FlattenedDataset')|label: ExtractInputForSavedModel[FlattenedDataset]}"];
"ApplySavedModel[Phase0]" [label="{ApplySavedModel|phase: 0|label: ApplySavedModel[Phase0]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase0]" -> "ApplySavedModel[Phase0]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase0]";
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" [label="{PackedCombineAccumulate|combiners: [_CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('x/mean_and_var/Cast', 'x/mean_and_var/truediv', 'x/mean_and_var/truediv_1', 'x/mean_and_var/zeros'), label='CacheableCombineAccumulate[x/mean_and_var]'), _CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('y/mean_and_var/Cast', 'y/mean_and_var/truediv', 'y/mean_and_var/truediv_1', 'y/mean_and_var/zeros'), label='CacheableCombineAccumulate[y/mean_and_var]')]|label: PackedCombineAccumulate[ApplySavedModel[Phase0]]|partitionable: True}"];
"ApplySavedModel[Phase0]" -> "PackedCombineAccumulate[ApplySavedModel[Phase0]]";
"CacheableCombineAccumulate[x/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[x/mean_and_var]|label: CacheableCombineAccumulate[x/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" -> "CacheableCombineAccumulate[x/mean_and_var]";
"CacheableCombineMerge[x/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[x/mean_and_var]}"];
"CacheableCombineAccumulate[x/mean_and_var]" -> "CacheableCombineMerge[x/mean_and_var]";
"ExtractCombineMergeOutputs[x/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[x/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[x/mean_and_var]" -> "ExtractCombineMergeOutputs[x/mean_and_var]";
"CreateTensorBinding[x/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":0 -> "CreateTensorBinding[x/mean_and_var/Placeholder]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[x/mean_and_var]":1 -> "CreateTensorBinding[x/mean_and_var/Placeholder_1]";
"CacheableCombineAccumulate[y/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[y/mean_and_var]|label: CacheableCombineAccumulate[y/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase0]]" -> "CacheableCombineAccumulate[y/mean_and_var]";
"CacheableCombineMerge[y/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[y/mean_and_var]}"];
"CacheableCombineAccumulate[y/mean_and_var]" -> "CacheableCombineMerge[y/mean_and_var]";
"ExtractCombineMergeOutputs[y/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[y/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[y/mean_and_var]" -> "ExtractCombineMergeOutputs[y/mean_and_var]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":0 -> "CreateTensorBinding[y/mean_and_var/Placeholder]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[y/mean_and_var]":1 -> "CreateTensorBinding[y/mean_and_var/Placeholder_1]";
"CreateSavedModelForAnalyzerInputs[Phase1]" [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x_square_deviations/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('x_square_deviations/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/Cast', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/truediv', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/truediv_1', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\"), ('y_square_deviations/mean_and_var/zeros', \"Tensor\<shape: [], \<dtype: 'float32'\>\>\")])|label: CreateSavedModelForAnalyzerInputs[Phase1]}"];
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> "CreateSavedModelForAnalyzerInputs[Phase1]";
"ApplySavedModel[Phase1]" [label="{ApplySavedModel|phase: 1|label: ApplySavedModel[Phase1]|partitionable: True}"];
"CreateSavedModelForAnalyzerInputs[Phase1]" -> "ApplySavedModel[Phase1]";
"ExtractInputForSavedModel[FlattenedDataset]" -> "ApplySavedModel[Phase1]";
"PackedCombineAccumulate[ApplySavedModel[Phase1]]" [label="{PackedCombineAccumulate|combiners: [_CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('x_square_deviations/mean_and_var/Cast', 'x_square_deviations/mean_and_var/truediv', 'x_square_deviations/mean_and_var/truediv_1', 'x_square_deviations/mean_and_var/zeros'), label='CacheableCombineAccumulate[x_square_deviations/mean_and_var]'), _CombinerOpWrapper(combiner=\<WeightedMeanAndVarCombiner\>, keys=('y_square_deviations/mean_and_var/Cast', 'y_square_deviations/mean_and_var/truediv', 'y_square_deviations/mean_and_var/truediv_1', 'y_square_deviations/mean_and_var/zeros'), label='CacheableCombineAccumulate[y_square_deviations/mean_and_var]')]|label: PackedCombineAccumulate[ApplySavedModel[Phase1]]|partitionable: True}"];
"ApplySavedModel[Phase1]" -> "PackedCombineAccumulate[ApplySavedModel[Phase1]]";
"CacheableCombineAccumulate[x_square_deviations/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[x_square_deviations/mean_and_var]|label: CacheableCombineAccumulate[x_square_deviations/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase1]]" -> "CacheableCombineAccumulate[x_square_deviations/mean_and_var]";
"CacheableCombineMerge[x_square_deviations/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[x_square_deviations/mean_and_var]}"];
"CacheableCombineAccumulate[x_square_deviations/mean_and_var]" -> "CacheableCombineMerge[x_square_deviations/mean_and_var]";
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[x_square_deviations/mean_and_var]" -> "ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]";
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: x_square_deviations/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]":0 -> "CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]";
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: x_square_deviations/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[x_square_deviations/mean_and_var]":1 -> "CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]";
"CacheableCombineAccumulate[y_square_deviations/mean_and_var]" [label="{ExtractFromDict|keys: CacheableCombineAccumulate[y_square_deviations/mean_and_var]|label: CacheableCombineAccumulate[y_square_deviations/mean_and_var]|partitionable: True}"];
"PackedCombineAccumulate[ApplySavedModel[Phase1]]" -> "CacheableCombineAccumulate[y_square_deviations/mean_and_var]";
"CacheableCombineMerge[y_square_deviations/mean_and_var]" [label="{CacheableCombineMerge|combiner: \<WeightedMeanAndVarCombiner\>|label: CacheableCombineMerge[y_square_deviations/mean_and_var]}"];
"CacheableCombineAccumulate[y_square_deviations/mean_and_var]" -> "CacheableCombineMerge[y_square_deviations/mean_and_var]";
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]" [label="{ExtractCombineMergeOutputs|output_tensor_info_list: [TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None), TensorInfo(dtype=tf.float32, shape=(), temporary_asset_value=None)]|label: ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]|{<0>0|<1>1}}"];
"CacheableCombineMerge[y_square_deviations/mean_and_var]" -> "ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]";
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]" [label="{CreateTensorBinding|tensor: y_square_deviations/mean_and_var/Placeholder:0|is_asset_filepath: False|label: CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]}"];
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]":0 -> "CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]";
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]" [label="{CreateTensorBinding|tensor: y_square_deviations/mean_and_var/Placeholder_1:0|is_asset_filepath: False|label: CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]}"];
"ExtractCombineMergeOutputs[y_square_deviations/mean_and_var]":1 -> "CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]";
CreateSavedModel [label="{CreateSavedModel|table_initializers: 0|output_signature: OrderedDict([('x_normalized', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\"), ('y_normalized', \"Tensor\<shape: [None], \<dtype: 'float32'\>\>\")])|label: CreateSavedModel}"];
"CreateTensorBinding[x/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[x_square_deviations/mean_and_var/Placeholder_1]" -> CreateSavedModel;
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder]" -> CreateSavedModel;
"CreateTensorBinding[y_square_deviations/mean_and_var/Placeholder_1]" -> CreateSavedModel;
}
""")

_COMBINER_PACKING_TEST_CASES = [
    _PACKABLE_ANALYZER_SINGLE_PHASE_CASE,
    _PACKABLE_ANALYZER_TWO_PHASES_CASE,
]


class CombinerPackingUtilTest(test_case.TransformTestCase):

  @test_case.named_parameters(*_COMBINER_PACKING_TEST_CASES)
  def test_perform_combiner_packing_optimization(
      self, feature_spec, preprocessing_fn, num_phases,
      expected_dot_graph_str_before_packing,
      expected_dot_graph_str_after_packing):

    graph, structured_inputs, structured_outputs = (
        impl_helper.trace_preprocessing_function(
            preprocessing_fn, feature_spec, use_tf_compat_v1=True))

    def _side_effect_fn(saved_model_future, cache_value_nodes,
                        unused_num_phases):
      return (saved_model_future, cache_value_nodes)

    with mock.patch.object(
        combiner_packing_util,
        'perform_combiner_packing_optimization',
        side_effect=_side_effect_fn):
      transform_fn_future_before, unused_cache = analysis_graph_builder.build(
          graph, structured_inputs, structured_outputs)
    transform_fn_future_after, unused_cache = (
        combiner_packing_util.perform_combiner_packing_optimization(
            transform_fn_future_before, unused_cache, num_phases))
    dot_string_before = nodes.get_dot_graph(
        [transform_fn_future_before]).to_string()
    self.assertMultiLineEqual(
        msg='Result dot graph is:\n{}'.format(dot_string_before),
        first=dot_string_before,
        second=expected_dot_graph_str_before_packing)
    dot_string_after = nodes.get_dot_graph(
        [transform_fn_future_after]).to_string()
    self.WriteRenderedDotFile(dot_string_after)
    self.assertMultiLineEqual(
        msg='Result dot graph is:\n{}'.format(dot_string_after),
        first=dot_string_after,
        second=expected_dot_graph_str_after_packing)


if __name__ == '__main__':
  test_case.main()
