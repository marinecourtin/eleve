import pytest

from eleve.memory import MemoryStorage
from eleve.incremental_memory import IncrementalMemoryStorage
from eleve import Eleve

@pytest.mark.parametrize("storage_class", [MemoryStorage, IncrementalMemoryStorage])
def test_basic_entropy(storage_class):
    """
    Forward that begins by « le petit »:
     - le petit chat
     - le petit chien
     - le petit None * 2
    Backward that begins by « petit le » :
     - petit le None * 2
     - petit le pour * 2
    --> count is the mean of 4 and 4, and entropy is the mean of 1.5 and 1.
    """
    m = Eleve(2, storage_class)
    m.add_sentence(['le','petit','chat'])
    m.add_sentence(['le','petit','chien'])
    m.add_sentence(['pour','le','petit'], freq=2)
    assert m.query_node(('le', 'petit')) == (4.0, 1.25)

def test_basic_segmentation():
    l = Eleve(2)
    l.add_sentence(['je', 'vous', 'parle', 'de', 'hot', 'dog'])
    l.add_sentence(['j', 'ador', 'les', 'hot', 'dog'])
    l.add_sentence(['hot', 'dog', 'ou', 'pas'])
    l.add_sentence(['hot', 'dog', 'ou', 'sandwich'])

    assert l.segment(['je', 'deteste', 'les', 'hot', 'dog']) == [['je'], ['deteste'], ['les'], ['hot', 'dog']]
    #assert l.segment(['je', 'deteste', 'les', 'sandwich']) == [['je'], ['deteste'], ['les'], ['sandwich']]
    assert l.segment(['je', 'vous', 'ou', 'hot', 'dog']) == [['je', 'vous'], ['ou'], ['hot', 'dog']]
