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

tests: test_requirements build test-black test-lint test-e2e

test-black:
	$(ACTIVATE) && \
	black --check --diff $(SOURCEDIR)

test-lint:
	$(ACTIVATE) && \
	pylint $(SOURCEDIR) --max-line-length=120 --max-attributes=99 --disable=missing-function-docstring

test-e2e:
	$(ACTIVATE) && \
	./dist/stackzou -l

clean-build:
	/bin/rm -rf ./build ./dist

clean-venv:
	/bin/rm -rf ./venv

clean: clean-build clean-venv
