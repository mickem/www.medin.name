#! /usr/bin/env python
# encoding: utf-8

import argparse
import os

from subprocess import check_output
from shutil import rmtree


def main():
    TASKS = {
        "setup": setup,
        "html": html,
        "regenerate": regenerate,
        "publish": publish,
        "serve": serve,
        "clean": clean,
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


def setup(ctx):
    """ Install all web dependencies """
    shell_with_npm("npm install")
    old = os.getcwd()
    os.chdir("themes/mickem-bootstrap")
    shell_with_npm("bower install")
    os.chdir(old)

def html(ctx):
    """ Generate html sources (with base configuration) """
    shell_with_npm("{pelican} {input} -o {output} -s {baseconf} {extra}", ctx)


def regenerate(ctx):
    """ Regenerate html sources (with base configuration) """
    ctx["extra"] += ["-r"]
    html(ctx)


def publish(ctx):
    """ Generate html sources (with publish configuration) """
    shell_with_npm("{pelican} {input} -o {output} -s {publishconf} {extra}", ctx)


def serve(ctx):
    """ Start HTML server """
    shell("cd {output} && {python} -m pelican.server {serve_port}", ctx)


def clean(ctx):
    """ Clean output directory and cache """
    rmtree(ctx["output"])
    rmtree(ctx["cache"])


def shell_with_npm(command, ctx={}):
    env_copy = os.environ.copy()
    env_copy["PATH"] += os.pathsep + shell("npm bin")
    print env_copy["PATH"]

    return shell(command, ctx, env_copy)

def shell(command, ctx={}, env=None):
    return check_output(command.format(**ctx), shell=True, universal_newlines=True, env=env)

if __name__ == "__main__":
    main()
