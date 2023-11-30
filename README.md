## Usage

```
swarm-app -e configs.create -e local stack.deploy -e local
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
│   │   └── env
│   ├── prod/
│   │   └── env
│   └── test/
│       └── env
├── README
├── env
└── docker-compose.yml
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
