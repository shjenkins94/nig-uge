import sys

""" qsub_status.py evaluates cpu_hung_min_time as an int and divides by it.
Make sure that cpu_hung_min_time isn't less than zero."""
if {{cookiecutter.cpu_hung_min_time}} < 1:
    print('ERROR: cpu_hung_min_time must be at least 1')
    # exits with status 1 to indicate failure
    sys.exit(1)
