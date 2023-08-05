from sigla.helpers.importers import import_from_xml_string
from sigla.classes.nodes.NodeTemplate import NodeTemplate
from sigla.tests.helpers import MemoryNodeTemplate


class TestConvertToInternalClasses:
    def test_simple(self):
        source = "<a name='a'><b name='b'></b></a>"
        got_nodes = NodeTemplate("a", {"name": "a"})
        got_nodes.append(NodeTemplate("b", {"name": "b"}))
        assert (
            import_from_xml_string(source, TemplateClass=MemoryNodeTemplate)
            == got_nodes
        )

    def test_conversion(self):
        source = "<a name='a' age-int='33' price-float='1.2' data-json='{\"v1\": 1}'></a>"  # noqa: E501
        res = import_from_xml_string(source, TemplateClass=MemoryNodeTemplate)
        assert res.attributes == {
            "name": "a",
            "age": 33,
            "price": 1.2,
            "data": {"v1": 1},
        }
