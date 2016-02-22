T2T := $(wildcard src/*.t2t)
HTML= $(T2T:.t2t=.html)

t2t: $(HTML)

generate: $(HTML)
	python3 scripts/generate.py

serve: generate
	cd www; python3 -m http.server

%.html : %.t2t inc/settings.t2t
	txt2tags -C inc/settings.t2t -H -i "$<" -o "$@" 


