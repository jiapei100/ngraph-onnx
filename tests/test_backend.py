# ******************************************************************************
# Copyright 2018-2020 Intel Corporation
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
# ******************************************************************************

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

import onnx.backend.test
import pytest

import ngraph_onnx.onnx_importer.backend as ng_backend

import tests.utils


def expect_fail(test_case_path):  # type: (str) -> None
    """Mark the test as expected to fail."""
    module_name, test_name = test_case_path.split('.')
    module = globals().get(module_name)
    if hasattr(module, test_name):
        pytest.mark.xfail(getattr(module, test_name))
    else:
        logging.getLogger().warning('Could not mark test as XFAIL, not found: %s', test_case_path)


# Set backend device name to be used instead of hardcoded by ONNX BackendTest class ones.
selected_backend_name = tests.utils.BACKEND_NAME
ng_backend.NgraphBackend.backend_name = selected_backend_name

# This is a pytest magic variable to load extra plugins
# Uncomment the line below to enable the ONNX compatibility report
# pytest_plugins = 'onnx.backend.test.report',

# import all test cases at global scope to make them visible to python.unittest
backend_test = onnx.backend.test.BackendTest(ng_backend, __name__)

# MaxPool Indices -> NGRAPH-3131
backend_test.exclude('test_maxpool_with_argmax')

# RNN -> NC-323
backend_test.exclude('test_simple_rnn')
backend_test.exclude('test_rnn')
backend_test.exclude('test_operator_rnn')

# GRU -> NGONNX-325
backend_test.exclude('test_gru')

# Big model tests (see test_zoo_models.py):
backend_test.exclude('test_bvlc_alexnet')
backend_test.exclude('test_densenet121')
backend_test.exclude('test_inception_v1')
backend_test.exclude('test_inception_v2')
backend_test.exclude('test_resnet50')
backend_test.exclude('test_shufflenet')
backend_test.exclude('test_squeezenet')
backend_test.exclude('test_vgg19')
backend_test.exclude('test_zfnet512')

# Support for ONNX Sequence type - NGONNX-789
backend_test.exclude('test_sequence_model')


# Tests which fail on the CPU backend -> NC-330
backend_test.exclude('test_Conv3d_dilated')
backend_test.exclude('test_Conv3d_dilated_strided')

if selected_backend_name == 'IE':
    # segfaults
    backend_test.exclude('test_greater_cpu')
    backend_test.exclude('test_greater_bcast_cpu')
    backend_test.exclude('test_hardmax_axis_0_cpu')
    backend_test.exclude('test_less_cpu')
    backend_test.exclude('test_less_bcast_cpu')
    backend_test.exclude('test_log_cpu')

# NOTE: ALL backend_test.exclude CALLS MUST BE PERFORMED BEFORE THE CALL TO globals().update

OnnxBackendNodeModelTest = None
OnnxBackendSimpleModelTest = None
OnnxBackendPyTorchOperatorModelTest = None
OnnxBackendPyTorchConvertedModelTest = None
globals().update(backend_test.enable_report().test_cases)

# Dynamic Expand -> NGONNX-367
expect_fail('OnnxBackendNodeModelTest.test_expand_dim_changed_cpu')
expect_fail('OnnxBackendNodeModelTest.test_expand_dim_unchanged_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_expand_shape_model1_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_expand_shape_model2_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_expand_shape_model3_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_expand_shape_model4_cpu')

# Dynamic Reshape -> NGONNX-357
expect_fail('OnnxBackendNodeModelTest.test_reshape_extended_dims_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_negative_dim_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_one_dim_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_reduced_dims_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_negative_extended_dims_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_reordered_all_dims_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_reordered_last_dims_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_zero_and_negative_dim_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reshape_zero_dim_cpu')

# Dynamic Tile -> NGONNX-368
expect_fail('OnnxBackendNodeModelTest.test_tile_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tile_precomputed_cpu')
expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_repeat_cpu')
expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_repeat_dim_overflow_cpu')

