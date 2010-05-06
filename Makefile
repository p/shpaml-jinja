SOURCES=src/aml.py src/filter.py src/runtime.py src/shpaml.py

PYTHON=python

build/aml.py: $(SOURCES) tools/build-aml.py
	$(PYTHON) tools/build-aml.py $(SOURCES) $(.TARGET)

build/aml-cat.py: $(SOURCES)
	cat $(SOURCES) >$(.TARGET)

test: build/aml.py build/aml-cat.py

clean:
	rm -f build/*.py

.PHONY: clean
