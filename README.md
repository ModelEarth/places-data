# Places Data

Uses a Github Action to fetch and uncompress the All the Place tar.gz file to the output folder.

Data from alltheplaces.xyz

	python3 -m venv env &&
	source env/bin/activate

	python alltheplaces_to_csv.py

Output resides in [places-data](https://github.com/ModelEarth/places-data) repo.
