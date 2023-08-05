from typing import Iterable, Dict

import paddle.nn as nn
import paddle.nn.functional as F
from paddle import Tensor


class CosineSimilarityLoss(nn.Layer):
    """
    CosineSimilarityLoss expects, that the inputs consist of two sentence embedding (u and v) and a float label.

    It computes the vectors u = model(input_text[0]) and v = model(input_text[1]) and measures the cosine-similarity between the two.
    By default, it minimizes the following loss: ||input_label - cosine_sim(u,v)||_2.

    Args:
        loss_fct(nn.Layer, optinal, defaults to obj: `nn.MSELoss()`): The loss function should be used to compare the cosine_similartiy(u,v) with the input_label? 
            By default, MSE: ||input_label - cosine_sim(u,v)||_2

    Example::


    """
    def __init__(self, loss_fct = nn.MSELoss()):
        super(CosineSimilarityLoss, self).__init__()
        self.loss_fct = loss_fct


    def forward(self, sentence_embeddings: Iterable[Tensor], labels: Tensor):
        # embeddings = [self.model(sentence_feature)['sentence_embedding'] for sentence_feature in sentence_features]

        output = F.cosine_similarity(sentence_embeddings[0], sentence_embeddings[1])
        return self.loss_fct(output, labels)

