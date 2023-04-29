# TraVLR dataset generation

This repo contains code for generating the following datasets:

- Spatiality dataset (SpatialDatasetGen)
- Cardinality dataset (CardinalityDatasetGen)
- Quantifier dataset (QuantifierDatasetGen)
- Numerical comparison dataset (CompareDatasetGen)

Additional code for generating basic datasets used for preliminary experimentation are also included:

- SimpleDatasetGen: Single object. Query: "red circle"
- SimpleDataset2Gen: Single object. Query: "left"/"right"/"bottom"/"top"/"centre"
- SimpleDataset3Gen: Two objects. Query: "There is a red circle and a blue square".

To generate datasets, update const.py and run:
```
python main.py
```

An `index.csv` file and a `metadata.jsonl` file will be generated for each dataset. 

The `index.csv` contains the following columns: caption, query, answer, image, split, id.
The `metadata.jsonl` file will contain fields which differ slightly based on the dataset. 
For instance, the cardinality dataset will contain fields as follows:
- `objects`: a list of objects e.g. {"shape": "octagon", "colour": "yellow", "pattern": null, "row": 0, "column": 5, "size": "medium", "queried": false}. `shape` are `colour` are properties of the object, row and column are the objects' position, and `queried`
- `case`: e.g. ["circle", 2], the "pair" or tuple which is used to determine the train-test split. 
- `caption_abstract`: e.g. `[0, 1, 2, 3, 4, 5, 6, 7, 8]` represents the order in which the objects in `objects_list` are named in the caption.
- `query_abstract`: e.g. `{"attr": "circle", "number": 2, "rel": "equal"}` is an abstract representation of the query.
- `query`: e.g. `There are 2 circle objects.`
- `answer`: e.g. `true`
- `split`: e.g. `train`

## Config

```
INDEX_FILEPATH = "./data/"
IMAGES_FILEPATH = INDEX_FILEPATH + "images/"
NUM_CONDITIONS = {
    'num_train' : 32000,
    'num_val' : 10000,
    'num_val_test' : 10000,
    'num_test' : 20000,
}
DATASET = "cardinality" # "compare/quantifier/cardinality/spatial"
```
- `DATASET`: the dataset to be generated e.g. "quantifier"
- `INDEX_FILEPATH`: the folder where the dataset will be generated
- `IMAGES_FILEPATH`: the folder where the dataset images will be generated
- `NUM_CONDITIONS`: number of examples for each subset/split of the dataset (train, validation, validation test, test)

## Generation from metadata

We also provide code for generating a dataset from a metadata file using the script `gen_metadata.py`. 

- `METADATA_FILE`: the path to the metadata file
- `INDEX_FILEPATH`: the folder where the dataset will be generated
- `DATASET`: the dataset to be generated e.g. "quantifier"

## Unit tests

To run all unit tests:
```
python -m unittest discover Tests
```

To run a specific unit test e.g. test_SpatialQueryGen.py:
```
python -m unittest Tests.test_SpatialQueryGen
```