# Cast (support for String type)
expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT_to_STRING_cpu')
expect_fail('OnnxBackendNodeModelTest.test_cast_STRING_to_FLOAT_cpu')

# Scan -> NGONNX-433
expect_fail('OnnxBackendNodeModelTest.test_scan9_sum_cpu')
expect_fail('OnnxBackendNodeModelTest.test_scan_sum_cpu')

# Compress -> NGONNX-438
expect_fail('OnnxBackendNodeModelTest.test_compress_default_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_compress_0_cpu')
expect_fail('OnnxBackendNodeModelTest.test_compress_1_cpu')
expect_fail('OnnxBackendNodeModelTest.test_compress_negative_axis_cpu')

# Isnan -> NGONNX-440
expect_fail('OnnxBackendNodeModelTest.test_isnan_cpu')

# Constant of Shape -> NGONNX-445
expect_fail('OnnxBackendNodeModelTest.test_constantofshape_float_ones_cpu')
expect_fail('OnnxBackendNodeModelTest.test_constantofshape_int_zeros_cpu')

# Scatter -> NGONNX-446
expect_fail('OnnxBackendNodeModelTest.test_scatter_with_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_scatter_without_axis_cpu')

# Max unpool -> NGONNX-447
expect_fail('OnnxBackendNodeModelTest.test_maxunpool_export_with_output_shape_cpu')
expect_fail('OnnxBackendNodeModelTest.test_maxunpool_export_without_output_shape_cpu')

# OneHot -> NGONNX-486
expect_fail('OnnxBackendNodeModelTest.test_onehot_with_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_onehot_without_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_onehot_negative_indices_cpu')
expect_fail('OnnxBackendNodeModelTest.test_onehot_with_negative_axis_cpu')

# TF id vectorizer -> NGONNX-523
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_batch_onlybigrams_skip0_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_batch_onlybigrams_skip5_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_batch_uniandbigrams_skip5_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_only_bigrams_skip0_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_onlybigrams_levelempty_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_onlybigrams_skip5_cpu')
expect_fail('OnnxBackendNodeModelTest.test_tfidfvectorizer_tf_uniandbigrams_skip5_cpu')

# Non zero -> NGONNX-472
expect_fail('OnnxBackendNodeModelTest.test_nonzero_example_cpu')

# Quantized NGONNX-595
# Scale / zero point not a scalar
expect_fail('OnnxBackendNodeModelTest.test_qlinearconv_cpu')
expect_fail('OnnxBackendNodeModelTest.test_qlinearmatmul_2D_cpu')
expect_fail('OnnxBackendNodeModelTest.test_qlinearmatmul_3D_cpu')
expect_fail('OnnxBackendNodeModelTest.test_matmulinteger_cpu')

# IsInf - NGONNX-528
expect_fail('OnnxBackendNodeModelTest.test_isinf_cpu')
expect_fail('OnnxBackendNodeModelTest.test_isinf_negative_cpu')
expect_fail('OnnxBackendNodeModelTest.test_isinf_positive_cpu')

# Pooling ops NGONNX-597
expect_fail('OnnxBackendNodeModelTest.test_maxpool_2d_ceil_cpu')
expect_fail('OnnxBackendNodeModelTest.test_maxpool_2d_dilations_cpu')
expect_fail('OnnxBackendNodeModelTest.test_averagepool_2d_ceil_cpu')

# Modulus - NGONNX-527
# fmod=0 is not supported
expect_fail('OnnxBackendNodeModelTest.test_mod_broadcast_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_int16_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_int32_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_int64_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_int8_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_uint16_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_uint32_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_uint64_cpu')
expect_fail('OnnxBackendNodeModelTest.test_mod_uint8_cpu')
# float16 is not supported for Sign operator
expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_float16_cpu')

# NonMaxSuppression - NGONNX-526
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_center_point_box_format_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_flipped_coordinates_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_identical_boxes_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_limit_output_size_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_single_box_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_suppress_by_IOU_and_scores_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_suppress_by_IOU_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_two_batches_cpu')
expect_fail('OnnxBackendNodeModelTest.test_nonmaxsuppression_two_classes_cpu')

