import pathlib
import collections

import dtoolcore

from dtoolbioimage import Image as dbiImage



def iter_identifiers_with_extension(dataset, extension):

    for idn in dataset.identifiers:
        if dataset.item_properties(idn)["relpath"].endswith(extension):
            yield idn


class IndexedDirtree(object):

    def __init__(self, base_dirpath):
        self.base_dirpath = pathlib.Path(base_dirpath)
        self.index = {
            dtoolcore.utils.generate_identifier(str(rpath)): rpath
            for rpath in self.relpath_iter
        }

    @property
    def abspath_iter(self):
        return (
            fpath
            for fpath in self.base_dirpath.rglob("*")
            if fpath.is_file()
        )

    @property
    def relpath_iter(self):
        return (
            fpath.relative_to(self.base_dirpath)
            for fpath in self.abspath_iter
        )

    @property
    def identifiers(self):
        return list(self.index)

    def item_properties(self, idn):
        rpath = self.index[idn]
        return {
            'relpath': str(rpath)
        }

    def item_content_abspath(self, idn):
        return self.base_dirpath/self.index[idn]

    def __len__(self):
        return len(self.identifiers)


class ImageDataSetView(collections.abc.Sequence):

    def __init__(self, container):
        self.container = container
        self.identifiers = list(iter_identifiers_with_extension(container, ".jpg"))

    def __len__(self):
        return len(self.identifiers)

    def __getitem__(self, idx):
        idn = self.identifiers[idx]
        return self.item_by_idn(idn)

    def item_by_idn(self, idn):
        fpath = self.container.item_content_abspath(idn)
        im = dbiImage.from_file(fpath)
        im.properties = self.container.item_properties(idn)
        return im

