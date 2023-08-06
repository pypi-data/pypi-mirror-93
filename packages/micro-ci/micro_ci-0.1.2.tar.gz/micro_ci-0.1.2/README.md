# Micro-CI

_Micro-CI_ is a tiny package that allow you to run entire continuous integration
(CI) pipelines locally, without having to run all commands manually or
maintaining separate scripts for it.

> :warning: This project is still in _alpha_ stage. This means that interfaces
might change more often than expected. If you have any kind of issue, please
drop me a line: [edgar.klenske@gauss-ml.com](mailto:edgar.klenske@gauss-ml.com).

## Introduction

Have you ever pushed to a git repository, just to see one component of the CI
pipeline fail? The next time you run `pylint`, `mypy`, `flake8` and all the
other tools manually before pushing changes. Maybe you have created a script. Or
you even set up pre-commit hooks to run things automatically. But once something
changes in the CI pipeline, you have to update your pre-commit hooks again.
That's a waste of time!

Micro-CI reads the GitLab CI configuration file `.gitlab-ci.yml` and lets you
run all stages with one command. Therefore, your local dry-run is always
consistent with the "official" CI pipeline.

## Getting Started

You can install _Micro-CI_ with PIP easily:
```bash
pip install micro-ci
```

From now on, you can just run `mci` in the folder where your `.gitlab-ci.yml`
file is located.

`mci` runs in the context `merge_request`, so that all those stages should be
executed that are run in a merge request pipeline.
