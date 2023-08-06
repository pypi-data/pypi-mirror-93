import os
import sys
import pathlib
import shutil

from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_string('config_file', None, "Path to experiment's config file.")

def main(argv):
    del argv

    copy_from: str = os.path.join(sys.prefix, 'pulmoscan_resources', 'resources')
    if not os.path.exists(copy_from):
        copy_from: str = os.path.join(sys.prefix, 'local', 'pulmoscan_resources', 'resources')

    copy_to = os.path.join(pathlib.Path().absolute(), 'resources')
    shutil.copytree(copy_from, copy_to)


def entry():
    '''
    An entrypoint for command line tool.
    '''
    app.run(main)


if __name__ == '__main__':
    entry()
