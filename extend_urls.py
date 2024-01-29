import glob
import logging
import requests
import pandas as pd
from rich import print
from tqdm.auto import tqdm


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO,
        handlers=[logging.FileHandler("./data/logs.txt"),
                  logging.StreamHandler()],
    )

    logger = logging.getLogger(__name__)

    print("Getting all data bases ...")
    files = glob.glob("./data/*db*.csv")
    logger.info(f"Total number of data bases is {len(files)}")

    session = requests.Session()

    for file in files:
        df = pd.read_csv(file)
        df = df.dropna(subset=["link"]).reset_index(drop=True)
        urls = df.link.to_list()
        logger.info(f"Extending links in the {file} data base ...")

        expanded_urls = []
        for url in tqdm(urls, total=len(urls)):
            resp = session.head(url, allow_redirects=True)
            expanded_urls.append(resp.url)

        df["expanded_link"] = expanded_urls
        new_file = file.replace(".csv", "-expanded_links.csv")
        df.to_csv(new_file, index=False)

    logger.info(f"{'-' * 50}")


if __name__ == "__main__":
    main()
