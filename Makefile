SOURCES=src/aml.py src/filter.py src/runtime.py src/shpaml.py src/whitespace_removal.py

PYTHON=python

all: build/aml_jinja.py build/aml_erb.py

build/aml_jinja.py: $(SOURCES) src/aml_jinja.py tools/build_aml.py
	$(PYTHON) tools/build_aml.py -o $(.TARGET) -m aml_jinja $(SOURCES) src/aml_jinja.py

build/aml_erb.py: $(SOURCES) src/aml_erb.py tools/build_aml.py
	$(PYTHON) tools/build_aml.py -o $(.TARGET) -m aml_erb $(SOURCES) src/aml_erb.py

build/aml_cat.py: $(SOURCES)
	cat $(SOURCES) >$(.TARGET)

test: build/aml.py build/aml_cat.py

clean:
	rm -f build/*.py

.PHONY: clean
