venv:
	[ -d venv ] || python3 -m venv venv && \
	. ./venv/bin/activate && \
	pip install pyinstaller && \
	pip install -r test_requirements.txt && \
	pip install -r requirements.txt

build:
	. ./venv/bin/activate && \
	pyinstaller \
		--onefile \
		--name=stackzou \
		--hidden-import invoke \
		--hidden-import slugify \
		stackzou/cli.py

clean:
	/bin/rm -rf ./build ./dist

clean-all: clean
	/bin/rm -rf venv

install:
	install ./dist/stackzou ~/.local/bin

test: test-black test-lint test-e2e

test-black:
	. ./venv/bin/activate && \
	black --check --diff stackzou

test-lint:
	. ./venv/bin/activate && \
	pylint stackzou --max-line-length=120

test-e2e:
	. ./venv/bin/activate && \
	./dist/stackzou -l