# Dynamic Slice NGONNX-522, 599
expect_fail('OnnxBackendNodeModelTest.test_slice_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_default_axes_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_default_steps_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_end_out_of_bounds_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_neg_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_neg_steps_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_start_out_of_bounds_cpu')
expect_fail('OnnxBackendNodeModelTest.test_slice_negative_axes_cpu')

# StrNormalizer NGONNX-600
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_export_monday_casesensintive_lower_cpu')
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_export_monday_casesensintive_nochangecase_cpu')
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_export_monday_casesensintive_upper_cpu')
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_export_monday_empty_output_cpu')
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_export_monday_insensintive_upper_twodim_cpu')
expect_fail('OnnxBackendNodeModelTest.test_strnormalizer_nostopwords_nochangecase_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_monday_casesensintive_lower_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_monday_casesensintive_nochangecase_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_monday_casesensintive_upper_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_monday_empty_output_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_monday_insensintive_upper_twodim_cpu')
expect_fail('OnnxBackendSimpleModelTest.test_strnorm_model_nostopwords_nochangecase_cpu')

# RoiAlign - NGONNX-601
expect_fail('OnnxBackendNodeModelTest.test_roialign_cpu')

# Upsample - NGONNX-781
expect_fail('OnnxBackendNodeModelTest.test_upsample_nearest_cpu')

# BitShift - NGONNX-752
expect_fail('OnnxBackendNodeModelTest.test_bitshift_left_uint16_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_left_uint32_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_left_uint64_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_left_uint8_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_right_uint16_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_right_uint32_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_right_uint64_cpu')
expect_fail('OnnxBackendNodeModelTest.test_bitshift_right_uint8_cpu')

# Det - NGONNX-754
expect_fail('OnnxBackendNodeModelTest.test_det_2d_cpu')
expect_fail('OnnxBackendNodeModelTest.test_det_nd_cpu')

# GatherElements, ScatterElements - NGONNX-757
expect_fail('OnnxBackendNodeModelTest.test_gather_elements_0_cpu')
expect_fail('OnnxBackendNodeModelTest.test_gather_elements_1_cpu')
expect_fail('OnnxBackendNodeModelTest.test_gather_elements_negative_indices_cpu')
expect_fail('OnnxBackendNodeModelTest.test_scatter_elements_with_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_scatter_elements_with_negative_indices_cpu')
expect_fail('OnnxBackendNodeModelTest.test_scatter_elements_without_axis_cpu')

# GatherND - NGONNX-758
expect_fail('OnnxBackendNodeModelTest.test_gathernd_example_int32_cpu')

# Resize - NGONNX-782
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_cubic_A_n0p5_exclude_outside_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_cubic_align_corners_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_cubic_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_linear_align_corners_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_linear_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_scales_nearest_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_sizes_cubic_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_sizes_linear_pytorch_half_pixel_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_sizes_nearest_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_downsample_sizes_nearest_tf_half_pixel_for_nn_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_tf_crop_and_resize_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_cubic_A_n0p5_exclude_outside_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_cubic_align_corners_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_cubic_asymmetric_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_cubic_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_linear_align_corners_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_linear_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_scales_nearest_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_sizes_cubic_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_sizes_nearest_ceil_half_pixel_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_sizes_nearest_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_sizes_nearest_floor_align_corners_cpu')
expect_fail('OnnxBackendNodeModelTest.test_resize_upsample_sizes_nearest_round_prefer_ceil_asymmetric_cpu')

# Tests pass on backend with support for nGraph v1 opset.
expect_fail('OnnxBackendNodeModelTest.test_constant_pad_cpu')
expect_fail('OnnxBackendNodeModelTest.test_edge_pad_cpu')
expect_fail('OnnxBackendNodeModelTest.test_reflect_pad_cpu')

# DynamicQuantizeLinear - NGONNX-786
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_cpu')
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_expanded_cpu')
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_max_adjusted_cpu')
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_max_adjusted_expanded_cpu')
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_min_adjusted_cpu')
expect_fail('OnnxBackendNodeModelTest.test_dynamicquantizelinear_min_adjusted_expanded_cpu')

