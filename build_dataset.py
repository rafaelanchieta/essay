import logging
import os

import pandas as pd
from sklearn.model_selection import train_test_split

from essay import Essay

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('build_dataset')


class Corpus:
    """
    This class creates and reads the training, development, and test sets.
    """

    def __init__(self, corpus=None):
        """
        Receive the essay as a data frame
        :param corpus:
        """
        if corpus is not None:
            self.corpus = corpus

    def build_corpus(self):
        """
        Build splits for training, development, and testing fo the corpus
        :return:
        """
        training, development, testing = split_stratified_into_train_val_test(self.corpus, stratify_colname='score',
                                                                              random_state=230)
        self.save_split('train', training)
        self.save_split('dev', development)
        self.save_split('test', testing)

    @staticmethod
    def read_corpus() -> (pd, pd, pd):
        """
        Read the splits of the corpus
        :return: training, development, and testing
        """
        path = 'essay-br/splits'
        files = os.listdir(path)
        for file in files:
            if file == 'train.csv':
                training = pd.read_csv(os.path.join(path, file), converters={'essay': eval, 'competence': eval})
            elif file == 'dev.csv':
                development = pd.read_csv(os.path.join(path, file), converters={'essay': eval, 'competence': eval})
            else:
                testing = pd.read_csv(os.path.join(path, file), converters={'essay': eval, 'competence': eval})
        return training, development, testing

    @staticmethod
    def save_split(name: str, df_input):
        """
        Save the splits of the corpus as a csv file
        :param name: name of the split
        :param df_input: content of the splits as a data frame
        :return:
        """
        df_input.to_csv('essay-br/splits/'+name+'.csv', index=False, header=True)
        logger.info(name + '.cs saved in essays-br/splits/')


def split_stratified_into_train_val_test(df_input, stratify_colname='y', frac_train=0.8, frac_val=0.1, frac_test=0.1,
                                         random_state=None):
    """
    Splits a Pandas dataframe into three subsets (train, val, and test)
    following fractional ratios provided by the user, where each subset is
    stratified by the values in a specific column (that is, each subset has
    the same relative frequency of the values in the column). It performs this
    splitting by running train_test_split() twice.

    Parameters
    ----------
    df_input : Pandas dataframe
        Input dataframe to be split.
    stratify_colname : str
        The name of the column that will be used for stratification. Usually
        this column would be for the label.
    frac_train : float
    frac_val   : float
    frac_test  : float
        The ratios with which the dataframe will be split into train, val, and
        test data. The values should be expressed as float fractions and should
        sum to 1.0.
    random_state : int, None, or RandomStateInstance
        Value to be passed to train_test_split().

    Returns
    -------
    df_train, df_val, df_test :
        Dataframes containing the three splits.
    """

    if frac_train + frac_val + frac_test != 1.0:
        raise ValueError('fractions %f, %f, %f do not add up to 1.0' % (frac_train, frac_val, frac_test))

    if stratify_colname not in df_input.columns:
        raise ValueError('%s is not a column in the dataframe' % stratify_colname)

    X = df_input  # Contains all columns.
    y = df_input[[stratify_colname]]  # Dataframe of just the column on which to stratify.

    # Split original dataframe into train and temp dataframes.
    df_train, df_temp, y_train, y_temp = train_test_split(X, y, test_size=(1.0 - frac_train), random_state=random_state)

    # Split the temp dataframe into val and test dataframes.
    relative_frac_test = frac_test / (frac_val + frac_test)
    df_val, df_test, y_val, y_test = train_test_split(df_temp, y_temp, test_size=relative_frac_test,
                                                      random_state=random_state)

    assert len(df_input) == len(df_train) + len(df_val) + len(df_test)

    return df_train, df_val, df_test


if __name__ == '__main__':
    essay = Essay()
    c = Corpus()
    # c.build_corpus()
    train, dev, test = c.read_corpus()
    print(train.shape)
    # print(test.shape)
    # print(dev.shape)
