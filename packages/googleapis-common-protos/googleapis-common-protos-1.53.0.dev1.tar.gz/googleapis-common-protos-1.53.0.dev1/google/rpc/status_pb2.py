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
# source: google/rpc/status.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/rpc/status.proto",
    package="google.rpc",
    syntax="proto3",
    serialized_options=b"\n\016com.google.rpcB\013StatusProtoP\001Z7google.golang.org/genproto/googleapis/rpc/status;status\370\001\001\242\002\003RPC",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n\x17google/rpc/status.proto\x12\ngoogle.rpc\x1a\x19google/protobuf/any.proto"N\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\x12%\n\x07\x64\x65tails\x18\x03 \x03(\x0b\x32\x14.google.protobuf.AnyBa\n\x0e\x63om.google.rpcB\x0bStatusProtoP\x01Z7google.golang.org/genproto/googleapis/rpc/status;status\xf8\x01\x01\xa2\x02\x03RPCb\x06proto3',
    dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR],
)


_STATUS = _descriptor.Descriptor(
    name="Status",
    full_name="google.rpc.Status",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="code",
            full_name="google.rpc.Status.code",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="message",
            full_name="google.rpc.Status.message",
            index=1,
            number=2,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="details",
            full_name="google.rpc.Status.details",
            index=2,
            number=3,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=66,
    serialized_end=144,
)

_STATUS.fields_by_name["details"].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name["Status"] = _STATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Status = _reflection.GeneratedProtocolMessageType(
    "Status",
    (_message.Message,),
    {
        "DESCRIPTOR": _STATUS,
        "__module__": "google.rpc.status_pb2"
        # @@protoc_insertion_point(class_scope:google.rpc.Status)
    },
)
_sym_db.RegisterMessage(Status)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
