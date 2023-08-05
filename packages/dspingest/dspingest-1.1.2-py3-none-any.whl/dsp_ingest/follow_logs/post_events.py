import os
import time

def follow_tail(logfile_handle):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    logfile_handle.seek(0, os.SEEK_END)
    # start infinite loop
    while True:
        # read last line of file
        line = logfile_handle.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue
        yield line


def ingest_into_dsp(logfile_handle, 
                    dsp_install_dir,
                    dsp_host,
                    dsp_source,
                    dsp_sourcetype,
                    log_dir):
    scloud_bin=os.path.join(dsp_install_dir,"scloud")
    dsp_ingest_cmd=scloud_bin+" ingest post-events --log_dir "+log_dir+" --host "+dsp_host+" --source "+dsp_source+" --sourcetype "+dsp_sourcetype
    lines = follow_tail(logfile_handle)
    # iterate over the generator
    for line in lines:
        cmd = "echo  " + '"' + line + '"' + ' | ' + dsp_ingest_cmd
        os.system(cmd)