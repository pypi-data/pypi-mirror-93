# -*- coding: utf-8 -*-
import json

import click
from chaoslib.control import load_global_controls
from chaoslib.exceptions import ChaosException
from chaoslib.experiment import ensure_experiment_is_valid, run_experiment
from chaoslib.settings import get_loaded_settings, load_settings
from chaoslib.types import Schedule, Strategy
from logzero import logger

from pdchaoscli.event import EventHandler
from pdchaoscli.experiment import builder
from pdchaoscli.loader import load_attack, load_endpoint
from pdchaoscli.logging import configure_logger
from pdchaoscli.settings import PDCLI_CONFIG_PATH, set_attack, set_endpoint


@click.group()
@click.option('--verbose', is_flag=True, help='Display debug level traces.')
@click.option('--no-log-file', is_flag=True,
              help='Disable logging to file entirely.')
@click.option('--log-file', default="pdchaoscli.log", show_default=True,
              help="File path where to write the command's log.")
@click.pass_context
def cli(ctx: click.Context, verbose: bool = False,
        no_log_file: bool = False, log_file: str = "pdchaoscli.log"):
    if no_log_file:
        configure_logger(verbose=verbose)
    else:
        configure_logger(verbose=verbose, log_file=log_file)

    subcommand = ctx.invoked_subcommand

    # make it nicer for going through the log file
    logger.debug("#" * 79)
    logger.debug("Running command '{}'".format(subcommand))

    ctx.obj = {
        "settings_path": click.format_filename(PDCLI_CONFIG_PATH)
    }
    logger.debug("Using settings file '{}'".format(ctx.obj["settings_path"]))


@cli.command()
@click.option('--rollback-strategy',
              default="default", show_default=False,
              help="Rollback runtime strategy. Default is to never play them on interruption or failed hypothesis.",
              type=click.Choice(['default', 'always', 'never', 'deviated']))
@click.option('--hypothesis-strategy',
              default="default",
              type=click.Choice([
                  "default", "before-method-only", "after-method-only", "during-method-only", "continously"
              ], case_sensitive=True),
              help='Strategy to execute the hypothesis during the run.')
@click.option('--hypothesis-frequency',
              default=1.0, type=float,
              help='Pace at which running the hypothesis. Only applies when strategy is either: '
                   'during-method-only or continuously')
@click.option('--fail-fast',
              is_flag=True, default=False,
              help='When running in the during-method-only or continuous strategies, indicate the hypothesis can fail '
                   'the scenario as soon as it deviates once. Otherwise, keeps running until the end of the scenario.')
@click.option('--dry', is_flag=True,
              help='Run the attack without executing activities.')
@click.argument('definition',
                required=False)
@click.pass_context
def run(ctx: click.Context, definition: str, dry: bool = False,
        rollback_strategy: str = "default",
        hypothesis_strategy: str = "default",
        hypothesis_frequency: float = 1.0, fail_fast: bool = False):
    """Run the attack or scenario DEFINITION and print its journal."""

    settings = load_settings(PDCLI_CONFIG_PATH) or get_loaded_settings()

    # load attack from proofdock
    try:
        set_endpoint(settings, load_endpoint())
        attack = load_attack(settings, definition)
        set_attack(settings, attack)

        # build a CTK experiment based on the attack or scenario
        experiment = builder.build(attack)
    except Exception as x:
        logger.error(str(x))
        logger.debug(x)
        exit(1)

    load_global_controls(settings)

    try:
        ensure_experiment_is_valid(experiment)
    except ChaosException as x:
        logger.error(str(x))
        logger.debug(x)
        exit(1)

    experiment["dry"] = dry
    settings.setdefault("runtime", {}).setdefault("rollbacks", {}).setdefault("strategy", rollback_strategy)
    hypothesis_strategy = Strategy.from_string(hypothesis_strategy)
    schedule = Schedule(continous_hypothesis_frequency=hypothesis_frequency, fail_fast=fail_fast)
    event_handlers = [EventHandler(settings)]

    journal = run_experiment(
        experiment, settings=settings, event_handlers=event_handlers, strategy=hypothesis_strategy, schedule=schedule)
    run_has_deviated = journal.get("deviated", False)
    run_has_failed = journal["status"] != "completed"

    if run_has_failed or run_has_deviated:
        exit(1)

    click.echo(json.dumps(journal))
