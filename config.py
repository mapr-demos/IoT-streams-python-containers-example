"""
config.py

for global variable declarations across other modules
"""
#
# initialized to 10 because we will init the graph data
# by consuming the first 10 sensor events off each sensor's
# dedicated topic.
#
master_offset = 10