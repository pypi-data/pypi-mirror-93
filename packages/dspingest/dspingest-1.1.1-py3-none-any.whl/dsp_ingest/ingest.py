import os
import dsp_ingest
from dsp_ingest.get_args.cli import Arguments as get_arguments
from dsp_ingest.purge_logs.purge import purge_scloud_logs as purge
from multiprocessing import Process
from dsp_ingest.follow_logs.post_events import ingest_into_dsp
from dsp_ingest.log_gen.parse_configs import get_logfiles


dsp_log_mon_processes = []


class DspIngest:
    def __init__(self):
        args = get_arguments()
        self.args_dict = dict(args)

    def process_target_func(self, log_file_handle):
        ingest_into_dsp(log_file_handle,
                        self.args_dict['dsp_install_dir'],
                        self.args_dict['dsp_host'],
                        self.args_dict['dsp_source'],
                        self.args_dict['dsp_sourcetype'],
                        self.args_dict['log_dir']
                        )

    def call_for_dspingest(self):
        config_dir=self.args_dict['config_dir']
        logs=get_logfiles(config_dir)
        # iterate through the config.yamls meant for log-generator and get the logfiles.
        for log in logs:
            log_file_handle=open(log)
            process = Process(target=self.process_target_func(log_file_handle))
            dsp_log_mon_processes.append(process)
            process.start()
        # start the process so that it can stream the logfile individually.
        purge_process = Process(target=purge(self.args_dict['log_dir'],self.args_dict['purge_frequency_in_secs']))
        dsp_log_mon_processes.append(purge_process)
        purge_process.start()
        # house-keeping for the processes.
        for process in dsp_log_mon_processes:
          process.join()