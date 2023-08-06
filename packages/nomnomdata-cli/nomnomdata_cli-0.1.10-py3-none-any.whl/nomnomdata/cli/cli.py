import hashlib
import json
import logging
import os
import platform
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import click
import coloredlogs
import pkg_resources
import requests
from packaging import version
from pkg_resources import iter_entry_points
from rich import box, print
from rich.panel import Panel
from rich.table import Table

from . import __version__


class BrokenCommand(click.Command):
    def __init__(self, name):

        super().__init__(name)
        util_name = os.path.basename(sys.argv and sys.argv[0] or __file__)
        self.help = "\nEntrypoint could not be loaded \n\n\b\n" + traceback.format_exc()
        self.short_help = (
            f"CLI Plugin failed to load. See `{util_name} {self.name} --help"
        )

    def invoke(self, ctx):
        click.echo(self.help, color=ctx.color)
        ctx.exit(1)


def _get_statefile_name(key):
    key_bytes = sys.prefix.encode("utf-8")
    name = hashlib.sha224(key_bytes).hexdigest()
    return name


current_time = datetime.utcnow()

CLI_CACHE = Path.home() / ".nnd" / "cache" / (_get_statefile_name(sys.prefix) + ".json")

SELFCHECK_DATE_FMT = "%Y-%m-%dT%H:%M:%SZ"


class VersionCheck(object):
    def __init__(self):
        self.state: Dict[str, Any] = {}

        try:
            if CLI_CACHE.exists() and CLI_CACHE.is_file():
                self.state = json.loads(CLI_CACHE.read_text())
        except:
            pass

    def _get_pypi_latest(self, package_name):
        try:
            resp = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=2)
            if resp.ok:
                data = resp.json()
                return data["info"]["version"]
        except:
            pass
        else:
            return False

    def check(self, package_name, current_version):
        package_cache = self.state.get(package_name, {})
        pypi_version = None
        if package_cache and "last_check" in package_cache:
            last_check = datetime.strptime(
                package_cache["last_check"], SELFCHECK_DATE_FMT
            )
            if (current_time - last_check).total_seconds() < 7 * 24 * 60 * 60:
                pypi_version = package_cache["pypi_version"]
        if pypi_version is None:
            pypi_version = self._get_pypi_latest(package_name)
            package_cache = {
                "pypi_version": pypi_version,
                "last_check": current_time.strftime(SELFCHECK_DATE_FMT),
            }
            self.state[package_name] = package_cache
            try:
                CLI_CACHE.parent.mkdir(parents=True, exist_ok=True)
                text = json.dumps(self.state, sort_keys=True, indent=4)
                CLI_CACHE.write_text(text)
            except:
                pass

        if pypi_version:
            pypi_version = version.parse(pypi_version)
            current_version = version.parse(current_version)
            if current_version < pypi_version:
                return True, pypi_version
        return False, None


@click.group()
@click.version_option(version=__version__, prog_name="nomnomdata-cli")
@click.option(
    "-l",
    "--loglevel",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
@click.pass_context
def cli(ctx, loglevel=None):
    """Nom Nom Data Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["LOG_LEVEL"] = loglevel
    coloredlogs.install(
        level=logging.getLevelName(loglevel),
        stream=sys.stdout,
        fmt="%(msecs)d:%(levelname)s:%(name)s:%(message)s",
    )


def main():
    check = VersionCheck()
    plugins = []
    outdated_plugins = []
    for entry in iter_entry_points("nomnomdata.cli_plugins"):
        package_name = entry.dist.project_name
        version = entry.dist.version
        outdated, new_version = check.check(package_name, version)
        plugins.append(f"{package_name}-{version}-({entry.dist.location})")
        if outdated:
            outdated_plugins.append(
                f"[bold yellow]{package_name} is outdated, latest version is {new_version}[/bold yellow]"
            )

    info_table = Table(
        "",
        box=box.MINIMAL,
        show_header=False,
        pad_edge=True,
        show_edge=False,
    )

    msg = [
        ("Version", __version__),
        ("Directory", str(Path.cwd())),
        ("Platform", sys.platform),
        ("Python", platform.python_version()),
        ("Plugins: ", " ".join(plugins)),
    ]

    info_table.add_column()
    for row in msg:
        info_table.add_row(*row)

    outdated, new_version = check.check("nomnomdata-cli", __version__)
    warnings = []
    if outdated:
        warnings.append(
            f"[bold yellow]nomnomdata-cli is outdated, latest version is {new_version}[/bold yellow]"
        )
    for entry_point in iter_entry_points("nomnomdata.cli_plugins"):
        try:
            cli.add_command(entry_point.load())
        except (pkg_resources.VersionConflict, pkg_resources.DistributionNotFound) as e:
            warnings.append(f"[bold red] {entry_point.dist}[/bold red]\t{e.report()}")
            cli.add_command(BrokenCommand(entry_point.name))
        except:
            warnings.append(traceback.format_exc())
            cli.add_command(BrokenCommand(entry_point.name))
    main_table = Table.grid()
    main_table.add_row(info_table)

    if warnings:
        warning_table = Table(
            "Issues",
            box=box.MINIMAL,
            show_header=True,
            pad_edge=True,
            show_edge=False,
            expand=True,
        )
        for row in warnings:
            warning_table.add_row(row)
        main_table.add_row(warning_table)

    print(
        Panel(
            main_table,
            box=box.HEAVY,
            title_align="left",
            title="[orange1]Nom Nom Data CLI[/orange1]",
        )
    )
    cli()
