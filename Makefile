SOURCES=src/aml.py src/filter.py src/runtime.py src/shpaml.py src/whitespace_removal.py

PYTHON=python

build/shpaml_jinja.py: $(SOURCES) src/shpaml_jinja.py tools/build_aml.py
	$(PYTHON) tools/build_aml.py -o $(.TARGET) -m shpaml_jinja $(SOURCES) src/shpaml_jinja.py

build/aml_cat.py: $(SOURCES)
	cat $(SOURCES) >$(.TARGET)

test: build/aml.py build/aml_cat.py

clean:
	rm -f build/*.py

.PHONY: clean
