# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feast/core/Runner.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='feast/core/Runner.proto',
  package='feast.core',
  syntax='proto3',
  serialized_options=b'\n\020feast.proto.coreB\013RunnerProtoZ3github.com/feast-dev/feast/sdk/go/protos/feast/core',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x66\x65\x61st/core/Runner.proto\x12\nfeast.core\"i\n\x19\x44irectRunnerConfigOptions\x12\x19\n\x11targetParallelism\x18\x01 \x01(\x05\x12\x1b\n\x13\x64\x65\x61\x64LetterTableSpec\x18\x02 \x01(\t\x12\x14\n\x0ctempLocation\x18\x03 \x01(\t\"\x8e\x05\n\x1b\x44\x61taflowRunnerConfigOptions\x12\x0f\n\x07project\x18\x01 \x01(\t\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\x12\n\nworkerZone\x18\x03 \x01(\t\x12\x16\n\x0eserviceAccount\x18\x04 \x01(\t\x12\x0f\n\x07network\x18\x05 \x01(\t\x12\x12\n\nsubnetwork\x18\x06 \x01(\t\x12\x19\n\x11workerMachineType\x18\x07 \x01(\t\x12\x1c\n\x14\x61utoscalingAlgorithm\x18\x08 \x01(\t\x12\x14\n\x0cusePublicIps\x18\t \x01(\x08\x12\x14\n\x0ctempLocation\x18\n \x01(\t\x12\x15\n\rmaxNumWorkers\x18\x0b \x01(\x05\x12\x1b\n\x13\x64\x65\x61\x64LetterTableSpec\x18\x0c \x01(\t\x12\x43\n\x06labels\x18\r \x03(\x0b\x32\x33.feast.core.DataflowRunnerConfigOptions.LabelsEntry\x12\x12\n\ndiskSizeGb\x18\x0e \x01(\x05\x12\x1d\n\x15\x65nableStreamingEngine\x18\x0f \x01(\x08\x12\x16\n\x0eworkerDiskType\x18\x10 \x01(\t\x12\x65\n\x17kafkaConsumerProperties\x18\x11 \x03(\x0b\x32\x44.feast.core.DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a>\n\x1cKafkaConsumerPropertiesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42T\n\x10\x66\x65\x61st.proto.coreB\x0bRunnerProtoZ3github.com/feast-dev/feast/sdk/go/protos/feast/coreb\x06proto3'
)




_DIRECTRUNNERCONFIGOPTIONS = _descriptor.Descriptor(
  name='DirectRunnerConfigOptions',
  full_name='feast.core.DirectRunnerConfigOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='targetParallelism', full_name='feast.core.DirectRunnerConfigOptions.targetParallelism', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deadLetterTableSpec', full_name='feast.core.DirectRunnerConfigOptions.deadLetterTableSpec', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tempLocation', full_name='feast.core.DirectRunnerConfigOptions.tempLocation', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=144,
)


_DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY = _descriptor.Descriptor(
  name='LabelsEntry',
  full_name='feast.core.DataflowRunnerConfigOptions.LabelsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='feast.core.DataflowRunnerConfigOptions.LabelsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='feast.core.DataflowRunnerConfigOptions.LabelsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=692,
  serialized_end=737,
)

_DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY = _descriptor.Descriptor(
  name='KafkaConsumerPropertiesEntry',
  full_name='feast.core.DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='feast.core.DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='feast.core.DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=739,
  serialized_end=801,
)

