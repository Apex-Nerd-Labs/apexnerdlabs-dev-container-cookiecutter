import re
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.project_slug }}"

module_name = re.sub(r"-", "_", module_name)
module_name = re.sub(r"[^_a-zA-Z0-9]", "", module_name)

if not re.match(MODULE_REGEX, module_name):
    print(
        "ERROR: The project slug must contain only letters, numbers, and underscores."
    )
    sys.exit(1)
