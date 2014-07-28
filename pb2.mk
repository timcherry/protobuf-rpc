PROTO_SRC=./
PY_SRC=./

PROTO_SOURCES=$(shell find $(PROTO_SRC) -name '*.proto')
PROTO_PY = $(patsubst $(PROTO_SRC)/%.proto, $(PY_SRC)/%_pb2.py, $(PROTO_SOURCES))
PROTO_JAVA = $(patsubst $(PROTO_SRC)/%.proto, $(JAVA_SRC)/com/livefyre/%.java, $(PROTO_SOURCES))
PROTO_PY_SRC = $(patsubst $(PROTO_SRC)/%.proto, $(PY_SRC)/%.proto, $(PROTO_SOURCES))
PROTO_NODE = $(patsubst $(PROTO_SRC)/%.proto, $(NODE_SRC)/%.proto, $(PROTO_SOURCES))

pb2_compile: pb2_compile_python
	@echo "Compile... done!"

pb2_compile_python: $(PROTO_PY) $(PROTO_PY_SRC)

$(PY_SRC)/%_pb2.py: $(PROTO_SRC)/%.proto
	mkdir -p $(PY_SRC)
	protoc --proto_path=/usr/include/ --proto_path=env/lib/python2.7/site-packages/ --python_out=$(PY_SRC) -I$(PROTO_SRC)  $<
	touch "$(dir $@)/__init__.py"
	perl -i -pe 'print "\# \@PydevCodeAnalysisIgnore\n" if $$. == 1;s/^( *)(class [a-zA-Z0-9_]+\(_?message\.Message\):)/$$1$$2\n$$1  """\@DynamicAttrs"""/g' $@

$(PY_SRC)/%.proto: $(PROTO_SRC)/%.proto
	cp $< $@
