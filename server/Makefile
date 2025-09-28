# Makefile - builds Python utils directly with PyInstaller
VENV_DIR := .venv
PYINSTALLER := $(VENV_DIR)/bin/pyinstaller
PY := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

UTILS_DIR := utils
DIST_DIR := dist
LOCAL_BIN := $(HOME)/.local/bin

.PHONY: all deps utest texmat clean install test

all: utest texmat

deps:
	@echo "Installing build deps into $(VENV_DIR) (if not already)..."
	@test -x $(PIP) || (echo "pip not found in $(VENV_DIR). Create venv first."; exit 1)
	$(PIP) install --upgrade pip
	$(PIP) install pyinstaller dill numpy sympy fire

# Build targets
utest: deps
	@echo "Building utest..."
	$(PYINSTALLER) --clean --onefile --name utest \
		--hidden-import=sympy --hidden-import=sympy.parsing \
		--hidden-import=numpy --hidden-import=dill \
		$(UTILS_DIR)/utest.py
	@echo "Built: $(DIST_DIR)/utest"

texmat: deps
	@echo "Building texmat..."
	$(PYINSTALLER) --clean --onefile --name texmat \
		--hidden-import=sympy --hidden-import=sympy.parsing \
		--hidden-import=numpy --hidden-import=dill \
		$(UTILS_DIR)/texmat.py
	@echo "Built: $(DIST_DIR)/texmat"

install: all
	@echo "Installing binaries to $(LOCAL_BIN)"
	mkdir -p $(LOCAL_BIN)
	cp -v $(DIST_DIR)/utest $(LOCAL_BIN)/utest
	chmod +x $(LOCAL_BIN)/utest
	cp -v $(DIST_DIR)/texmat $(LOCAL_BIN)/texmat
	chmod +x $(LOCAL_BIN)/texmat

test:
	@if [ -x $(DIST_DIR)/utest ]; then \
		echo "Running binary test..."; \
		$(DIST_DIR)/utest ./space/sample.dill ./space/user.dill -n 5 || true; \
	else \
		echo "Binary not found, running script directly"; \
		$(PY) $(UTILS_DIR)/utest.py ./space/sample.dill ./space/user.dill -n 5 || true; \
	fi

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ $(DIST_DIR)/ __pycache__/
