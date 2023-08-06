# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml._common._error_definition import error_decorator
from azureml._common._error_definition.error_strings import AzureMLErrorStrings

from azureml._common._error_definition.user_error import (
    ArgumentOutOfRange,
    InvalidData,
    Timeout,
    BadData,
    Authorization,
    ConnectionFailure
)


@error_decorator(use_parent_error_code=True)
class ArgumentSizeOutOfRange(ArgumentOutOfRange):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.ARGUMENT_SIZE_OUT_OF_RANGE


@error_decorator(use_parent_error_code=True)
class DownloadFailed(ConnectionFailure):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.DOWNLOAD_FAILED


@error_decorator(use_parent_error_code=True)
class InvalidColumnLength(InvalidData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.INVALID_COLUMN_LENGTH


@error_decorator(use_parent_error_code=True)
class FlushTaskTimeout(Timeout):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.TIMEOUT_FLUSH_TASKS


@error_decorator(use_parent_error_code=True)
class BadDataDownloaded(BadData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.BAD_DATA_DOWNLOAD


@error_decorator(use_parent_error_code=True)
class BadDataUpload(BadData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.BAD_DATA_UPLOAD


@error_decorator(use_parent_error_code=True)
class AuthorizationStorageAccount(Authorization):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.AUTHORIZATION_BLOB_STORAGE


@error_decorator(use_parent_error_code=True)
class InvalidColumnData(InvalidData):
    @property
    def message_format(self):
        return AzureMLErrorStrings.UserErrorStrings.INVALID_COLUMN_DATA
