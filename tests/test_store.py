from configurinator.common import File
from configurinator.persist.store import deserialize, serialize
from configurinator.utils.ui import YesNoResult


def test_serialize_deserialize():
    objs = [True, 1, 1., 'test', File(__file__), YesNoResult(True, False)]
    for obj in objs:
        assert deserialize(serialize(obj)) == obj
