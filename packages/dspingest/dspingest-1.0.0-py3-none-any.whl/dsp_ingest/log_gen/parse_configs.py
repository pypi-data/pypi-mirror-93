import yaml
import os

def get_logfiles(config_dir):
    logfiles=[]
    all_yamls = [os.path.join(config_dir, f) for f in os.listdir(config_dir)]
    for config_yaml in all_yamls:
        with open(config_yaml) as f:
           data = yaml.load(f, Loader=yaml.FullLoader)
           logfiles.append(data['file'])
    return logfiles