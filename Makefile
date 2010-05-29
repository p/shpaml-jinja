SOURCES=src/aml.py src/filter.py src/runtime.py src/shpaml.py src/whitespace_removal.py

PYTHON=python

all: build/shpaml_jinja.py build/shpaml_erb.py

build/shpaml_jinja.py: $(SOURCES) src/shpaml_jinja.py tools/build_aml.py
	$(PYTHON) tools/build_aml.py -o $(.TARGET) -m shpaml_jinja $(SOURCES) src/shpaml_jinja.py

build/shpaml_erb.py: $(SOURCES) src/shpaml_erb.py tools/build_aml.py
	$(PYTHON) tools/build_aml.py -o $(.TARGET) -m shpaml_erb $(SOURCES) src/shpaml_erb.py

build/aml_cat.py: $(SOURCES)
	cat $(SOURCES) >$(.TARGET)

test: build/aml.py build/aml_cat.py

clean:
	rm -f build/*.py

.PHONY: clean
