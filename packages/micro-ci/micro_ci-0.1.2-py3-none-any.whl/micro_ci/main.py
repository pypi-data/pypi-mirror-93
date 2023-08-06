"""Main module of Micro-CI."""
# pylint: disable=unsubscriptable-object

import subprocess
import tempfile
from typing import Any, Dict, List, Optional

import yaml


def main(disable: Optional[List] = None) -> None:
    """Monolithic main function."""

    with open(".gitlab-ci.yml", "r") as file:
        try:
            config: Dict[str, Any] = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    stages = config["stages"]
    only = "merge_requests"

    variables = {}
    try:
        variables = config["variables"]
    except ValueError:
        pass

    warnings = []

    for stage in stages:
        if disable and stage in disable:
            continue
        jobs = []
        for name, job in config.items():
            try:
                if job["stage"] == stage:
                    jobs.append(name)
            except (TypeError, KeyError):
                pass  # ignore when job isn't a dict or doesn't contain "stage"

        for job in jobs:
            jc = config[job]
            if (
                "only" not in jc
                or only in jc["only"]
                or "refs" in jc["only"]
                and only in jc["only"]["refs"]
            ):
                try:
                    script = jc["script"]
                    with tempfile.NamedTemporaryFile() as tmp:
                        fh = open(tmp.name, "w")
                        print("#!/bin/bash", file=fh)
                        for name, value in variables.items():
                            print(f"{name}={value}")
                            print(f"{name}={value}", file=fh)
                        for line in script:
                            print(f"{line}")
                            print(f"{line}", file=fh)
                        fh.close()

                        try:
                            subprocess.run(["bash", f"{tmp.name}"], check=True)
                        except subprocess.CalledProcessError:
                            if "allow_failure" in jc:
                                af = jc["allow_failure"]
                            else:
                                af = False

                            if af:
                                warnings.append(
                                    f"Micro-CI: Job {job} in stage {stage} failed, "
                                    "but was allowed to fail."
                                )
                                print(
                                    f"Micro-CI: Job {job} in stage {stage} failed, "
                                    "but was allowed to fail."
                                )
                            else:
                                print(f"Micro-CI: Job {job} in stage {stage} failed. Exiting.")
                                exit(1)

                except KeyError:
                    pass

    print("Micro-CI: All stages done, no errors.")
    if warnings:
        for w in warnings:
            print(w)


if __name__ == "__main__":
    main()
