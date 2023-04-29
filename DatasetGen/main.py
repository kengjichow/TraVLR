from SpatialDatasetGen.SpatialValGen import SpatialExtraGen
import os
from const import NUM_CONDITIONS, INDEX_FILEPATH, DATASET

if not os.path.exists(INDEX_FILEPATH):
    os.mkdir(INDEX_FILEPATH)
    os.mkdir(INDEX_FILEPATH + "images/")
    os.mkdir(INDEX_FILEPATH + "features/")

if DATASET == "spatial":
    from SpatialDatasetGen.SpatialDatasetGen import SpatialDatasetGen
    generator = SpatialDatasetGen()
    generator.gen_conditions(NUM_CONDITIONS)
if DATASET == "quantifier":
    from QuantifierDatasetGen.QuantifierDatasetGen import QuantifierDatasetGen
    generator = QuantifierDatasetGen()
    generator.gen_conditions(NUM_CONDITIONS)
elif DATASET == "cardinality":
    from CardinalityDatasetGen.CardinalityDatasetGen import CardinalityDatasetGen
    generator = CardinalityDatasetGen()
    generator.gen_conditions(NUM_CONDITIONS)
elif DATASET == "compare":
    from CompareDatasetGen.CompareDatasetGen import CompareDatasetGen
    generator = CompareDatasetGen()
    generator.gen_conditions(NUM_CONDITIONS)
elif DATASET == "spatial_extra":
    from SpatialDatasetGen.SpatialDatasetGen import SpatialDatasetGen
    generator = SpatialExtraGen()
    generator.gen_dataset("test_Jul20_metadata.jsonl")
