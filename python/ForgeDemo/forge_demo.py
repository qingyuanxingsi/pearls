# -*- coding: utf-8 -*-

from featureforge.feature import input_schema, output_schema
import unittest
from featureforge.validate import BaseFeatureFixture, APPROX, EQ
from featureforge.feature import make_feature
from schema import And


@input_schema({"height": int})
def image_height(img):
    return img.get("height", 0)

@input_schema({'posts_nr': And(int, lambda i: i >= 0),
               'pictures_nr': And(int, lambda i: i >= 0)})
@output_schema(float, lambda i: i >= 0 and i <= 1)
def picture_posts_ratio(user):
    total = user['posts_nr'] + user['pictures_nr']
    if not total:
        return 0.0
    return float(user['pictures_nr']) / total

class TestPicturesRatio(unittest.TestCase, BaseFeatureFixture):
    feature = make_feature(picture_posts_ratio)
    fixtures = dict(
        test_simple=({"posts_nr": 4, "pictures_nr": 1},
                     APPROX, 0.2),
        test_no_pics=({"posts_nr": 3, "pictures_nr": 0},
                      EQ, 0.0),
        test_nothing=({"posts_nr": 0, "pictures_nr": 0},
                      EQ, 0.0),
    )