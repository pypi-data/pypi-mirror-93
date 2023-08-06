# Copyright 2018 NTT Data.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import uuid

from oslo_versionedobjects import fields


# Import fields from oslo.versionedobjects
StringField = fields.StringField
ListOfObjectsField = fields.ListOfObjectsField
ListOfStringsField = fields.ListOfStringsField
DictOfStringsField = fields.DictOfStringsField
DateTimeField = fields.DateTimeField
BooleanField = fields.BooleanField
BaseEnumField = fields.BaseEnumField
Enum = fields.Enum
ObjectField = fields.ObjectField
IntegerField = fields.IntegerField
FieldType = fields.FieldType


class BaseTackerEnum(Enum):
    def __init__(self):
        super(BaseTackerEnum, self).__init__(valid_values=self.__class__.ALL)


class ContainerFormat(BaseTackerEnum):
    AKI = 'AKI'
    AMI = 'AMI'
    ARI = 'ARI'
    BARE = 'BARE'
    DOCKER = 'DOCKER'
    OVA = 'OVA'
    OVF = 'OVF'

    ALL = (AKI, AMI, ARI, BARE, DOCKER, OVA, OVF)


class ContainerFormatFields(BaseEnumField):
    AUTO_TYPE = ContainerFormat()


class DiskFormat(BaseTackerEnum):
    AKI = 'AKI'
    AMI = 'AMI'
    ARI = 'ARI'
    ISO = 'ISO'
    QCOW2 = 'QCOW2'
    RAW = 'RAW'
    VDI = 'VDI'
    VHD = 'VHD'
    VHDX = 'VHDX'
    VMDK = 'VMDK'

    ALL = (AKI, AMI, ARI, ISO, QCOW2, RAW, VDI, VHD, VHDX, VMDK)


class DiskFormatFields(BaseEnumField):
    AUTO_TYPE = DiskFormat()


class PackageOnboardingStateType(BaseTackerEnum):
    CREATED = 'CREATED'
    UPLOADING = 'UPLOADING'
    PROCESSING = 'PROCESSING'
    ONBOARDED = 'ONBOARDED'

    ALL = (CREATED, UPLOADING, PROCESSING, ONBOARDED)


class PackageOnboardingStateTypeField(BaseEnumField):
    AUTO_TYPE = PackageOnboardingStateType()


class PackageOperationalStateType(BaseTackerEnum):
    ENABLED = 'ENABLED'
    DISABLED = 'DISABLED'

    ALL = (ENABLED, DISABLED)


class PackageOperationalStateTypeField(BaseEnumField):
    AUTO_TYPE = PackageOperationalStateType()


class PackageUsageStateType(BaseTackerEnum):
    IN_USE = 'IN_USE'
    NOT_IN_USE = 'NOT_IN_USE'

    ALL = (IN_USE, NOT_IN_USE)


class PackageUsageStateTypeField(BaseEnumField):
    AUTO_TYPE = PackageUsageStateType()


class DictOfNullableField(fields.AutoTypedField):
    AUTO_TYPE = fields.Dict(fields.FieldType(), nullable=True)


class UUID(fields.UUID):
    def coerce(self, obj, attr, value):
        uuid.UUID(str(value))
        return str(value)


class UUIDField(fields.AutoTypedField):
    AUTO_TYPE = UUID()
