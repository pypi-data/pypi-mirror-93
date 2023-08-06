"""Command-line interface."""
import click
from . import server

@click.command()
@click.version_option()
@click.argument("ofx_file")
def main(ofx_file) -> None:
    """Will I have money tomorrow ?."""
    try:
        occ = open("occ.save", "r").read()
        logging.debug("occ read")
    except:
        pass
    server.main(ofx_file)
    

if __name__ == "__main__":
    main(prog_name="wihmt")  # pragma: no cover
