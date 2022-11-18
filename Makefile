.PHONY = build

build:
	python3 configure.py --create-user-config
	docker run --rm -v $OPENLANE_ROOT:/openlane -v $(PDK_ROOT):$(PDK_ROOT) -v $(PWD):/work -e PDK_ROOT=$(PDK_ROOT) -u $(id -u $(USER)):$(id -g $(USER)) $(OPENLANE_IMAGE_NAME) /bin/bash -c "./flow.tcl -verbose 2 -overwrite -design /work/src -run_path /work/runs -tag wokwi"
	cp runs/wokwi/results/final/verilog/gl/tt2_tholin_diceroll.v src

pdk:
	if not [ -d "caravel_user_project" ]; then git clone "https://github.com/efabless/caravel_user_project.git" -b "mpw-7a"; fi
	cd caravel_user_project && make setup

tests:
	cd src && make clean && make

gltests:
	cd src && make clean && GATES=yes make

clean:
	rm -rf runs
	rm -f src/tt2_tholin_diceroll.v

distclean:
	rm -rf runs pdk openlane caravel_user_project
