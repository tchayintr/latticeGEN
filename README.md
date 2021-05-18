# Dictionary-based Lattice Generator
#### _latticeGEN_

A Python script for generating dictionary-based lattices.
Utilizing Aho-Corasick algorithm to match substrings in raw text.


#### Requirement

- python3 >= 3.7.3
- ahocorapy >= 1.6.1
- networkx >= 2.5.1
- pathlib >= 1.0.1
- pickle


#### Usage (see scripts/sample_gen.sh for more details)
```
usage: gen.py [-h] --input_data INPUT_DATA
              [--output_data_path_prefix OUTPUT_DATA_PATH_PREFIX]
              [--output_data_filename_prefix OUTPUT_DATA_FILENAME_PREFIX]
              [--external_dic_path EXTERNAL_DIC_PATH] [--case_sensitive]
              [--chunk_freq_threshold CHUNK_FREQ_THRESHOLD] [--save_dic]
              [--gen_lattice] [--unuse_single_token]

optional arguments:
  -h, --help            show this help message and exit
  --input_data INPUT_DATA
  --output_data_path_prefix OUTPUT_DATA_PATH_PREFIX
  --output_data_filename_prefix OUTPUT_DATA_FILENAME_PREFIX
  --external_dic_path EXTERNAL_DIC_PATH
  --case_sensitive
  --chunk_freq_threshold CHUNK_FREQ_THRESHOLD
  --save_dic
  --gen_lattice
  --unuse_single_token
```
