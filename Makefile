SOURCEDIR = stackzou
requirements := venv/.requirements.txt
test_requirements := venv/.test_requirements.txt
SOURCEFILES := $(shell find $(SOURCEDIR) -name '*.py')
ACTIVATE = . ./venv/bin/activate

# default target
# alias
build: dist/stackzou

venv:
	python3 -m venv venv

dist/stackzou: venv $(SOURCEFILES) $(requirements)
	$(ACTIVATE) && \
	pyinstaller \
		--onefile \
		--name=stackzou \
		--hidden-import invoke \
		--hidden-import slugify \
		stackzou/cli.py && \
	touch dist/stackzou

# alias
.PHONY: requirements
requirements: $(requirements)

$(requirements): requirements.txt venv
	$(ACTIVATE) && \
	pip install -r requirements.txt && \
	touch $(requirements)

# alias
.PHONY: test_requirements
test_requirements: $(test_requirements)

$(test_requirements): test_requirements.txt $(requirements)
	$(ACTIVATE) && \
	pip install -r test_requirements.txt && \
	touch $(test_requirements)

install:
	install ./dist/stackzou ~/.local/bin

tests: test-black test-pylint test-build test-unit

test-black: test_requirements
	$(ACTIVATE) && \
	black --check --diff $(SOURCEDIR) tests

test-pylint: test_requirements
	$(ACTIVATE) && \
	pylint $(SOURCEDIR) tests

test-build: test_requirements build
	./dist/stackzou --version
	./dist/stackzou -l
	cd examples && ../dist/stackzou env simple compose.show
	cd examples && ../dist/stackzou env simple deploy
	cd examples && ../dist/stackzou env simple stack.ps
	cd examples && ../dist/stackzou env simple stack.ps --format=lines
	cd examples && ../dist/stackzou env simple stack.ps --format=clines
	cd examples && ../dist/stackzou env simple stack.ps --format=cclines
	sleep 5
	cd examples && ../dist/stackzou env simple stack.ps --format=cclines
	sleep 5
	cd examples && ../dist/stackzou env simple stack.rm

test-unit: test_requirements
	git clean -fdx examples
	$(ACTIVATE) && \
	PYTHONDONTWRITEBYTECODE=1 coverage run -m pytest -v && \
	coverage report

test-coverage: test_requirements
	$(ACTIVATE) && \
	coverage report

test-coverage-html: test_requirements
	$(ACTIVATE) && \
	coverage html
	xdg-open htmlcov/index.html

clean-build:
	/bin/rm -rf ./build ./dist

clean-venv:
	/bin/rm -rf ./venv

clean-tests:
	/bin/rm -f ./examples/envs/simple/.stackzou.env

clean: clean-build clean-venv clean-tests
