=======================
Level package structure
=======================

Attention. This docs are just the idea of how it should work. They are not up 
to date with the code right now.

After developing a new level, levels packaging should be made by calling to 
`manage.py build-level {level_name} {output_file}`.

This will create a file with `.lvl` extension that will be in fact a compressed
file with the following structure:

- manifest.json
- frontend/
- backend/
