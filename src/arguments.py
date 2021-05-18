import argparse
from pathlib import Path


class ArgumentLoader(object):
    def parse_args(self):
        args = self.get_parser().parse_args()
        return args

    def get_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--input_data',
                            required=True,
                            type=Path,
                            default=None)
        parser.add_argument('--output_data_path_prefix',
                            type=Path,
                            default='outputs/')
        parser.add_argument('--output_data_filename_prefix',
                            type=Path,
                            default=None)
        parser.add_argument('--external_dic_path', type=Path, default=None)
        parser.add_argument('--case_sensitive', action='store_true')
        parser.add_argument('--chunk_freq_threshold', type=int, default=1)
        parser.add_argument('--save_dic', action='store_true')
        parser.add_argument('--gen_lattice', action='store_true')
        parser.add_argument('--unuse_single_token', action='store_true')

        return parser
