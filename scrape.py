import os
import glob
import time
import json
import logging
import pandas as pd
from rich import print
from pathlib import Path
from tqdm.auto import tqdm
from apify_client import ApifyClient


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.FileHandler("./data/logs.txt"), logging.StreamHandler()],
    )

    logger = logging.getLogger(__name__)

    print("Getting all data bases ...")
    files = glob.glob("./data/*expanded_links.csv")
    logger.info(f"Total number of data bases is {len(files)}")

    print("Setting-up the API Client ...")
    with open("./data/api_keys.json") as f:
        api_keys = json.load(f)

    actor_name = "compass/crawler-google-places"
    client = ApifyClient(api_keys[actor_name])
    # Prepare the Actor input
    run_input = {
        "startUrls": [],
        "maxReviews": 99999,
        "language": "en",
        "onlyDataFromSearchPage": True,
        "includeWebResults": False,
        "scrapeDirectories": False,
        "deeperCityScrape": False,
        "reviewsSort": "newest",
        "scrapeReviewerName": True,
        "scrapeReviewerId": True,
        "scrapeReviewerUrl": True,
        "scrapeReviewId": True,
        "scrapeReviewUrl": True,
        "scrapeResponseFromOwnerText": True,
        "skipClosedPlaces": False,
    }

    total_time = 0.0
    for file in files:
        logger.info(f"Extracting links from the {file} data base ...")
        df = pd.read_csv(file)

        logger.info(f"Total links are {len(df)}")

        # Run the Actor and wait for it to finish
        print("Getting data, please wait ...")
        Path("./data/reviews").mkdir(parents=True, exist_ok=True)
        for i, row in tqdm(df.iterrows(), total=len(df)):
            output_file = f"./data/reviews/{row['name']}.json"
            if os.path.exists(output_file):
                logger.info(f"File for {row['link']} already exists. Skipping ...")
                continue
            logger.info(f"Scrapping reviews for {row['link']}")
            run_input["startUrls"] = [{"url": row.expanded_link}]

            # begin scrapping
            start = time.time()
            run = client.actor(actor_name).call(run_input=run_input)
            end = time.time()

            elapsed_time = end - start
            logger.info(f"Elapsed time for {row['link']}: {elapsed_time: 0.4f}s")
            total_time += elapsed_time
            print(f"Total time so far: {total_time: 0.4f}s")

            results = []
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)

            total_textual_reviews = sum(
                [r["text"] is not None for r in results[0]["reviews"]]
            )
            logger.info(f"Total scrapped reviews is {total_textual_reviews}")
            logger.info(f"Total ratings is {len(results[0]['reviews'])}")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Total scrapping time is {total_time: 0.4f}s")
    logger.info(f"{'-' * 50}")


if __name__ == "__main__":
    main()
