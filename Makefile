# Makefile: helper tasks
.PHONY: sync-static

sync-static:
	python3 scripts/sync_static.py
