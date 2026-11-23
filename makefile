all:
	@clear
	@uv run python3 pac-man.py config.json
	@$(MAKE) clean
# 	clear

clean:
	@rm -rf src/__pycache* src/*/__pycache*

