SCRIPT = BierAmpel.py
BINARY_NAME = BierAmpel
PYTHON = /bin/python3
PIP = /bin/pip
BIN_DIR = /opt
SYSD_DIR = /etc/systemd/system
SYSD_FILE = BierAmpel.service

.PHONY: all init build_pyinstaller build_nuitka clean

all: init build_pyinstaller

init:
	$(PIP) install --upgrade pip
	$(PIP) install pyinstaller nuitka
	$(PIP) install -r requirements.txt

build_pyinstaller: init
	pyinstaller --onefile --name $(BINARY_NAME) $(SCRIPT)
	@echo "Binärdatei erstellt in: dist/$(BINARY_NAME)"
	$(MAKE) clean

build_nuitka: init
	nuitka --standalone --onefile --output-filename=dist/$(BINARY_NAME) $(SCRIPT)
	@echo "Binärdatei mit Nuitka erstellt."
	$(MAKE) clean

setup:
	cp dist/${BINARY_NAME} ${BIN_DIR}/
	chmod +x ${BIN_DIR}/${BINARY_NAME}
	cp ${SYSD_FILE} ${SYSD_DIR}/
	systemctl daemon-reload

clean:
	rm -rf venv/ *.build/ *.dist/ build/ *.spec $(BINARY_NAME)
