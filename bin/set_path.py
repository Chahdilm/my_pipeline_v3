import os 
current_dir = os.getcwd()
print(current_dir)
path_act = "/home/maroua/Bureau/wip/my_pipeline_v2/"
os.chdir(path_act)
# Optional: check that it worked
print("Current directory is now:", os.getcwd())

from bin.path_variable import *
