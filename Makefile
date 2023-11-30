setup:
	[ -d venv ] || python3 -m venv venv && \
	. ./venv/bin/activate && \
	pip install pyinstaller && \
	pip install -r test_requirements.txt && \
	pip install -r requirements.txt

build:
	. ./venv/bin/activate && \
	pyinstaller \
		--onefile \
		--name=swarm-app \
		--hidden-import invoke \
		--hidden-import slugify \
		swarm_app/cli.py

clean:
	/bin/rm -rf ./build ./dist

clean-all: clean
	/bin/rm -rf venv

install:
	install ./dist/swarm-app ~/.local/bin

test: test-black test-lint test-e2e

test-black:
	. ./venv/bin/activate && \
	black --check --diff swarm_app

test-lint:
	. ./venv/bin/activate && \
	pylint swarm_app

test-e2e:
	. ./venv/bin/activate && \
	./dist/swarm-app -l
