from typing import  List, Dict, Sequence, Union
import napari
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
    viewer = napari.current_viewer()
    p = Path(path)
    im = Image.load_h5file(path)
    data = im.image.copy()  # read data from file
    pixel_size_um = im.get_pixel_sizes(unit="µm")

    # set name and scale of image
    layer_attributes = {"name": p.stem, "scale": pixel_size_um}

    # add to list that will be returned
    return_data = [(data, layer_attributes)]

    # if coords are present, include those as points
    if im.get_pixel_coordinates() is not None:
        # @todo: fix scaling 
        coords_layer_attributes = {"name": "coords_"+p.stem, "scale": pixel_size_um, "edge_color": "red", "face_color": "transparent", "size": 10.}
        coords = im.get_pixel_coordinates().copy()

        # add as layer
        return_data.append((coords, coords_layer_attributes, 'points'))    
    
    # set correct scaling
    viewer.scale_bar.visible = True
    viewer.scale_bar.unit = "um"
    
    return return_data