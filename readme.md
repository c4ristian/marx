# Marx Project

## What is it?
This Python library provides a [notebook](bitcoin_distribution.ipynb) to analyse 
the wealth distribution of Bitcoin. It builds on a [CSV file](data/bitcoin_balances_13052022.csv)
containing the richest bitcoin addresses and their balances. The balances were crawled from the 
website [BitInfoCharts](https://bitinfocharts.com/en/top-100-richest-bitcoin-addresses.html) using 
the script [execute_crawler.py](execute_crawler.py).

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/c4ristian/marx

## Setup
```sh
conda env create -f environment.yml

conda activate marx
```

## Jupyter
### Install Kernel 
```sh
python -m ipykernel install --user --name=marx
```

### Run Notebooks
```sh
jupyter notebook
```

## License
[Apache 2.0](LICENSE.txt)


## Contact us
[christian.koch@th-nuernberg.de](mailto:christian.koch@th-nuernberg.de)
