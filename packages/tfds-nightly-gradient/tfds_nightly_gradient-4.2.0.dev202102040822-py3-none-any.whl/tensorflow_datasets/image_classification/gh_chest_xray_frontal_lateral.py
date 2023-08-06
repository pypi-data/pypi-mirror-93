"""gh_chest_xray_frontal_lateral dataset."""

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
gradient health private chest xray data including frontal, lateral and none three category. The dataset has three split: train/val/test. Only the train split has labels.
"""


class GhChestXrayFrontalLateral(tfds.core.GeneratorBasedBuilder):
  """private chest xray data including frontal and lateral"""

  VERSION = tfds.core.Version('0.1.0')
  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
	you need have access to this private dataset
  """

  def _info(self):
    return tfds.core.DatasetInfo(
      builder=self,
      description=_DESCRIPTION,
      features=tfds.features.FeaturesDict({
        "image/name": tfds.features.Text(),
        "image": tfds.features.Image(shape=(None, None, 1),
                                         dtype=tf.uint16,
                                         encoding_format='png'),
        "label": tfds.features.ClassLabel(names=["None", "frontal", "lateral"]),
      }),

      homepage='https://dataset-homepage/',
      citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    data_path = dl_manager.manual_dir
    train_df = pd.read_csv(os.path.join(data_path, "label.csv"))
    train_df.drop('timestamp', axis=1, inplace=True)
    train_df['filename'] = train_df['filename'].apply(lambda fname: os.path.join(data_path, fname))

    val_names = glob(os.path.join(data_path, 'val/*.jpg'))
    val_df =  pd.DataFrame(list(zip(val_names, ["None" for i in range(0, len(val_names))])), columns=['filename', 'label'])

    test_names = glob(os.path.join(data_path, 'test/*.jpg'))
    test_df =  pd.DataFrame(list(zip(test_names, ["None" for i in range(0, len(test_names))])), columns=['filename', 'label'])

    return [
      tfds.core.SplitGenerator(
          name=tfds.Split.TRAIN,
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
      tfds.core.SplitGenerator(
          name=tfds.Split.TEST,
          gen_kwargs={
            'df':test_df,
          },
      ),
    ]

  def _generate_examples(self, df):
    """Yields examples."""
    for idx, row in df.iterrows():
      record = {
        "image/name": "/".join(row.filename.split("/")[-2:]),
        "image": row.filename,
        "label": row.label
      }

      yield idx, record
