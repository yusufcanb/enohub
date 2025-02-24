import argparse
import yaml

from loguru import logger
from enohub.config import EnoHubConfig
from enohub.hub import EnOceanHub


class YAMLParseAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        with open(values, "r") as stream:
            try:
                parsed = yaml.safe_load(stream)
                config = EnoHubConfig(**parsed)
                logger.info("Config file parsed.")
                setattr(namespace, self.dest, config)
            except yaml.YAMLError as exc:
                logger.error("Error parsing YAML file")
                logger.exception(exc)


class EnOceanHubCLI(argparse.ArgumentParser):
    def __init__(
        self,
        prog="enohub",
        usage=None,
        description="EnOcean Sensor Hub. Listens ESP3 packets from EnOcean USB 3000 device and pipes into TimescaleDB time-series database.",
        epilog=None,
        parents=[],
        formatter_class=argparse.HelpFormatter,
        prefix_chars="-",
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler="error",
        add_help=True,
        allow_abbrev=True,
    ):
        super().__init__(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
        )

    def run(self):
        self.add_argument(
            "-c",
            "--config",
            required=True,
            action=YAMLParseAction,
            dest="config",
            help="path of the enohub config file",
        )
        args = self.parse_args()
        hub = EnOceanHub(args.config)
        hub.loop()
