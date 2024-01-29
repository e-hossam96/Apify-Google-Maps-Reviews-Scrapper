# Apify Google Maps Scrapper

Scrapping google maps reviews for places provided their links in its shortened form by using [Apify](https://apify.com/) actors.

## Setup

- Download and install Anaconda from https://www.anaconda.com/download
- Open the `anaconda powershell prompt` from the start menu or seach the menu bar for it.
- Create a new python environment by executing the command `conda create -n api python=3.11 pip`
- Activate the new environment by executing `conda activate api`
- Clone the repository or download it from GitHub
- Change the current directory to where the repository is located
- Install the requirements by executing `pip install -r requirements.txt`
- Add the data folder in the same driectory inside the repository.

You should have the following files and the data folder:

```bash
$ ls
README.md  data/  extend_urls.py  requirements.txt  scrape.py
```

The data folder contains the `JSON` file containing the tokens and the data bases which contain the links collected before.

```bash
$ ls data
api_keys.json  hospitals_db-a.csv  hospitals_db-b.csv
```

## Subscription

To be able to use the code, you need to provide your API key for the [Google Maps Crawler](https://apify.com/compass/crawler-google-places) in a file called `api_keys.json` in the data directory as follows:

```json
{
  "compass/crawler-google-places": "APIFY_API_KEY"
}
```

To get the API key:

- Head to the [Google Maps Crawler](https://apify.com/compass/crawler-google-places).
- Create the account and select `Try for free`
- Once directed to the console, you will see the `Google Maps Crawler` in your `Actors` tab on the left
- Click on the actor and select `API Clients` from the `API` tab on the right and hit the copy button on top next to `API Tokens`
- Paste the API key in the json file above

## Crawling

The provided links are shortened which is not expected by the API, so we will expand them. The following steps will process the data bases and save the new version. Follow the commands below to start scrapping the reviews:

```shell
python ./extend_urls.py
python ./scrape.py
```

The [scrape](./scrape.py) scripts will load all the processed data bases, copy the links, and start crawling the reviews for each link. Once a link is totally craweled, the reviews will be save in a new dirctory called `reviews` under the `data` folder. Don't update the `reviews` folder until the entire process is completed. If at any point you need to stop the execution, press `CTRL+C` or `⌘+C`. When you need to rerun the code, the code will continue from where it left off.
