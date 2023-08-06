import click
import nabg


@click.command()
@click.option(
    "--number-of-sentences", "-n", default=1, help="Number of sentences to generate."
)
@click.option(
    "--topic", "-t", default=None, help="Topic on which to generate bullshit."
)
def main(n: int, topic: str):
    print(nabg.ionize(n, topic))


if __name__ == "__main__":
    main()