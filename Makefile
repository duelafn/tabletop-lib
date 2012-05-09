
VERSION_FROM=ttlib

.PHONY: test increment_bugfix increment_minor increment_major dist

test:
	python t/hexmap.t

increment_bugfix:
	perl -pi -E 's/^__version__\s*=\s*"\d+\.\d+\.\K(\d+)(?:\-dev)?(".*)/($$1+1) . $$2/e' ${VERSION_FROM}/__init__.py

increment_minor:
	perl -pi -E 's/^__version__\s*=\s*"\d+\.\K(\d+)\.\d+(?:\-dev)?(".*)/($$1+1) . ".0$$2"/e' ${VERSION_FROM}/__init__.py

increment_major:
	perl -pi -E 's/^__version__\s*=\s*"\K(\d+)\.\d+\.\d+(?:\-dev)?(".*)/($$1+1) . ".0.0$$2"/e' ${VERSION_FROM}/__init__.py

dist:
	@echo -n "Comparing ChangeLog and ${VERSION_FROM}/__init__.py versions... "
	@perl -E 'local $$/;($$CH,$$TT)=<>; $$vch=$$1 if $$CH=~/^v([\d.]+)/m; $$vtt=$$1 if $$TT=~/^__version__\s*\=\s*"([\d.]+)"/m; die "ChangeLog version ($$vch) does not match ${VERSION_FROM} version ($$vtt)" unless $$vch and $$vch eq $$vtt' ChangeLog ${VERSION_FROM}/__init__.py
	@echo "[ok]"
	python setup.py sdist
