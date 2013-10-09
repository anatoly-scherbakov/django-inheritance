#!/usr/bin/env python
import os
import sys

this_file   = os.path.abspath(__file__)
project_dir = os.path.dirname(this_file)
base_dir    = os.path.dirname(project_dir)

sys.path.append(base_dir)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sampleproject.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
