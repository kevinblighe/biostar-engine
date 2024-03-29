set -ueo pipefail

# Get parameters.
INPUT_DATA={{sequence.value}}
ACCESSION_LIST={{accessions.value}}
FISH_DB={{runtime.local_root}}/blastdb/fish_species/fish_species
TAXONOMY_DIR={{runtime.local_root}}/taxonomy
RESULT_VIEW={{settings.index}}

# Internal parameters.
REF_DIR=ref
REF_SEQ=reference.fa
INDEX=reference
TAXA_MAP=acc2taxa.txt
RESULT_DIR=results

# Check if $FISH_DB exist.
if [ ! -f "$FISH_DB.nhr" ]; then
echo "Blast database of all fish species should be present. $FISH_DB does not exist."
fi

# Create reference sequence file.
mkdir -p $REF_DIR
blastdbcmd -entry 'all' -db ${FISH_DB} -outfmt '%f' >${REF_DIR}/$REF_SEQ

# Create accession-taxid map.
blastdbcmd -entry 'all' -db ${FISH_DB} -outfmt '%a,%T' |tr ',' '\t'  >${REF_DIR}/$TAXA_MAP

# Build centrifuge index.
cd $REF_DIR

centrifuge-build -p 4 --conversion-table $TAXA_MAP --taxonomy-tree $TAXONOMY_DIR/nodes.dmp --name-table $TAXONOMY_DIR/names.dmp $REF_SEQ $INDEX >/dev/null
cd ..

# Run classification using centrifuge.
mkdir -p $RESULT_DIR
echo -e "Classifying sequences and assigning taxonomic labels.\n"
centrifuge -x ${REF_DIR}/$INDEX -U $INPUT_DATA --report-file ${RESULT_DIR}/report.txt -S ${RESULT_DIR}/classification.txt

# Plot results.
python -m biostar.tools.classify.plotter ${RESULT_DIR}/report.txt >${RESULT_VIEW}

