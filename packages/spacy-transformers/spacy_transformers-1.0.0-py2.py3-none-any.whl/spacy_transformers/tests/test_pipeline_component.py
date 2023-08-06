import pytest
from spacy.language import Language
from spacy.training.example import Example
from spacy.util import make_tempdir
from spacy.vocab import Vocab
from spacy.tokens import Doc
from spacy import util
from spacy_transformers.layers import TransformerListener
from thinc.api import Model, Config
from numpy.testing import assert_equal

from .util import DummyTransformer
from ..pipeline_component import Transformer
from ..data_classes import TransformerData, FullTransformerBatch


@pytest.fixture
def vocab():
    return Vocab()


@pytest.fixture
def docs(vocab):
    return [
        Doc(vocab, words=["hello", "world"]),
        Doc(vocab, words=["this", "is", "another"]),
    ]


@pytest.fixture
def component(vocab):
    return Transformer(Vocab(), DummyTransformer())


@pytest.fixture(scope="module")
def simple_nlp():
    nlp = Language()
    nlp.add_pipe("transformer")
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))

    optimizer = nlp.initialize()
    for i in range(2):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)

    return nlp


def test_init(component):
    assert isinstance(component.vocab, Vocab)
    assert isinstance(component.model, Model)
    assert hasattr(component.set_extra_annotations, "__call__")
    assert component.listeners == []
    assert component.cfg == {"max_batch_items": 4096}


def test_predict(component, docs):
    trf_data = component.predict(docs)
    assert isinstance(trf_data, FullTransformerBatch)
    assert len(trf_data.tensors) == component.model.layers[0].attrs["depth"]
    n_tokens = trf_data.wordpieces.input_ids.shape[1]
    width = component.model.layers[0].attrs["width"]
    assert trf_data.tensors[-1].shape == (len(docs), n_tokens, width)


def test_set_annotations(component, docs):
    trf_data = component.predict(docs)
    component.set_annotations(docs, trf_data)
    for doc in docs:
        assert isinstance(doc._.trf_data, TransformerData)


def test_set_extra_annotations(component, docs):
    Doc.set_extension("custom_attr", default="")

    def custom_annotation_setter(docs, trf_data):
        doc_data = list(trf_data.doc_data)
        for doc, data in zip(docs, doc_data):
            doc._.custom_attr = data

    component.set_extra_annotations = custom_annotation_setter
    trf_data = component.predict(docs)
    component.set_annotations(docs, trf_data)
    for doc in docs:
        assert isinstance(doc._.custom_attr, TransformerData)


def test_listeners(component, docs):
    docs = list(component.pipe(docs))
    for listener in component.listeners:
        assert listener.verify_inputs(docs)


TRAIN_DATA = [
    ("I like green eggs", {"tags": ["N", "V", "J", "N"]}),
    ("Eat blue ham", {"tags": ["V", "J", "N"]}),
]


def test_transformer_pipeline_simple(simple_nlp):
    """Test that a simple pipeline with just a transformer at least runs"""
    doc = simple_nlp("We're interested at underwater basket weaving.")
    assert doc


def test_transformer_pipeline_long_token(simple_nlp):
    """Test that a simple pipeline does not raise an error on texts that exceeds
    the model max length. We should truncate instead.
    """
    doc = simple_nlp("https://example.com/" + "a/" * 1000)


cfg_string = """
    [nlp]
    lang = "en"
    pipeline = ["transformer","tagger"]

    [components]

    [components.tagger]
    factory = "tagger"
    
    [components.tagger.model]
    @architectures = "spacy.Tagger.v1"
    nO = null

    [components.tagger.model.tok2vec]
    @architectures = "spacy-transformers.TransformerListener.v1"
    grad_factor = 1.0
    upstream = ${components.transformer.name}
    
    [components.tagger.model.tok2vec.pooling]
    @layers = "reduce_mean.v1"

    [components.transformer]
    factory = "transformer"
    name = "custom_upstream"
    """


def test_transformer_pipeline_tagger():
    """Test that a pipeline with just a transformer+tagger runs and trains properly"""
    orig_config = Config().from_str(cfg_string)
    nlp = util.load_model_from_config(orig_config, auto_fill=True, validate=True)
    assert nlp.pipe_names == ["transformer", "tagger"]
    tagger = nlp.get_pipe("tagger")
    transformer = nlp.get_pipe("transformer")
    tagger_trf = tagger.model.get_ref("tok2vec").layers[0]
    assert isinstance(transformer, Transformer)
    assert isinstance(tagger_trf, TransformerListener)
    assert tagger_trf.upstream_name == "custom_upstream"
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
        for tag in t[1]["tags"]:
            tagger.add_label(tag)

    # Check that the Transformer component finds it listeners
    assert transformer.listeners == []
    optimizer = nlp.initialize(lambda: train_examples)
    assert tagger_trf in transformer.listeners

    for i in range(2):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)

    doc = nlp("We're interested at underwater basket weaving.")
    doc_tensor = tagger_trf.predict([doc])
    assert_equal(doc._.trf_data.tensors, doc_tensor[0].tensors)

    # ensure IO goes OK
    with make_tempdir() as d:
        file_path = d / "trained_nlp"
        nlp.to_disk(file_path)
        nlp2 = util.load_model_from_path(file_path)
        doc = nlp2("We're interested at underwater basket weaving.")
        tagger2 = nlp2.get_pipe("tagger")
        tagger_trf2 = tagger2.model.get_ref("tok2vec").layers[0]
        doc_tensor2 = tagger_trf2.predict([doc])
        assert_equal(doc_tensor2[0].tensors, doc_tensor[0].tensors)


def test_transformer_pipeline_empty():
    """Test that the pipeline doesn't fail with empty input"""
    orig_config = Config().from_str(cfg_string)
    nlp = util.load_model_from_config(orig_config, auto_fill=True, validate=True)
    tagger = nlp.get_pipe("tagger")
    train_examples = []
    for t in TRAIN_DATA:
        train_examples.append(Example.from_dict(nlp.make_doc(t[0]), t[1]))
        for tag in t[1]["tags"]:
            tagger.add_label(tag)

    # train on empty doc
    optimizer = nlp.initialize()
    losses = {}
    empty_train_example = Example.from_dict(nlp.make_doc(""), {})
    nlp.update(train_examples, sgd=optimizer, losses=losses)
    nlp.update([empty_train_example], sgd=optimizer, losses=losses)
    train_examples.append(empty_train_example)
    nlp.update(train_examples, sgd=optimizer, losses=losses)

    # predict empty doc
    doc = nlp("")
    _assert_empty(doc._.trf_data)
    docs = nlp.pipe(["", ""])
    for doc in docs:
        _assert_empty(doc._.trf_data)
    nlp.pipe([])

    # predict combination of empty and non-empty
    doc = nlp("This is a sentence")
    normal_tags = [t.tag_ for t in doc]

    docs = list(nlp.pipe(["", "This is a sentence", "", ""]))
    _assert_empty(docs[0]._.trf_data)
    assert [t.tag_ for t in docs[0]] == []
    assert [t.tag_ for t in docs[1]] == normal_tags
    _assert_empty(docs[2]._.trf_data)
    _assert_empty(docs[3]._.trf_data)


def _assert_empty(trf_data):
    assert trf_data.wordpieces.strings == []
    assert trf_data.wordpieces.input_ids.size == 0
    assert trf_data.wordpieces.attention_mask.size == 0
    assert trf_data.tensors == []
    assert len(trf_data.align.data) == 0
