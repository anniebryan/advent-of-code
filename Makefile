# Extract positional arguments:
YEAR := $(word 2, $(MAKECMDGOALS))
DAY  := $(word 3, $(MAKECMDGOALS))

# Prevent make from treating YEAR/DAY as targets
$(YEAR) $(DAY):
	@:

# ---- Targets ----

create:
	@echo "Creating AOC day $(DAY) for $(YEAR)"
	python3 scripts/create_day.py $(YEAR) $(DAY)

run:
	@echo "Running solution for AOC $(YEAR) Day $(DAY)"
	python3 scripts/run.py $(YEAR) $(DAY)
