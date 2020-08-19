# Copyright 2019-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import pytest

import braket.ir.jaqcd as instruction
from braket.default_simulator import noise_operations
from braket.default_simulator.operation_helpers import check_CPTP, from_braket_instruction
from braket.ir.jaqcd import shared_models

testdata = [
    (instruction.Bit_Flip(target=5, prob=0.01), (5,), noise_operations.Bit_Flip),
    (instruction.Phase_Flip(target=6, prob=0.23), (6,), noise_operations.Phase_Flip),
    (instruction.Depolarizing(target=3, prob=0.45), (3,), noise_operations.Depolarizing),
    (instruction.Amplitude_Damping(target=3, prob=0.67), (3,), noise_operations.Amplitude_Damping),
    (
        instruction.Kraus(
            targets=[4],
            matrices=[
                [[[0.8, 0], [0, 0]], [[0, 0], [0.8, 0]]],
                [[[0, 0], [0, 0.6]], [[0.6, 0], [0, 0]]],
            ],
        ),
        (4,),
        noise_operations.Kraus,
    ),
]


@pytest.mark.parametrize("instruction, targets, operation_type", testdata)
def test_gate_operation_matrix_is_CPTP(instruction, targets, operation_type):
    check_CPTP(from_braket_instruction(instruction).matrices)


@pytest.mark.parametrize("instruction, targets, operation_type", testdata)
def test_from_braket_instruction(instruction, targets, operation_type):
    operation_instance = from_braket_instruction(instruction)
    assert isinstance(operation_instance, operation_type)
    assert operation_instance.targets == targets


@pytest.mark.xfail(raises=ValueError)
def test_from_braket_instruction_unsupported_instruction():
    from_braket_instruction(shared_models.DoubleTarget(targets=[4, 3]))