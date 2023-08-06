# This file is a part of elabftwapy-cli to interact with an elabFTW instance via a CLI
# Copyright (C) 2021 Karlsruhe Institute of Technology
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import sys
from functools import wraps

import click
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError
from requests.exceptions import SSLError
from xmlhelpy import option

from elabapy_cli.lib.climanager import CLIManager


def apy_command(func):
    """Decorator to handle basic input parameters."""

    option(
        "host",
        char="h",
        description="Host name of the eLabFTW instance to use for the API.",
    )(func)

    option(
        "token", char="k", description="Personal access token (PAT) to use for the API."
    )(func)

    option(
        "skip-verify",
        char="s",
        is_flag=True,
        description="Skip verifying the SSL/TLS certificate of the host.",
    )(func)

    @wraps(func)
    def decorated_command(token, host, skip_verify, *args, **kwargs):
        token = token if token is not None else os.environ.get("ELAB_PAT")
        host = host if host is not None else os.environ.get("ELAB_HOST")
        verify = not skip_verify

        climanager = CLIManager(endpoint=host, token=token, verify=verify)

        kwargs["climanager"] = climanager

        try:
            func(*args, **kwargs)
        except HTTPError as e:
            click.echo(e, err=True)
            sys.exit(1)
        except SSLError as e:
            click.echo(e, err=True)
            click.echo(
                "Use the '-s' option to skip verifying the SSL/TLS certificate of the"
                " host."
            )
            sys.exit(1)
        except ConnectionError as e:
            click.echo(e, err=True)
            click.echo(
                "Could not connect to the host. It could be that the url is"
                " incorrect or the host is temporarily unavailable."
            )
            sys.exit(1)

    return decorated_command
