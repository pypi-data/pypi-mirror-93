
"""gh_xray_siamese dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow_datasets.public_api as tfds
from tensorflow_datasets.image_classification import gh_xray_siamese


class GhXraySiameseTest(tfds.testing.DatasetBuilderTestCase):
  # TODO(gh_xray_siamese):
  DATASET_CLASS = gh_xray_siamese.GhXraySiamese
  SPLITS = {
      "train": 3,  # Number of fake train example
      "test": 1,  # Number of fake test example
  }

  # If you are calling `download/download_and_extract` with a dict, like:
  #   dl_manager.download({'some_key': 'http://a.org/out.txt', ...})
  # then the tests needs to provide the fake output paths relative to the
  # fake data directory
  # DL_EXTRACT_RESULT = {'some_key': 'output_file1.txt', ...}


if __name__ == "__main__":
  tfds.testing.test_main()
