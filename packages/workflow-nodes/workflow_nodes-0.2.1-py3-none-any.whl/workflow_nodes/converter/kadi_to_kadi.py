# Copyright 2020 Karlsruhe Institute of Technology
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
import json

from kadi_apy import apy_command
from kadi_apy import CLIRecord
from kadi_apy import id_identifier_options
from kadi_apy import KadiAPI
from xmlhelpy import option

from .main import converter


@converter.command(version="0.1.0")
@apy_command
@id_identifier_options(class_type=CLIRecord, helptext="to copy to the second instance")
@option(
    "force",
    char="f",
    description="Force deleting and overwriting existing data",
    is_flag=True,
)
@option(
    "host-2",
    char="H",
    description="Host name of the second Kadi4Mat instance to use for the API.",
    required=True,
)
@option(
    "token-2",
    char="K",
    description="Second personal access token (PAT) to use for the API.",
    required=True,
)
@option(
    "skip-verify-2",
    char="S",
    is_flag=True,
    description="Skip verifying the SSL/TLS certificate of the second host.",
)
@option(
    "file-path",
    char="p",
    description="File path for downloading/uploading files.",
    required=True,
)
def kadi_to_kadi(record, force, host_2, token_2, skip_verify_2, file_path):
    """Copy record data between two Kadi4Mat instances."""

    meta = record.meta
    record.get_file(file_path, force)

    KadiAPI.token = token_2
    KadiAPI.host = host_2
    KadiAPI.verify = skip_verify_2

    record_2 = CLIRecord(
        identifier=meta["identifier"], title=meta["title"], create=True
    )

    record_2.set_attribute(description=meta["description"])
    record_2.set_attribute(type=meta["type"])

    for tag in meta["tags"]:
        record_2.add_tag(tag)

    record_2.add_metadata(metadata=json.dumps(meta["extras"]), file=None, force=force)

    record_2.upload_file(file_name=file_path, force=force, pattern="*")
