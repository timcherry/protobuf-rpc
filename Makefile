.PHONY: clean env/bin/activate stats

test: env
	. env/bin/activate;
	nosetests $(NOSEARGS);

run: env
	env/bin/python src/run.py

clean:
	find src/ -type f -name "*.pyc" -exec rm {} \;

env: env/bin/activate
env/bin/activate: requirements.txt
	test -d env || virtualenv --no-site-packages env
	ln -fs env/bin .
	. env/bin/activate; pip install -r requirements.txt 
	touch env/bin/activate
