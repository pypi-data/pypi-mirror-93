import os
import sys

def dir_exists(directory):
    if not os.path.isdir(directory):
        print("The directory "+ directory +" specified does not exist")
        sys.exit(1)
    else:
        return True

def check_for_scloud(directory):
    if not os.path.isfile(os.path.join(directory,"scloud")):
        print("The scloud binary doesn't exist with in the DSP installation directory.")
        sys.exit(2)
    else:
        return True