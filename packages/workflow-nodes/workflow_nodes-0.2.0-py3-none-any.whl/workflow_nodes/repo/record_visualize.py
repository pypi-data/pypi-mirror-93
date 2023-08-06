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
from xmlhelpy import argument
from xmlhelpy import Choice
from xmlhelpy import Integer
from xmlhelpy import option

from .main import repo


@repo.command(version="0.1.0")
@apy_command
@argument(
    "start_id", description="The ID of the record to start with.", param_type=Integer
)
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
    "link_level",
    char="l",
    description="The maximum link distance to visualize.",
    default=2,
    param_type=Integer,
)
def record_visualize(start_id, output_file, output_format, link_level):
    """Visualize the links of a given record."""

    if not shutil.which("dot"):
        click.echo("'dot' not found in PATH, maybe Graphviz is not installed?")
        sys.exit(1)

    id_list = [start_id]
    id_list_current_level = [start_id]

    while link_level > 0:
        id_list_next_level = []

        for _id in id_list_current_level:
            items_to = Record(id=_id).get_record_links(direction="to").json()["items"]
            items_from = (
                Record(id=_id).get_record_links(direction="from").json()["items"]
            )

            for item in items_from:
                id_list_next_level.append(item["record_from"]["id"])
            for item in items_to:
                id_list_next_level.append(item["record_to"]["id"])

        id_list_current_level = list(set(id_list_next_level))
        id_list = id_list + id_list_next_level
        link_level = link_level - 1

    id_list = list(set(id_list))

    dot = Digraph(
        format=output_format, node_attr={"color": "lightblue2", "style": "filled"}
    )

    for id in id_list:
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
                    if (
                        results["record_to"]["id"] in id_list
                        and results["record_from"]["id"] in id_list
                    ):
                        dot.edge(
                            f"{results['record_to']['id']}",
                            f"{results['record_from']['id']}",
                            label=f"{results['name']} (ID: {results['id']})",
                        )
                    else:
                        pass
                except Exception as e:
                    click.echo(e)
        else:
            raise_request_error(response=response)

    dot.render(output_file, cleanup=True)
