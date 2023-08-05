# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/field_behavior.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/api/field_behavior.proto",
    package="google.api",
    syntax="proto3",
    serialized_options=b"\n\016com.google.apiB\022FieldBehaviorProtoP\001ZAgoogle.golang.org/genproto/googleapis/api/annotations;annotations\242\002\004GAPI",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b"\n\x1fgoogle/api/field_behavior.proto\x12\ngoogle.api\x1a google/protobuf/descriptor.proto*{\n\rFieldBehavior\x12\x1e\n\x1a\x46IELD_BEHAVIOR_UNSPECIFIED\x10\x00\x12\x0c\n\x08OPTIONAL\x10\x01\x12\x0c\n\x08REQUIRED\x10\x02\x12\x0f\n\x0bOUTPUT_ONLY\x10\x03\x12\x0e\n\nINPUT_ONLY\x10\x04\x12\r\n\tIMMUTABLE\x10\x05:Q\n\x0e\x66ield_behavior\x12\x1d.google.protobuf.FieldOptions\x18\x9c\x08 \x03(\x0e\x32\x19.google.api.FieldBehaviorBp\n\x0e\x63om.google.apiB\x12\x46ieldBehaviorProtoP\x01ZAgoogle.golang.org/genproto/googleapis/api/annotations;annotations\xa2\x02\x04GAPIb\x06proto3",
    dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR],
)

_FIELDBEHAVIOR = _descriptor.EnumDescriptor(
    name="FieldBehavior",
    full_name="google.api.FieldBehavior",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="FIELD_BEHAVIOR_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="OPTIONAL",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="REQUIRED",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="OUTPUT_ONLY",
            index=3,
            number=3,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="INPUT_ONLY",
            index=4,
            number=4,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="IMMUTABLE",
            index=5,
            number=5,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=81,
    serialized_end=204,
)
_sym_db.RegisterEnumDescriptor(_FIELDBEHAVIOR)

FieldBehavior = enum_type_wrapper.EnumTypeWrapper(_FIELDBEHAVIOR)
FIELD_BEHAVIOR_UNSPECIFIED = 0
OPTIONAL = 1
REQUIRED = 2
OUTPUT_ONLY = 3
INPUT_ONLY = 4
IMMUTABLE = 5

FIELD_BEHAVIOR_FIELD_NUMBER = 1052
field_behavior = _descriptor.FieldDescriptor(
    name="field_behavior",
    full_name="google.api.field_behavior",
    index=0,
    number=1052,
    type=14,
    cpp_type=8,
    label=3,
    has_default_value=False,
    default_value=[],
    message_type=None,
    enum_type=None,
    containing_type=None,
    is_extension=True,
    extension_scope=None,
    serialized_options=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
)

DESCRIPTOR.enum_types_by_name["FieldBehavior"] = _FIELDBEHAVIOR
DESCRIPTOR.extensions_by_name["field_behavior"] = field_behavior
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

field_behavior.enum_type = _FIELDBEHAVIOR
google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(field_behavior)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
