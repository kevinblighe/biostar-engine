set -ueo pipefail

# Get parameters.
INPUT={{sequence.value}}
GENOME={{genome.value}}
LEN_FILTER={{align_length.value}}

INDEX=${GENOME}
INDEX_DIR=$(dirname ${GENOME})/bwa

mkdir -p ${INDEX_DIR}
INDEX=${INDEX_DIR}/{{genome.uid}}

# Internal parameters.
WORK={{runtime.work_dir}}/work
mkdir -p ${WORK}

# Main results.
RESULT_VIEW={{runtime.work_dir}}/{{settings.index}}
OUTPUT=${WORK}/aligned.bam

# Build bwa index if not exist.

if [ ! -f "$INDEX.bwt" ]; then
echo "Building bwa index."
bwa index -p ${INDEX} ${GENOME}
fi

# Align sequences

echo  "Mapping reads to the genome."
bwa mem -t 4 ${INDEX} ${INPUT}  | samtools view -b |samtools sort >${OUTPUT}
samtools index ${OUTPUT}

echo "Computing statistics."
echo "--------------------"
samtools flagstat ${OUTPUT}
echo "--------------------"

# Get samtools flagstats results.
samtools flagstat ${OUTPUT} >${WORK}/alignment_stats.txt

# Get number of reads mapped to each chromosome.
samtools idxstats ${OUTPUT} >${WORK}/chrom_mapping.txt

echo "Applying filters to alignments and generating statistics."

# Get classification table after applying filters.
python -m biostar.tools.lamar_align.parse_align ${OUTPUT} ${LEN_FILTER}  >${WORK}/classification_table.txt

echo "Generating plots."

# Plot results.

python -m biostar.tools.lamar_align.plotter ${WORK}/alignment_stats.txt \
${WORK}/chrom_mapping.txt ${WORK}/classification_table.txt>${RESULT_VIEW}