_DATAFLOWRUNNERCONFIGOPTIONS = _descriptor.Descriptor(
  name='DataflowRunnerConfigOptions',
  full_name='feast.core.DataflowRunnerConfigOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='project', full_name='feast.core.DataflowRunnerConfigOptions.project', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region', full_name='feast.core.DataflowRunnerConfigOptions.region', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workerZone', full_name='feast.core.DataflowRunnerConfigOptions.workerZone', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='serviceAccount', full_name='feast.core.DataflowRunnerConfigOptions.serviceAccount', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='network', full_name='feast.core.DataflowRunnerConfigOptions.network', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='subnetwork', full_name='feast.core.DataflowRunnerConfigOptions.subnetwork', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workerMachineType', full_name='feast.core.DataflowRunnerConfigOptions.workerMachineType', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='autoscalingAlgorithm', full_name='feast.core.DataflowRunnerConfigOptions.autoscalingAlgorithm', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='usePublicIps', full_name='feast.core.DataflowRunnerConfigOptions.usePublicIps', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tempLocation', full_name='feast.core.DataflowRunnerConfigOptions.tempLocation', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maxNumWorkers', full_name='feast.core.DataflowRunnerConfigOptions.maxNumWorkers', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deadLetterTableSpec', full_name='feast.core.DataflowRunnerConfigOptions.deadLetterTableSpec', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='labels', full_name='feast.core.DataflowRunnerConfigOptions.labels', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='diskSizeGb', full_name='feast.core.DataflowRunnerConfigOptions.diskSizeGb', index=13,
      number=14, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enableStreamingEngine', full_name='feast.core.DataflowRunnerConfigOptions.enableStreamingEngine', index=14,
      number=15, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workerDiskType', full_name='feast.core.DataflowRunnerConfigOptions.workerDiskType', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kafkaConsumerProperties', full_name='feast.core.DataflowRunnerConfigOptions.kafkaConsumerProperties', index=16,
      number=17, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY, _DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=801,
)

_DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY.containing_type = _DATAFLOWRUNNERCONFIGOPTIONS
_DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY.containing_type = _DATAFLOWRUNNERCONFIGOPTIONS
_DATAFLOWRUNNERCONFIGOPTIONS.fields_by_name['labels'].message_type = _DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY
_DATAFLOWRUNNERCONFIGOPTIONS.fields_by_name['kafkaConsumerProperties'].message_type = _DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY
DESCRIPTOR.message_types_by_name['DirectRunnerConfigOptions'] = _DIRECTRUNNERCONFIGOPTIONS
DESCRIPTOR.message_types_by_name['DataflowRunnerConfigOptions'] = _DATAFLOWRUNNERCONFIGOPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DirectRunnerConfigOptions = _reflection.GeneratedProtocolMessageType('DirectRunnerConfigOptions', (_message.Message,), {
  'DESCRIPTOR' : _DIRECTRUNNERCONFIGOPTIONS,
  '__module__' : 'feast.core.Runner_pb2'
  # @@protoc_insertion_point(class_scope:feast.core.DirectRunnerConfigOptions)
  })
_sym_db.RegisterMessage(DirectRunnerConfigOptions)

DataflowRunnerConfigOptions = _reflection.GeneratedProtocolMessageType('DataflowRunnerConfigOptions', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY,
    '__module__' : 'feast.core.Runner_pb2'
    # @@protoc_insertion_point(class_scope:feast.core.DataflowRunnerConfigOptions.LabelsEntry)
    })
  ,

  'KafkaConsumerPropertiesEntry' : _reflection.GeneratedProtocolMessageType('KafkaConsumerPropertiesEntry', (_message.Message,), {
    'DESCRIPTOR' : _DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY,
    '__module__' : 'feast.core.Runner_pb2'
    # @@protoc_insertion_point(class_scope:feast.core.DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry)
    })
  ,
  'DESCRIPTOR' : _DATAFLOWRUNNERCONFIGOPTIONS,
  '__module__' : 'feast.core.Runner_pb2'
  # @@protoc_insertion_point(class_scope:feast.core.DataflowRunnerConfigOptions)
  })
_sym_db.RegisterMessage(DataflowRunnerConfigOptions)
_sym_db.RegisterMessage(DataflowRunnerConfigOptions.LabelsEntry)
_sym_db.RegisterMessage(DataflowRunnerConfigOptions.KafkaConsumerPropertiesEntry)


DESCRIPTOR._options = None
_DATAFLOWRUNNERCONFIGOPTIONS_LABELSENTRY._options = None
_DATAFLOWRUNNERCONFIGOPTIONS_KAFKACONSUMERPROPERTIESENTRY._options = None
# @@protoc_insertion_point(module_scope)
