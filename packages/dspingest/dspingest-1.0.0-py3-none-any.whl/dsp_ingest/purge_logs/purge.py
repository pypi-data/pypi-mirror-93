import os
import time

def purge_scloud_logs(log_dir, purge_frequency_in_secs):
    print("purging temp files")
    while True:
        time.sleep(purge_frequency_in_secs)
        cmd="sudo rm -rf "+os.path.join(log_dir,"scloud*INFO*")
        os.system(cmd)
        print("purged files, will wait for next iteration")