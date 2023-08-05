import argparse
import dsp_ingest.validate_args.validate as validate


class Arguments:
    def __init__(self):
        # create the parser for consuming arguments.
        input_parser = argparse.ArgumentParser(prog="dsp_ingest",
                                               usage="%(prog)s [options] dsp_install_dir",
                                               description="Ingesting logs into DSP with python multi-processing.",
                                               prefix_chars='-',
                                               epilog="The package takes care of purging the generated scloud.* files automatically.")
        # add the arguments
        input_parser.add_argument('--dsp_install_dir',
                                  action='store',
                                  type=str,
                                  required=True,
                                  help="Specify the directory at which DSP is installed.")
        input_parser.add_argument('--dsp_host',
                                  action='store',
                                  type=str,
                                  required=False,
                                  default="DSP-POC",
                                  help="Specify the default DSP host name.")
        input_parser.add_argument('--dsp_source',
                                  action='store',
                                  type=str,
                                  required=False,
                                  default="dsp_ingest",
                                  help="Specify the default DSP source.")
        input_parser.add_argument('--dsp_sourcetype',
                                  action='store',
                                  type=str,
                                  required=False,
                                  default="dsp_logs",
                                  help="Specify the default DSP sourcetype.")
        input_parser.add_argument('--log_dir',
                                  action='store',
                                  type=str,
                                  required=True,
                                  help="Specify the directory at which DSP Scloud ingest logs and sample logs must be stored.")
        input_parser.add_argument('--purge_frequency_in_secs',
                                  action='store',
                                  type=int,
                                  default=3,
                                  required=False,
                                  help="How frequently should the scloud*INFO logfiles be purged."
                                   )
        # parse the arguments
        self.args = input_parser.parse_args()
        self.args_dict = vars(self.args)
        # check if the DSP installation/scould binary directory exists
        validate.dir_exists(self.args.dsp_install_dir)
        validate.dir_exists(self.args.log_dir)
        validate.check_for_scloud(self.args.dsp_install_dir)
    
    def __iter__(self):
        for key,value in self.args_dict.items():
            yield (key, value)