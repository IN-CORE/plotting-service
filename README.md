# Plotting Service 
IN-CORE service to generate sample points for plotting fragiliy curves

## Create a conda environment
cd plotting-service
conda env create -f env.yml

## Initialize the database first
cd util-script
python init_db.py

## RUN
cd plotting-service
python app.py OR flask run

## Testing the flask app
cd test
python test_sample.py

## License

This project is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/MPL/2.0/). See [LICENSE](LICENSE).
