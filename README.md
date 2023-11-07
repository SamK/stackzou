

## Build

```
pip install -r build_requirements.txt
pip install -r requirements.txt
export PYTHONDONTWRITEBYTECODE=1
pyinstaller --onefile --name=swarm-app  --hidden-import=invoke swarm_app/cli.py
```

## Install

```
install ./dist/swarm-app ~/.local/bin
```

## Test

```
pip install pylint
pylint swarm_app
```

## Execute locally

```
PYTHONPATH=~/Code/swarm_app python3 ~/Code/swarm_app/swarm_app/cli.py  -l
```
