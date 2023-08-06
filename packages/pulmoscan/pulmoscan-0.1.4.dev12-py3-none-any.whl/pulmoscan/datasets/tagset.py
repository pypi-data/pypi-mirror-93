'''
Contains tools connected with tagsets.
'''


import typing
import os

import gin

@gin.configurable
class GlobalTagset:
    """Implements Tagset functionality for all datasets involved into training.

    Args:
        mapping (typing.Mapping[str, str]): Local to global labels mapping.
    """

    def __init__(self, mapping: typing.Mapping[str, str]):
        super().__init__()
        unique_global_values = sorted(set(mapping.values()))

        self._loc_to_glob = mapping
        self._glob_to_id: typing.MutableMapping[str, int] = {}
        for i, value in enumerate(unique_global_values):
            self._glob_to_id[value] = i

    def convert_global_to_id(self, global_label: str) -> int:
        '''
        Converts global (universal) labels to int identifier.
        '''

        return self._glob_to_id[global_label]

    def convert_local_to_id(self, local_label: str) -> int:
        '''
        Converts dataset-specific label to int identifier.
        '''

        return self._glob_to_id[self._loc_to_glob[local_label]]

    def convert_to_label(self, id_):
        '''
        Converts id to global label. Not implemented.
        '''

        raise NotImplementedError

    def __contains__(self, local_label: str) -> bool:
        '''
        Is global label in tagset.
        '''

        return local_label in self._loc_to_glob

    def __len__(self) -> int:
        '''
        Number of global labels is a size of the tagset.
        '''

        return len(self._glob_to_id)

    @property
    def labels(self) -> typing.List[str]:
        '''
        Returns all global labels as a list.
        '''

        return list(self._glob_to_id.keys())

    def to_dict(self) -> typing.Mapping[str, str]:
        '''
        Converts tagset to dictionary for serialization purposes.
        '''

        return {
            name: str(id_) for name, id_ in self._glob_to_id.items()
        }


def _read_map(path_to_file: str, separator: str = ';') -> typing.Mapping[str, str]:
    """Reads mapping from file.

    Args:
        path_to_file (str): Path to source file. It must contain lines with two
            words separated by ``separator``. The first one is local label, the second
            one is a global equivalent for the given local.
        separator (str, optional): Defaults to ';'.

    Returns:
        typing.Mapping[str, str]: local-to-global labels dictionary.
    """

    local_to_global_label: typing.MutableMapping[str, str] = {}
    with open(path_to_file, 'r') as mapping:
        for line in mapping:
            line = line.strip('\n')
            local, global_ = line.split(separator)
            local_to_global_label[local] = global_
    return local_to_global_label


@gin.configurable
def union_tagsets(
        list_of_paths_to_label_mappings: typing.Optional[typing.List[str]] = None
    ) -> GlobalTagset:
    """Union dataset-specific mappings from dataset's labels to global labels into Tagset.

    Args:
        list_of_paths_to_label_mappings (Optional[typing.List[str]]): List of paths to files
            that contain lines in format "local_label\tglobal_label".

    Returns:
        Tagset: An instance of :func:`GlobalTagset` class.
    """
    if list_of_paths_to_label_mappings is None:
        raise ValueError('None "list_of_paths_to_label_mappings" is not allowed')

    common_mapping: typing.MutableMapping[str, str] = {}
    for mapping_file in list_of_paths_to_label_mappings:
        if not os.path.exists(mapping_file):
            raise FileNotFoundError(f'Missing mapping file: {mapping_file}')
        mapping = _read_map(mapping_file)
        for key, value in mapping.items():
            if key in common_mapping and value != common_mapping[key]:
                err_msg = f'Key conflict. Key = {key}, File={mapping_file}. '
                err_msg += f'Mapping already has that key with another global label:{mapping[key]}. '
                err_msg += f'Trying to insert {value}.'
                raise KeyError(err_msg)
            common_mapping[key] = value

    return GlobalTagset(common_mapping)


LOCAL_MAPPINGS_PATHS = ['resources/mappings/rsna.txt', ]

@gin.configurable
def build_global_tagset() -> GlobalTagset:
    '''
    Returns current global tagset.
    '''

    return union_tagsets(LOCAL_MAPPINGS_PATHS)