# Range op - NGONNX-787
expect_fail('OnnxBackendNodeModelTest.test_range_float_type_positive_delta_cpu')
expect_fail('OnnxBackendNodeModelTest.test_range_float_type_positive_delta_expanded_cpu')
expect_fail('OnnxBackendNodeModelTest.test_range_int32_type_negative_delta_cpu')
expect_fail('OnnxBackendNodeModelTest.test_range_int32_type_negative_delta_expanded_cpu')

# Unique op - NGONNX-761
expect_fail('OnnxBackendNodeModelTest.test_unique_not_sorted_without_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_unique_sorted_with_axis_3d_cpu')
expect_fail('OnnxBackendNodeModelTest.test_unique_sorted_with_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_unique_sorted_with_negative_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_unique_sorted_without_axis_cpu')

# Round - NGONNX-760
expect_fail('OnnxBackendNodeModelTest.test_round_cpu')

# Operations not supported by nGraph Backends
expect_fail('OnnxBackendNodeModelTest.test_top_k_cpu')
expect_fail('OnnxBackendNodeModelTest.test_top_k_negative_axis_cpu')
expect_fail('OnnxBackendNodeModelTest.test_top_k_smallest_cpu')

# Tests which fail on the INTELGPU backend
if selected_backend_name == 'INTELGPU':
    expect_fail('OnnxBackendNodeModelTest.test_edge_pad_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_erf_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gemm_broadcast_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_2_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_one_hot_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_maxpool_2d_same_upper_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reflect_pad_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_sparse_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_ReflectionPad2d_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_ReplicationPad2d_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_pad_cpu')

# Tests which fail or are very slow on the INTERPRETER backend
if selected_backend_name == 'INTERPRETER':
    # Cast -> NGONNX-764
    expect_fail('OnnxBackendNodeModelTest.test_cast_DOUBLE_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_DOUBLE_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_FLOAT_cpu')

if selected_backend_name == 'CPU':
    # Cast -> NGONNX-764
    expect_fail('OnnxBackendNodeModelTest.test_cast_DOUBLE_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_DOUBLE_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_FLOAT_cpu')

if selected_backend_name == 'PlaidML':
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_sparse_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_ReflectionPad2d_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_ReplicationPad2d_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_pad_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_default_inbounds_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_default_max_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_default_min_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_output_shape_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_exclusive_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_reverse_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_reverse_exclusive_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_negative_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_edge_pad_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_erf_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_2_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_one_hot_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reflect_pad_cpu')
    # Test which fail on PlaidML with INTELGPU
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_pow_cpu')

