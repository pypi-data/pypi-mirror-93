import os

from easycv.pipeline import Pipeline
from easycv.transforms import Blur, Noise


def test_name():
    p = Pipeline([Noise(method="gaussian"), Noise(method="pepper"), Noise(method="sp")])
    assert p.name == "pipeline"
    p = Pipeline([Noise(method="sp"), Noise(method="gaussian")], name="test-pipeline")
    assert p.name == "test-pipeline"


def test_description():
    p = Pipeline([Noise(method="pepper"), Noise(method="gaussian", var=0.2)])
    p2 = Pipeline([Noise(method="pepper"), Noise(method="gaussian", var=0.2)])
    assert p.description() == p2.description()
    p3 = Pipeline([Noise(method="pepper"), Noise(method="gaussian")])
    p4 = Pipeline([Noise(method="pepper", amount=0.125), Noise(method="gaussian")])
    assert p3.description() != str(p4)


def test_num_transforms():
    p = Pipeline([Noise(method="sp"), Noise(method="pepper"), Noise(method="gaussian")])
    p2 = Pipeline([Noise(method="sp"), p, Noise(method="gaussian")])
    assert p2.num_transforms() == 5


def test_add_transform():
    p1 = Pipeline([Blur()])
    p2 = Pipeline([Blur(), Noise(method="gaussian")])
    p1.add_transform(Noise(method="gaussian"))
    assert p1 == p2
    p3 = Pipeline([Blur(), Noise(method="salt"), Noise(method="gaussian")])
    p2.add_transform(Noise(method="salt"), index=1)
    assert p2 == p3


def test_transforms():
    p = Pipeline([Noise(method="sp"), Noise(method="pepper"), Noise(method="gaussian")])
    assert len(p.transforms()) == p.num_transforms()


def test_save():
    p = Pipeline(
        [Blur(), Noise(method="pepper"), Noise(method="gaussian", var=0.4)],
        name="test",
    )
    p.save()
    assert os.path.exists("test.pipe")
    p2 = Pipeline("test.pipe")
    assert p == p2
    os.remove("test.pipe")
