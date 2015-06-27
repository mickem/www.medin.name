#! /usr/bin/env python
# encoding: utf-8

import argparse
import os

from subprocess import check_output
from shutil import rmtree


def main():
    TASKS = {
        "setup": setup,
        "develop": develop,
        "publish": publish,
        "clean": clean,
    }

    epilog = "Tasks:\n"

    for task_name, task in TASKS.items():
        epilog += "\t{} - {}\n".format(task_name, task.__doc__)

    parser = argparse.ArgumentParser(
            description="mickem-bootstrap pelican theme", 
            epilog=epilog, 
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tasks", metavar="task", nargs="+", help="Tasks to execute (in-order)")
    args = vars(parser.parse_args())

    for task in args["tasks"]:
        TASKS[task](args)


def setup(ctx):
    """ Install all web dependencies """
    shell_with_npm("npm install")
    shell_with_npm("bower install")

def clean(ctx):
    """ Clean output directory and cache """
    rmtree(ctx["output"])
    rmtree(ctx["cache"])

def develop(ctx):
    """ Run interactively to facilitate development """
    shell_with_npm("gulp watch")

def publish(ctx):
    """ Generate release artefacts """
    shell_with_npm("gulp build")

def shell_with_npm(command, ctx={}):
    env_copy = os.environ.copy()
    env_copy["PATH"] += os.pathsep + shell("npm bin").strip()
    return shell(command, ctx, env_copy)

def shell(command, ctx={}, env=os.environ.copy()):
    if os.path.isfile(".path"):
        with open(".path") as f:
            env["PATH"] = env["PATH"] + ";" + ";".join(map(lambda a:a.strip(), f.readlines()))
    return check_output(command.format(**ctx), shell=True, universal_newlines=True, env=env)

if __name__ == "__main__":
    main()
