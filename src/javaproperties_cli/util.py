import click
import javaproperties
from   . import __version__

def command(group=False):
    def wrapper(f):
        return click.command(
            cls=click.Group if group else click.Command,
            context_settings={"help_option_names": ["-h", "--help"]},
        )(click.version_option(
            __version__,
            '-V', '--version',
            message=(
                'javaproperties-cli %(version)s'
                f' (javaproperties {javaproperties.__version__})'
            ),
        )(f))
    return wrapper

infile_type = click.Path(
    exists     = True,
    dir_okay   = False,
    readable   = True,
    allow_dash = True,
)

outfile_type = click.Path(dir_okay=False, writable=True, allow_dash=True)

encoding_option = click.option(
    '-E', '--encoding',
    default='iso-8859-1',
    show_default=True,
    help='.properties file encoding',
)
