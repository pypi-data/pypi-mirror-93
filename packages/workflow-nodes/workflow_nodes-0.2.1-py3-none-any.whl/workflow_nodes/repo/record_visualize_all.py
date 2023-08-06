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
import shutil
import sys

import click
from graphviz import Digraph
from kadi_apy import apy_command
from kadi_apy import raise_request_error
from kadi_apy import Record
from kadi_apy import SearchResource
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import option

from .main import repo


@repo.command(version="0.1.0")
@apy_command
@argument(
    "output_file",
    description="The filename of the resulting graph. The correct file extension is"
    " appended to the name depending on the format.",
)
@option(
    "output_format",
    char="f",
    description="Output format of the record graph.",
    default="svg",
    param_type=Choice(["svg", "pdf", "png"]),
)
@option(
    "linked_only",
    char="l",
    is_flag=True,
    description="Flag indicating whether only records with at least one link should be"
    " shown.",
)
def record_visualize_all(output_file, output_format, linked_only):
    """Visualize a user's records and their links."""

    if not shutil.which("dot"):
        click.echo("'dot' not found in PATH, maybe Graphviz is not installed?")
        sys.exit(1)

    resource = SearchResource()
    responce = resource.search_items_user(item=Record, user=resource.pat_user_id)
    payload = responce.json()
    total_pages = payload["_pagination"]["total_pages"]

    record_ids = []
    for i in range(total_pages):
        response = resource.search_items_user(
            item=Record, user=resource.pat_user_id, page=i + 1
        )
        payload = response.json()
        for item in payload["items"]:
            record_id = item["id"]
            record = Record(id=record_id)

            if linked_only:
                if (
                    not record.get_record_links(direction="to").json()["items"]
                    and not record.get_record_links(direction="from").json()["items"]
                ):
                    continue

                record_ids.append(item["id"])
            else:
                record_ids.append(item["id"])

    dot = Digraph(
        format=output_format, node_attr={"color": "lightblue2", "style": "filled"}
    )

    for id in record_ids:
        record = Record(id=id)
        meta = record.meta

        dot.node(
            f"{record.id}",
            f"@{meta['identifier']} (ID: {record.id})",
            shape="ellipse",
            href=meta["_links"]["self"].replace("/api", ""),
        )
        response = record.get_record_links()

        if response.status_code == 200:
            payload = response.json()

            for results in payload["items"]:
                try:
                    dot.edge(
                        f"{results['record_to']['id']}",
                        f"{results['record_from']['id']}",
                        label=f"{results['name']} (ID: {results['id']})",
                    )
                except Exception as e:
                    click.echo(e)
        else:
            raise_request_error(response=response)

    dot.render(output_file, cleanup=True)