if selected_backend_name == 'IE':
    # Unsupported primitive of type: Sqrt
    expect_fail('OnnxBackendNodeModelTest.test_acosh_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_acosh_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_asinh_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_asinh_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_instancenorm_epsilon_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_instancenorm_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_mvn_expanded_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_default_axes_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_default_axes_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_do_not_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_do_not_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_keep_dims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_keep_dims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_negative_axes_keep_dims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reduce_l2_negative_axes_keep_dims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_sqrt_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_sqrt_example_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_sqrt_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_symbolic_override_cpu')

    # [NOT_IMPLEMENTED] Input image format BOOL is not supported yet...
    expect_fail('OnnxBackendNodeModelTest.test_and2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and_bcast3v1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and_bcast3v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and_bcast4v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and_bcast4v3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_and_bcast4v4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_not_2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_not_3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_not_4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or_bcast3v1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or_bcast3v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or_bcast4v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or_bcast4v3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_or_bcast4v4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_where_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_where_long_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor4d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor_bcast3v1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor_bcast3v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor_bcast4v2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor_bcast4v3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_xor_bcast4v4d_cpu')

    # Pooling layer. Unsupported mode. Only 4D and 5D blobs are supported as input.
    expect_fail('OnnxBackendNodeModelTest.test_averagepool_1d_default_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_maxpool_1d_default_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_maxpool_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_MaxPool1d_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_MaxPool1d_stride_cpu')

    # Layer y input port 1 is not connected to any data
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_3d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_dilations_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_kernel_shape_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_output_shape_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_pad_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_pads_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convtranspose_with_kernel_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_prelu_broadcast_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_prelu_example_cpu')

    # Cannot cast ngraph node y to CNNLayer!
    expect_fail('OnnxBackendNodeModelTest.test_basic_convinteger_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_convinteger_with_padding_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_dequantizelinear_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_quantizelinear_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_scatternd_cpu')

    # Incorrect precision f64!
    expect_fail('OnnxBackendNodeModelTest.test_cast_DOUBLE_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_DOUBLE_to_FLOAT_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_DOUBLE_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT_to_DOUBLE_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_exclusive_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_reverse_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_1d_reverse_exclusive_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cumsum_2d_negative_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_eyelike_with_dtype_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_mod_mixed_sign_float64_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_add_broadcast_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_add_size1_broadcast_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_add_size1_right_broadcast_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_add_size1_singleton_broadcast_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_addconstant_cpu')

    # Unsupported primitive of type: Ceiling name: y
    expect_fail('OnnxBackendNodeModelTest.test_ceil_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_ceil_example_cpu')

    # Can't convert dims 0 to Layout!
    expect_fail('OnnxBackendNodeModelTest.test_clip_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_default_max_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_default_min_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_inbounds_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_outbounds_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_clip_splitbounds_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gemm_default_scalar_bias_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_pow_bcast_scalar_cpu')

    # RuntimeError: data [<name>] doesn't exist
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT16_to_FLOAT_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_cast_FLOAT_to_FLOAT16_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_constant_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_dropout_default_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_dropout_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_eyelike_populate_off_main_diagonal_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_eyelike_without_dtype_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_identity_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_max_one_input_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_mean_one_input_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_min_one_input_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_shape_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_shape_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_size_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_size_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_sum_one_input_cpu')

    # RuntimeError: [PARAMETER_MISMATCH] Failed to set Blob with precision FP32
    expect_fail('OnnxBackendNodeModelTest.test_equal_bcast_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_equal_cpu')

    # [NOT_IMPLEMENTED] Input image format I64 is not supported yet...
    expect_fail('OnnxBackendNodeModelTest.test_gather_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_gather_negative_indices_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_mod_int64_fmod_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reversesequence_batch_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_reversesequence_time_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_non_float_params_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_Embedding_sparse_cpu')

    # RuntimeError: Cannot cast ngraph node LSTMSequence to CNNLayer!
    expect_fail('OnnxBackendNodeModelTest.test_lstm_defaults_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_lstm_with_initial_bias_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_lstm_with_peepholes_cpu')

    # RuntimeError: Cannot cast ngraph node output to CNNLayer!
    expect_fail('OnnxBackendNodeModelTest.test_gathernd_example_float32_cpu')

    # AssertionError: result mismatch
    expect_fail('OnnxBackendNodeModelTest.test_argmax_default_axis_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_default_axis_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_negative_axis_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_negative_axis_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_no_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmax_no_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_default_axis_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_default_axis_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_negative_axis_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_negative_axis_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_no_keepdims_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_argmin_no_keepdims_random_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_elu_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_axis_2_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_example_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_negative_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_hardmax_one_hot_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_logsoftmax_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_logsoftmax_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_logsoftmax_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_mvn_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_softmax_axis_0_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_softmax_axis_1_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_softmax_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_equal_parts_1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_equal_parts_2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_equal_parts_default_axis_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_variable_parts_1d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_variable_parts_2d_cpu')
    expect_fail('OnnxBackendNodeModelTest.test_split_variable_parts_default_axis_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_chunk_cpu')
    expect_fail('OnnxBackendPyTorchOperatorModelTest.test_operator_symbolic_override_nested_cpu')

    # RuntimeError: Node Split contains empty child edge for index 0
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_GLU_cpu')
    expect_fail('OnnxBackendPyTorchConvertedModelTest.test_GLU_dim_cpu')
