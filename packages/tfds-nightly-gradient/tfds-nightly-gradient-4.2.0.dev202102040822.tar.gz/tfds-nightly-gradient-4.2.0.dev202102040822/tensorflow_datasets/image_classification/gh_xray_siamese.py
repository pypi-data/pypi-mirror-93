"""gh_xray_siamese dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow_datasets.public_api as tfds
import tensorflow as tf
import pandas as pd
from glob import glob
import os


_CITATION = """
"""

_DESCRIPTION = """
Private xray data of Gradient Health
"""


class GhXraySiamese(tfds.core.GeneratorBasedBuilder):
  """Triplets dataset"""

  # TODO(gh_xray_siamese): Set up version.
  VERSION = tfds.core.Version('0.1.0')
  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
	  you need have access to this private dataset
  """

  def _info(self):
    # TODO(gh_xray_siamese): Specifies the tfds.core.DatasetInfo object
    return tfds.core.DatasetInfo(
        builder=self,
        # This is the description that will appear on the datasets page.
        description=_DESCRIPTION,
        # tfds.features.FeatureConnectors
        features=tfds.features.FeaturesDict({
          "image/name": tfds.features.Text(),
          "image": tfds.features.Image(shape=(None, None, 1),
                                         dtype=tf.uint16,
                                         encoding_format='png'),
          "label": tfds.features.ClassLabel(names=["ankle", "hand", "pevic"]),
        }),

        supervised_keys=('image', 'label'),
        # Homepage of the dataset for documentation
        homepage='https://dataset-homepage/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    data_path = dl_manager.manual_dir

    train_names = glob(os.path.join(data_path, 'train/**/*.png'))
    train_labels = [path.split('/')[-2] for path in train_names]
    train_df =  pd.DataFrame(list(zip(train_names, train_labels)), columns=['filename', 'label'])

    val_names = glob(os.path.join(data_path, 'val/**/*.png'))
    val_labels = [path.split('/')[-2] for path in val_names]
    val_df =  pd.DataFrame(list(zip(val_names, val_labels)), columns=['filename', 'label'])



    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
              'df':train_df,
            },
        ),
        tfds.core.SplitGenerator(
          name=tfds.Split.VALIDATION,
          gen_kwargs={
            'df':val_df,
          },
      ),
    ]

  def _generate_examples(self, df):
    """Yields examples."""
    for idx, row in df.iterrows():
      record = {
        "image/name": row.filename.split("/")[-1],
        "image": row.filename,
        "label": row.label
      }

      yield idx, record
