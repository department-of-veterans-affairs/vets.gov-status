> Updates the data powering the charts

These scripts automate updating the data that powers the charts for the scorecard. They pull data from Google Analytics.

## Running the scripts

There are three main scripts. They currently share a large portion of the code and will be refactored at some point.

- `update_data.py` is the main script providing the general chart data

- `update_filtered_views.py` is essentially the same but filters the data down by a path prefix.

- `update_vcl_clicks.py` is a specific script for pulling in clicks on the Veterans' Crisis Line

The scripts expect `serviceaccount.p12` which is a Google Service Account with access to the Google Analytics account. There are instructions at https://developers.google.com/identity/protocols/OAuth2ServiceAccount on getting that setup.

### System requirements

You'll need Python >= 3.5 (tested on Python 3.5.2) and pip. You can install in a virtual environment if you prefer to isolate the code.

The steps are:
 - `pip install -r requirements.txt`
 - `python3 update_data.py`
 - `python3 update_vcl_clicks.py`
 - `python3 update_filtered_views.py`

 Once complete you will have a set of csv files with the updated data. These can be moved to `_data` to update the charts.

## Configuration

Edit `config.json` with a list of file prefix to Google Analytics View ID mappings. You can find the View ID in Google Analytics Admin view, far right column is the view. Be sure to use the "All Web Site Data" view. Then click View Settings. View ID will be listed at the top.

For those boards that need a filtered set of data, that can be provided using `filtered.json` which has a `page_filter` field which provides a path prefix to match against. We use this primarily for different forms on our site that share the same Google Analytics property.

## Automation

We use the shell scripts `run_update.sh` and `run_python_script.sh` to automate much of the work each week to update the data and create a PR. These scripts are tailored to our environment and expect a GitHub API token to be configured in the `gitconfig` file. You will need to modify this to meet your own needs if you wish to use them.

We intend to transition from these shell scripts (currently invoked by cron) to a Jenkins-based system in the future.
