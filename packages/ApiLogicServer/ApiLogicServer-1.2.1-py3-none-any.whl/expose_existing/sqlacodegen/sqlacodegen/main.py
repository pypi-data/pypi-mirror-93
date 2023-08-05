from __future__ import unicode_literals, division, print_function, absolute_import

import argparse
import io
import sys

"""  FIXME remove
import logic_bank_utils.util as logic_bank_utils
(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="ApiLogicServer", my_file=__file__)
"""

import pkg_resources
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

from expose_existing.sqlacodegen.sqlacodegen.codegen import CodeGenerator


def main(calling_args=None):
    if calling_args:
        args = calling_args
    else:
        parser = argparse.ArgumentParser(description="Generates SQLAlchemy model code from an existing database.")
        parser.add_argument("url", nargs="?", help="SQLAlchemy url to the database")
        parser.add_argument("--version", action="store_true", help="print the version number and exit")
        parser.add_argument("--schema", help="load tables from an alternate schema")
        parser.add_argument("--tables", help="tables to process (comma-separated, default: all)")
        parser.add_argument("--noviews", action="store_true", help="ignore views")
        parser.add_argument("--noindexes", action="store_true", help="ignore indexes")
        parser.add_argument("--noconstraints", action="store_true", help="ignore constraints")
        parser.add_argument("--nojoined", action="store_true", help="don't autodetect joined table inheritance")
        parser.add_argument("--noinflect", action="store_true", help="don't try to convert tables names to singular form")
        parser.add_argument("--noclasses", action="store_true", help="don't generate classes, only tables")
        parser.add_argument("--outfile", help="file to write output to (default: stdout)")
        args = parser.parse_args()

    if args.version:
        version = pkg_resources.get_distribution("sqlacodegen").parsed_version
        print(version.public)
        return
    if not args.url:
        print("You must supply a url\n", file=sys.stderr)
        parser.print_help()
        return

    # Use reflection to fill in the metadata
    engine = create_engine(args.url)
    try:
        # dirty hack for sqlite
        engine.execute("""PRAGMA journal_mode = OFF""")
    except:
        pass
    metadata = MetaData(engine)
    tables = args.tables.split(",") if args.tables else None
    metadata.reflect(engine, args.schema, not args.noviews, tables)

    # Write the generated model code to the specified file or standard output
    outfile = io.open(args.outfile, "w", encoding="utf-8") if args.outfile else sys.stdout
    generator = CodeGenerator(metadata, args.noindexes, args.noconstraints, args.nojoined, args.noinflect, args.noclasses)
    generator.render(outfile)


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    # thanks: https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary/28463329
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def sqlacodegen(db_url: str, models_file: str):
    calling_args = DotDict({})
    calling_args.url = db_url
    calling_args.outfile = models_file
    calling_args.version = False
    main(calling_args)


# print("imported")
# main()
