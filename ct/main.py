import click
from click.core import Context
import click_extra as click
import logging
from click import style
from src.endpoint.to_main import To_main

class Main:
    @staticmethod
    def merge(ctx: Context, **kwargs) -> dict:
        return {**ctx.obj, **kwargs}

    @click.extra_group()
    @click.version_option(version='1.0.0', prog_name='By : Aza Ahmad',
                          message=f'{click.style("%(prog)s", fg="bright_magenta")} version {click.style("%(version)s", fg="bright_magenta")}')
    @click.pass_context
    def main(ctx: Context, **kwargs) -> None:
        """ Engine Smart Crawling by aza """
        ctx.obj = kwargs

    @main.command()
    @click.pass_context
    def case_table(ctx: click.Context) -> None:
        """case table"""
        if 'errors' not in ctx.obj:
            ctx.obj['errors'] = []

        To_main().table_main()





if __name__ == "__main__":
    Main.main()

