#! /usr/bin/env python
# encoding: utf-8

import argparse
import os

from subprocess import check_output
from shutil import rmtree


def main():
    TASKS = {
        "html": html,
        "develop": develop,
        "publish": publish,
        "serve": serve,
        "clean": clean,
        "setup": setup,
    }

    epilog = "Tasks:\n"

    for task_name, task in TASKS.items():
        epilog += "\t{} - {}\n".format(task_name, task.__doc__)

    parser = argparse.ArgumentParser(
            description="medin.name build system", 
            epilog=epilog, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tasks", metavar="task", nargs="+", help="Tasks to execute (in-order)")
    parser.add_argument("-i", "--input", default="content", help="Input directory")
    parser.add_argument("-o", "--output", default="output", help="Output directory")
    parser.add_argument("-c", "--cache", default="cache", help="Cache directory")
    parser.add_argument("-bc", "--baseconf", default="pelicanconf.py", help="Base configuration file")
    parser.add_argument("-pc", "--publishconf", default="publishconf.py", help="Publish configuration file")
    parser.add_argument("-p", "--serve-port", type=int, default=8000, help="Change port where HTML server listens on")
    parser.add_argument("-d", "--debug", action="store_true", help="Activate debug logging")
    parser.add_argument("-e", "--extra", nargs="*", default=[])

    parser.add_argument("--pelican", default="pelican", help="Pelican exec")
    parser.add_argument("--python", default="python", help="Python exec")

    args = vars(parser.parse_args())

    if args["debug"]:
        args["extra"] += ["-D"]
        print("args: {}".format(repr(args)))

    args["extra"] = " ".join(args["extra"])

    for task in args["tasks"]:
        TASKS[task](args)


def html(ctx):
    """ Generate html sources (with base configuration) """
    shell("{pelican} {input} -o {output} -s {baseconf} {extra}", ctx)


def develop(ctx):
    """ Run interactively to facilitate development """
    ctx["extra"] += " -r"
    html(ctx)


def publish(ctx):
    """ Generate html sources (with publish configuration) """
    shell("{pelican} {input} -o {output} -s {publishconf} {extra}", ctx)


def serve(ctx):
    """ Start HTML server """
    shell("cd {output} && {python} -m pelican.server {serve_port}", ctx)

def setup(ctx):
    """ Setup python and install all dependencies """
    shell("pip install pelican", ctx)
    shell("pip install beautifulsoup4", ctx)
    shell("pip install markdown", ctx)
    shell("pip install pillow", ctx)
    shell("pip install webassets", ctx)
    shell("pip install pelican-advthumbnailer", ctx)


def clean(ctx):
    """ Clean output directory and cache """
    rmtree(ctx["output"])
    rmtree(ctx["cache"])

def shell(command, ctx={}, env=None):
    env = os.environ.copy()
    if os.path.isfile(".path"):
        with open(".path") as f:
            env["PATH"] = env["PATH"] + ";" + ";".join(map(lambda a:a.strip(), f.readlines()))
    return check_output(command.format(**ctx), shell=True, universal_newlines=True, env=env)

if __name__ == "__main__":
    main()
