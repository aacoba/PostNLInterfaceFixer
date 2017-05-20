import os
import glob
import filerepair
import click

@click.command()
@click.option("--input_dir", prompt="input directory", help="The input directory of the PostNL Files", type=click.Path())
@click.option("--output_dir", prompt="output directory", help="The output directory of the PostNL Files", type=click.Path())
@click.option("--delete", default=False, help="Delete input files after repair", type=bool)
def batch_process(input_dir, output_dir, delete=False):
    for file in glob.glob(input_dir):
        fixer = filerepair.PostNlFileParser(file)
        save_path = os.path.join(output_dir, os.path.basename(file))
        fixer.save_as(save_path)
        print(save_path)


if __name__ == "__main__":
    batch_process()