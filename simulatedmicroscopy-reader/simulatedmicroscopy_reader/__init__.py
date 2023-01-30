from typing import  List, Dict, Sequence, Union

from simulatedmicroscopy import Image
from pathlib import Path

PathLike = str
PathOrPaths = Union[PathLike, Sequence[PathLike]]


def get_reader(path: PathOrPaths):
    # If we recognize the format, we return the actual reader function
    if isinstance(path, str) and path.endswith(".h5"):
        return h5_file_reader
    # otherwise we return None.
    return None


def h5_file_reader(path: PathOrPaths) -> List:
    p = Path(path)
    im = Image.load_h5file(path)
    data = im.image.copy()  # somehow read data from path
    ps = im.get_pixel_sizes()
    scale = ps/ps.min()
    layer_attributes = {"name": p.stem, "scale": scale}
    return_data = [(data, layer_attributes)]
    if im.get_pixel_coordinates() is not None:
        # @todo: fix scaling 
        coords_layer_attributes = {"name": "coords_"+p.stem, "scale": scale, "edge_color": "red", "face_color": "transparent", "size": [10, 10, 10]}
        coords = im.get_pixel_coordinates().copy()
        return_data.append((coords, coords_layer_attributes, 'points'))    
    
    return return_data