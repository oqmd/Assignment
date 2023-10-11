# coding:utf-8

import unittest
import pandas as pd
from pandas.testing import assert_frame_equal


def read_file(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError as e:
        return "FileNotFound"


def cal_house_num_between_min_price_and_max_price(min_price, max_price):
    houses = read_file("calendar_dec18.csv")
    houses.dropna(inplace=True)
    houses["price"] = houses["price"].apply(lambda x: float(x.replace("$", "").replace(",", "")))
    select_houses = houses[(houses["price"] <= max_price) & (houses["price"] >= min_price)]
    return len(select_houses["listing_id"].unique())


def find_reviews_by_listing_id(listing_id):
    reviews = pd.read_csv("reviews_dec18.csv")
    return reviews.loc[reviews["listing_id"] == listing_id, "comments"]


class TestReadFile(unittest.TestCase):
    def test_read_file(self):
        file_1 = "listings_dec18.csv"
        file_2 = "listings.csv"
        result = pd.read_csv(file_1)
        self.assertEqual(assert_frame_equal(read_file(file_1), result), None)
        self.assertEqual(read_file(file_2), "FileNotFound")

    def test_cal_house_num_between_min_price_and_max_price(self):
        min_price = 130
        max_price = 300
        self.assertEqual(cal_house_num_between_min_price_and_max_price(min_price, max_price), 12470)

    def test_find_reviews_by_liusting_id(self):
        listing_id = 12351
        self.assertEqual(len(find_reviews_by_listing_id(listing_id)), 493)


if __name__ == '__main__':
    unittest.main()