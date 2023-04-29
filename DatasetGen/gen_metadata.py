import os

from const import DATASET, INDEX_FILEPATH

## Fields to modify
METADATA_FILE = "./sample_metadata/quant_metadata.jsonl"
INDEX_FILEPATH = "./data/"
DATASET = "quantifier"

if not os.path.exists(INDEX_FILEPATH):
    os.mkdir(INDEX_FILEPATH)
    os.mkdir(INDEX_FILEPATH + "images/")
    os.mkdir(INDEX_FILEPATH + "features/")

if DATASET == "spatial":
    from SpatialDatasetGen.SpatialMetadataGen import SpatialMetadataGen
    SpatialMetadataGen(metadata_file=METADATA_FILE).gen_dataset()
elif DATASET == "quantifier":
    from QuantifierDatasetGen.QuantifierMetadataGen import QuantifierMetadataGen
    QuantifierMetadataGen(metadata_file=METADATA_FILE).gen_dataset()
elif DATASET == "cardinality":
    from CardinalityDatasetGen.CardinalityMetadataGen import CardinalityMetadataGen
    CardinalityMetadataGen(metadata_file=METADATA_FILE).gen_dataset()
elif DATASET == "compare":
    from CompareDatasetGen.CompareMetadataGen import CompareMetadataGen
    CompareMetadataGen(metadata_file=METADATA_FILE).gen_dataset()