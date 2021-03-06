#!usr/bin/env python3
#
# Author(s):    Roman Rivera (Invisible Institute)

'''export script for roster__2018-03_p441436'''

import pandas as pd
import __main__

import setup


def get_setup():
    ''' encapsulates args.
        calls setup.do_setup() which returns constants and logger
        constants contains args and a few often-useful bits in it
        including constants.write_yamlvar()
        logger is used to write logging messages
    '''
    script_path = __main__.__file__
    args = {
        'input_file': 'input/roster__2018-03.csv.gz',
        'input_profiles_file': 'input/roster__2018-03_profiles.csv.gz',
        'output_file': 'output/roster__2018-03.csv.gz',
        'output_profiles_file': 'output/roster__2018-03_profiles.csv.gz',
        }

    assert (args['input_file'].startswith('input/') and
            args['input_file'].endswith('.csv.gz')),\
        "input_file is malformed: {}".format(args['input_file'])
    assert (args['output_file'].startswith('output/') and
            args['output_file'].endswith('.csv.gz')),\
        "output_file is malformed: {}".format(args['output_file'])

    return setup.do_setup(script_path, args)


cons, log = get_setup()

df = pd.read_csv(cons.input_file)
sworn = df[df['is_sworn_officer'] == 'Y']['roster__2018-03_ID']
log.info("adding merge column if individual is sworn officer for %d officers", sworn.nunique())
df.to_csv(cons.output_file, **cons.csv_opts)

profiles_df = pd.read_csv(cons.input_profiles_file)
profiles_df['merge'] = profiles_df['roster__2018-03_ID'].isin(sworn)
profiles_df.to_csv(cons.output_profiles_file, **cons.csv_opts)
