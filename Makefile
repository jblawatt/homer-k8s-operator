#!/usr/bin/env make


VENV_ROOT=venv

PIP=$(VENV_ROOT)/bin/pip
PIP_SYNC=$(VENV_ROOT)/bin/pip-sync
PIP_COMPILE=$(VENV_ROOT)/bin/pip-compile

REQUREMENTS_TXT=requirements.txt


.PHONY: clean
.DEFAULT_GOAL := help

hello:
	@echo "hello world {1..10}"

help:
	@echo "this is the help"

# ---------------------------------------------------

$(VENV_ROOT): $(REQUREMENTS_TXT)
	python3 -m venv $(VENV_ROOT)
	$(PIP) install pip-tools
	$(MAKE) pip-sync


$(REQUREMENTS_TXT):
	touch $(REQUREMENTS_TXT)


pip-compile: $(VENV_ROOT) $(REQUREMENTS_TXT)
	$(PIP_COMPILE)


pip-sync:
	$(PIP_SYNC)


pip-update:
	$(PIP_COMPILE)
	$(PIP_SYNC)


# ---------------------------------------------------

serve:
	$(VENV_ROOT)/bin/kopf run src/operator.py


shell:
	$(VENV_ROOT)/bin/ipython


ingress:
	@kubectl delete ingress test-ingress
	@kubectl apply -f manifests/tests/ingress.yaml


# ---------------------------------------------------

clean:
	rm -rf $(VENV_ROOT)

