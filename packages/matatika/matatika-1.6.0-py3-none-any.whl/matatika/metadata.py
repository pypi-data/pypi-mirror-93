"""metadata module"""

import json


class Metadata:
    """Class for metadata objects"""

    def __init__(self, metadata):
        self.metadata = metadata

    def get_labels(self):
        """Returns all labels"""

        labels = []

        for label in _yield_values_by_key(self.metadata.get('related_table'), 'label'):
            labels.append(label)

        return labels

    @staticmethod
    def from_str(metadata_str):
        """Resolves a metadata object from a string"""

        return Metadata(json.loads(metadata_str))


def data_with_metadata_labels(data, metadata):
    """Creates a copy of data with keys replaced by labels resolved from metadata"""

    label_sources = {
        k: v for (k, v) in metadata['related_table'].items() if isinstance(v, list)}

    new_data = []

    for data_point in data:
        new_data_point = {}
        for old_key in data_point.keys():

            result = _search_for_key_value(label_sources, 'key', old_key)
            new_key = result['label'] if result else old_key
            new_data_point[new_key] = data_point[old_key]

        new_data.append(new_data_point)

    return new_data


def _search_for_key_value(node, key, val):

    if isinstance(node, dict):
        key_val = node.get(key)
        if key_val:
            if key_val == val:
                return node

        for sub_node in node.values():
            result = _search_for_key_value(sub_node, key, val)
            if result:
                return result

    elif isinstance(node, list):
        for sub_node in node:
            result = _search_for_key_value(sub_node, key, val)
            if result:
                return result

    return None


def _yield_values_by_key(node, key):

    if isinstance(node, dict):
        key_val = node.get(key)
        if key_val:
            yield key_val

        for sub_node in node.values():
            yield from _yield_values_by_key(sub_node, key)

    elif isinstance(node, list):
        for sub_node in node:
            yield from _yield_values_by_key(sub_node, key)
