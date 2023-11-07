build:
	. ~/.virtualenvs/swarm-app/bin/activate && \
	pyinstaller \
		--onefile \
		--name=swarm-app \
		--hidden-import invoke \
		--hidden-import slugify \
		swarm_app/cli.py

clean:
	/bin/rm -rf ./build ./dist


install:
	install ./dist/swarm-app ~/.local/bin
