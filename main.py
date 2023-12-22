"""

main.py: This file is the entry point of our application,
and it creates the necessary dependencies and executes the use case.

"""

import argparse
import logging

from src.book.book_controller import build_book_model
from src.book.book_model import GoodReadsBook
from src.book_id.book_id_controller import run as run_book_id_main
from src.common.app_io.reader.reader import (get_books_already_scraped,
                                             get_books_to_scrape, read_file)
from src.common.app_io.writer.writer import create_export_file, write_to_json
from src.review.review_service import run as run_review_main

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)


def main():
    parser = argparse.ArgumentParser()

    # BOOK

    parser.add_argument(
        "-s", "--service", type=str, choices=["book", "book_id", "review"]
    )
    parser.add_argument("-bip", "--book_ids_path", type=str)
    parser.add_argument("-odp", "--output_directory_path", type=str)
    parser.add_argument(
        "-f", "--format", type=str, default="json", choices=["json", "csv"]
    )

    # REVIEW

    parser.add_argument("--browser", type=str)
    parser.add_argument("--sort_order", type=str)

    args = parser.parse_args()

    if args.service == "book_id":
        run_book_id_main()
        logging.info("🎉 Success! [Book ID service] completed successfully! 🎉\n")

    if args.service == "book":
        ids = read_file(args.book_ids_path)
        books_already_scraped = get_books_already_scraped(args.output_directory_path)
        books_ids_to_scrape = get_books_to_scrape(ids, books_already_scraped)

        for book_id in books_ids_to_scrape:
            print(f"SCRAPING: {book_id}")
            try:
                book = GoodReadsBook(id=book_id)
                book_model = build_book_model(book)
                path = f"{args.output_directory_path}/{book_id}.json"

                if book_model.get("authorFullName") is None:
                    print(f"Skipping: {book_id} Author is None")
                else:
                    write_to_json(book_model, path)

            except Exception as e:
                print(f"SKIPPING: {book_id}. See: {e}")
                raise e

        create_export_file(args)
        logging.info("🎉 Success! [Book service] completed successfully! 🎉\n")

    if args.service == "review":
        run_review_main()

        ids = read_file(args.book_ids_path)

        books_already_scraped = get_books_already_scraped(args.output_directory_path)
        book_ids_to_scrape = get_books_to_scrape(ids, books_already_scraped)
        for book_id in book_ids_to_scrape:
            try:
                book_model = build_book_model(book_id)
                path = f"{args.output_directory_path}/{book_id}.json"
                write_to_json(book_model, path)
            except Exception as e:
                print(e)
                raise e

        create_export_file(args)
        logging.info("🎉 Success! [Book service] completed successfully! 🎉\n")
    if args.service == "book_id":
        run_book_id_main()
        logging.info("🎉 Success! [Book ID service] completed successfully! 🎉\n")
    if args.service == "review":
        run_review_main()
        logging.info("🎉 Success! [Review service] completed successfully! 🎉\n")


if __name__ == "__main__":
    main()
