import e2edutch.stanza
import stanza
from collections import OrderedDict
import tensorflow.compat.v1 as tf


def test_processor():
    nlp = stanza.Pipeline(lang='nl', processors='tokenize,coref')
