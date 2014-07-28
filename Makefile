.PHONY: clean env/bin/activate stats

export PYTHONPATH=$PYTHONPATH:./

PWD=`pwd`
ENV = env
PIP = $(PWD)/env/bin/pip
PYTHON = exec $(PWD)/env/bin/python
JENKINS_NOSE_ARGS = --with-xunit

test:
	env/bin/nosetests tests/
 
test-jenkins:
	env/bin/nosetests tests/ $(JENKINS_NOSE_ARGS)

clean:
	find src/ -type f -name "*.pyc" -exec rm {} \;


test-client: env
	env/bin/python example/search/search_client.py 

test-server: env
	env/bin/python example/search/search_server.py 

env: env/bin/activate
env/bin/activate: requirements.txt
	test -d env || virtualenv --no-site-packages env
	ln -fs env/bin .
	. env/bin/activate; pip install -r requirements.txt 
	touch env/bin/activate
