# Stackzou
[![Tests](https://github.com/SamK/stackzou/actions/workflows/tests.yml/badge.svg)](https://github.com/SamK/stackzou/actions/workflows/tests.yml)

A command line utility to deploy a stack on Docker Swarm.

## Features

* multi-environment
* env variables
* config template

## Usage

Deploy the prod environment:

```
stackzou env prod deploy
```

## Project structure

Your project **must** contain these files:

* `/docker-compose.yml`: the Docker Compose file
* `/envs/`: the directory where the environments are stored.
   Each subdirectory is considered an environment and must contain
   a `docker-compose.override.yml` file with the values specific to its environment.

Your project **can** contain these files:

* **dotenv files** are any file that ends with `.env`.
   They are read in this order:

   1. at the root of the project
   1. inside a environment directory.
   1. `~/.secrets/containers/${STACK_NAME}.env` is read by stackzou.

   The files `/envs/*/.configs.env` are reserved for Stackzou.
* **`/configs/`** is the directory where the "Docker Configs" files are stored.
   Stackzou reads the content of this directory and creates a "Docker Config" with each file it finds.
   If the filename ends with `.subst`, Stackzou attemps to render the file with the `envsubst` command.

Your project structure might looke like this:

```
./
├── configs/
│   ├── service1/
│   │   └── config.cfg
│   └── service2/
│       └── config.cfg
├── envs/
│   ├── local/
│   │   ├── docker-compose.override.yml
│   │   └── .env # le fichier doit finir par .env
│   ├── prod/
│   │   └── ... same
│   └── test/
│       └── ... same
├── .env
├── .gitignore
└── docker-compose.yml
```

```
$ cat .gitignore:
/envs/*/.configs.env
```

## Build

```
make
```

You can clean with:

```
make clean-build clean-venv
```
or
```
make clean
```

## Test

```
make tests
```

## Install

```
make install
```

## Release

1. Freeze requirements
1. test, tag and push
   ```
   make clean build tests
   git tag ...
   git push && git push --tags
   ```

## Execute locally

```
PYTHONPATH=~/Code/stackzou python3 ~/Code/stackzou/stackzou/cli.py -l
```
