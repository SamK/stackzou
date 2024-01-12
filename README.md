## Usage

```
stackzou -e env local configs.create stack.deploy
```

## Project structure

Ton projet de ressemble à un truc comme ça:

```
./
├── configs/
│   ├── service1/
│   │   └── index.html
│   └── service2/
│       └── index.html
├── envs/
│   ├── local/
│   │   ├── docker-compose.override.yml
│   │   └── .env # le fichier doit finir par .env
│   ├── prod/
│   │   └── ... pareil
│   └── test/
│       └── ... pareil
├── .env
└── docker-compose.yml
```

## Clean

```
make clean-build clean-venv
# or
make clean
```

## Build

```
make
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

```
make clean build tests
git tag ...
git push && git push --tags
make install
```

## Execute locally

```
PYTHONPATH=~/Code/stackzou python3 ~/Code/stackzou/stackzou/cli.py -l
```
