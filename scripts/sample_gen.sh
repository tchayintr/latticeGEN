set -e
echo "A Python script for generating dictionary-based lattices"

INPUT_DATA=(
    data/samples/best2010_sample_20.seg.sl \
)

OUTPUT_PATH_PREFIX=(
    outputs/samples \
)

OUTPUT_FILE_PREFIX=(
    best2010.sample \
)

CHUNK_THRESHOLD=1

for ((i=0; i<${#INPUT_DATA[@]}; i++));
do
    echo "## Generate trie for ${INPUT_DATA[i]}"
    python3 src/gen.py \
        --input_data ${INPUT_DATA[i]} \
        --output_data_path_prefix ${OUTPUT_PATH_PREFIX[i]} \
        --output_data_filename_prefix ${OUTPUT_FILE_PREFIX[i]}\
        --chunk_freq_threshold $CHUNK_THRESHOLD \
        --save_dic \
        --gen_lattice
    echo
done
