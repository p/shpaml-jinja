SOURCES=src/aml.py src/filter.py src/runtime.py src/shpaml.py

PYTHON=python

build/aml.py: $(SOURCES) tools/build_aml.py
	$(PYTHON) tools/build_aml.py $(SOURCES) $(.TARGET)

build/aml_cat.py: $(SOURCES)
	cat $(SOURCES) >$(.TARGET)

test: build/aml.py build/aml_cat.py

clean:
	rm -f build/*.py

.PHONY: clean
