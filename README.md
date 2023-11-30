## Usage

```
swarm-app -e env local configs.create stack.deploy
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
│   │   ├── docker-compose.override.yml  # pas obligatoire
│   │   ├── docker-compose.yml -> ../../docker-compose.base.yml
│   │   └── env.env
│   ├── prod/
│   │   └── ... pareil
│   └── test/
│       └── ... pareil
├── README
├── env
└── docker-compose.base.yml
```

## Build

```
make clean-all setup
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

## Execute locally

```
PYTHONPATH=~/Code/swarm-app python3 ~/Code/swarm-app/swarm_app/cli.py -l
```
