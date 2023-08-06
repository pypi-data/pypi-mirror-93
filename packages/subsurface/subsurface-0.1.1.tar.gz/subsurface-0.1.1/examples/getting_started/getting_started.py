"""
Getting started
===============
"""

# %%md
# Authors: Miguel de la Varga and Alexander Juestel
#
# This example how to read into subsurface structures a bunch of different
# data such as:
#
# - well data -> from csv all in one single file
#
# - topography -> from tif
#
# - Cross sections with textures from trace -> shp, png
#
# - Exported gempy model from netcdf


# %%
import shutil
import pandas as pd
import subsurface as ss
import pooch

# %%
# Read wells:
# -----------
# We can read well data - using welly as backend. First we need to have the
# data in the right format for digesting.

# %%

# Pulling data example
import subsurface.interfaces.to_liquid_earth
import subsurface.io.profiles.profiles_core
import subsurface.io.topography.topo_core
import subsurface.io.wells.wells_interface

model_file = pooch.retrieve(
    url="https://github.com/cgre-aachen/gempy_data/raw/master/"
        "data/subsurface/example1.zip",
    known_hash=None
)

data_path = model_file[:-4]
shutil.unpack_archive(model_file, extract_dir=model_file[:-4])

# Read original file
ori_wells = pd.read_csv(data_path + '/wells.csv')

# Add top and base columns
wells_fixed = ss.io.wells.add_tops_from_base_and_altitude_in_place(
    ori_wells,
    'Index',
    'Z',
    'Altitude'
)

wells_fixed['md'] = wells_fixed['top']
wells_fixed.to_csv(data_path + '/wells.csv')
wells_fixed

# %%md
# Now we can read the csv files into subsurface.UnstructuredData

# %%
wells_unstructured_data = ss.io.read_wells_to_unstruct(
    collar_file=data_path + '/wells.csv',
    read_collar_kwargs={
        'usecols': ['Index', 'X', 'Y', 'Altitude'],
        'header': 0
    },
    survey_file=data_path + '/wells.csv',
    read_survey_kwargs={
        'index_col': 'Index',
        'usecols': ['Index', 'md']  # if incl and azi not given -> well vertical
    },
    lith_file=data_path + '/wells.csv',
    read_lith_kwargs={
        'index_col': 'Index',
        'usecols': ['Index', 'top', 'base', 'formation'],
        'columns_map': {'top': 'top',
                        'base': 'base',
                        'formation': 'component lith',
                        }
    }

)


# %%
wells_unstructured_data

# %%md
# From UnstructuredData we can create geometric objects such a lines, points, meshes,
# etc. In the case of boreholes `subsurface.LineSet` is the most suitable geometric
# representation.

# %%
wells_element = ss.LineSet(wells_unstructured_data)

# %%
# All elements in subsurface have their direct link to a pyvista mesh. This
# transformation can be done by the functions `to_pyvista_...`.

# Pyvista mesh
wells_mesh = ss.visualization.to_pyvista_line(wells_element, radius=50)

# Plotting
ss.visualization.pv_plot(
    [wells_mesh],
    image_2d=False,
    ve=5
)

# %%md
# We can do the same for point data, for example the borehole location.

# %%

# UnstructuredData
borehole_location_struct = subsurface.io.wells.wells_interface.borehole_location_to_unstruct(
    collar_file=data_path + '/wells.csv',
    read_collar_kwargs={
        'usecols': ['Index', 'X', 'Y', 'Altitude'],
        'header': 0,
        'columns_map': {
            'X': 'x', 'Y': 'y', 'Altitude': 'altitude'
        }
    }
)
borehole_location_struct

# %%
# Element
borehole_location_point_set = ss.PointSet(borehole_location_struct)
borehole_location_point_set

# %%
# Pyvista mesh
borehole_loc_mesh = ss.visualization.to_pyvista_points(borehole_location_point_set)
borehole_loc_mesh

# %%
ss.visualization.pv_plot(
    [borehole_loc_mesh],
    image_2d=False,
    ve=5
)


# %%md
# Read Topography
# ---------------

# %%

# StructuredData
topo_structured_data = subsurface.io.topography.topo_core.read_structured_topography(data_path + '/DEM50.tif')
topo_structured_data
# %%
# Remove outliers
topo_structured_data.replace_outliers('topography', 0.98)

# Element
topo_element = ss.structs.StructuredGrid(topo_structured_data)
topo_element

# Pyvista mesh
topo_mesh = ss.visualization.to_pyvista_grid(topo_element, 'topography',
                                             data_order='C')

# %%
ss.visualization.pv_plot(
    [topo_mesh],
    image_2d=False,
    ve=5
)


# %%md
# Read Profiles
# -------------

# %%

profiles_traces = subsurface.io.profiles.profiles_core.lineset_from_trace(
    data_path + '/Profiles_cropped/Profile_PyVista.shp',
    idx=range(13)
)

# %%
profiles_trisurf_list, profiles_mesh_list = subsurface.io.profiles.profiles_core.create_tri_surf_from_traces_texture(
    data_path + '/Profiles_cropped/Profile_PyVista.shp',
    path_to_texture=[
        data_path + '/Profiles_cropped/profile001.png',
        data_path + '/Profiles_cropped/profile002.png',
        data_path + '/Profiles_cropped/profile003.png',
        data_path + '/Profiles_cropped/profile004.png',
        data_path + '/Profiles_cropped/profile005.png',
        data_path + '/Profiles_cropped/profile006.png',
        data_path + '/Profiles_cropped/profile007.png',
        data_path + '/Profiles_cropped/profile008.png',
        data_path + '/Profiles_cropped/profile009.png',
        data_path + '/Profiles_cropped/profile010.png',
        data_path + '/Profiles_cropped/profile011.png',
        data_path + '/Profiles_cropped/profile012.png',
        data_path + '/Profiles_cropped/profile013.png',
    ],
    idx=range(13),
    return_mesh=True,
    return_uv=True
)

# %%
ss.visualization.pv_plot(
    profiles_mesh_list,
    image_2d=False,
    ve=5
)

# %%md
# GemPy Mesh
# ----------

# %%
# UnstructuredData
gempy_unstructured_data = ss.io.read_unstruct(data_path + '/meshes.nc')

# Element
trisurf_gempy = ss.TriSurf(gempy_unstructured_data)

# Pyvista mesh
gempy_mesh = ss.visualization.to_pyvista_mesh(trisurf_gempy)

# %%
ss.visualization.pv_plot(
    [gempy_mesh],
    image_2d=False,
    ve=5
)


# %%
# sphinx_gallery_thumbnail_number = 6


# %%
# Export to binary
# ----------------

# %%
subsurface.interfaces.to_binary.base_structs_to_binary_file(data_path + '/gempy_base',
                                                            gempy_unstructured_data)
subsurface.interfaces.to_binary.base_structs_to_binary_file(data_path + '/wells',
                                                            wells_unstructured_data)
subsurface.interfaces.to_binary.base_structs_to_binary_file(data_path + '/topo',
                                                            topo_structured_data)
subsurface.interfaces.to_binary.base_structs_to_binary_file(data_path + '/collars',
                                                            borehole_location_struct)

for e, tri_surf in enumerate(profiles_trisurf_list):
    subsurface.interfaces.to_binary.base_structs_to_binary_file(data_path + f'/profile_{e}_mesh',
                                                                tri_surf.mesh)
    subsurface.interfaces.to_binary.base_structs_to_binary_file(
        data_path + f'/profile_{e}_texture_C',
        tri_surf.texture,
        order='C')

