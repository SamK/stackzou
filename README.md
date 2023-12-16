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

## Build

```
make clean-all venv
make build
```

## Install

```
make install
```

## Test

```
make test
```

## Standard

```
make clean build install
```

## Execute locally

```
PYTHONPATH=~/Code/stackzou python3 ~/Code/stackzou/stackzou/cli.py -l
```
