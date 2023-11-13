# Eevee: An Easy Annotation Tool

## Installation
There is no need to install, just go to https://axelsorensendev.github.io/Eevee/ and get started!

## Usage
### Setup page


### Annotation interface


### Shortcuts


## Use-cases
- [Annotate slot and intent detection for a new language](docs/xsid.md)
- 

## Compatability with other services
### Datasets library
To use data from the Huggingface datasets library with Eevee, we provide the `hf2conll.py` script. To use it, the steps are as follows:

* Find the dataset you would like to add annotation to: https://huggingface.co/datasets
* Download the data with: `python3 scripts/hf2conll.py conll2003`
* Import the data into Eevee, and use the setup-page as explained in [Usage](#usage)

### MaChAmp
The data exported from Eevee can directly be used in the [MaChAmp toolkit](https://github.com/machamp-nlp/), to easily train
and evaluate state-of-the-art models. However, MaChAmp is based on dataset configuration files. These can automatically be 
generated from the output of Eevee. This can be done with the `eevee2machamp` script provided in the `scripts` folder. The 
script expects an Eevee dataset file and the path to the training data (+optionally development data path), as follows:

```
python3 scripts/eevee2machamp.py pokemon.json and pokemon.conll
```

The script will produce a MaChAmp dataset configuration file and the training command.

