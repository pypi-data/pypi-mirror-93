"""
Helper functions for parsing files and processing headers.
"""
import datetime
import re
from functools import partial
from pathlib import Path

import numpy as np
import scipy.stats
from astropy.io import fits
from astropy.table import Table
import gwcs.coordinate_frames as cf

from dkist_inventory.transforms import TransformBuilder

__all__ = ['generate_inventory_from_frame_inventory', 'sort_headers', 'headers_from_filenames']


def process_json_headers(bucket, json_headers):
    """
    Extract the filenames and FITS headers from the inventory headers.

    Parameters
    ----------
    bucket: `str`
        The bucket in which the dataset resides.
    json_headers : `list` of `dict
        A list of dicts containing the JSON version of the headers as stored in inventory.

    Returns
    --------
    filenames
        The filenames (object keys) of the FITS files.
    fits_headers
        The FITS headers.
    extra_inventory
        The inventory keys directly extracted from the frame inventory

    """
    known_non_fits_keys = {
        "_id",
        "bucket",
        "frameStatus",
        "objectKey",
        "createDate",
        "updateDate",
        "lostDate",
    }
    fits_keys = set(json_headers[0].keys()).difference(known_non_fits_keys)

    def key_filter(keys, headers):
        return {x: headers[x] for x in keys if x in headers}

    non_fits_headers = list(map(partial(key_filter, known_non_fits_keys), json_headers))
    fits_headers = list(map(partial(key_filter, fits_keys), json_headers))

    filenames = [Path(h["objectKey"]).name for h in non_fits_headers]

    extra_inventory = {
        "original_frame_count": len(json_headers),
        "bucket": bucket,
        "create_date": datetime.datetime.utcnow().isoformat("T"),
    }

    return filenames, fits_headers, extra_inventory


def headers_from_filenames(filenames, hdu=0):
    """
    Generator to get the headers from filenames.
    """
    return [dict(fits.getheader(fname, ext=hdu)) for fname in filenames]


def table_from_headers(headers):
    return Table(rows=headers, names=list(headers[0].keys()))


def validate_headers(table_headers):
    """
    Given a bunch of headers, validate that they form a coherent set.

    This function also adds the headers to a list as they are read from the
    file.

    Parameters
    ----------
    headers :  iterator
        An iterator of headers.

    Returns
    -------
    out_headers : `list`
        A list of headers.
    """
    t = table_headers

    # Let's do roughly the minimal amount of verification here for construction
    # of the WCS. Validation for inventory records is done independently.

    # For some keys all the values must be the same
    same_keys = ["NAXIS", "DNAXIS"]
    naxis_same_keys = ["NAXISn", "CTYPEn", "CRVALn"]  # 'CRPIXn'
    dnaxis_same_keys = ["DNAXISn", "DTYPEn", "DPNAMEn", "DWNAMEn"]
    # Expand n in NAXIS keys
    for nsk in naxis_same_keys:
        for naxis in range(1, t["NAXIS"][0] + 1):
            same_keys.append(nsk.replace("n", str(naxis)))
    # Expand n in DNAXIS keys
    for dsk in dnaxis_same_keys:
        for dnaxis in range(1, t["DNAXIS"][0] + 1):
            same_keys.append(dsk.replace("n", str(dnaxis)))

    validate_t = t[same_keys]

    for col in validate_t.columns.values():
        if not all(col == col[0]):
            raise ValueError(f"The {col.name} values did not all match:\n {col}")

    return table_headers


def make_sorted_table(headers, filenames):
    """
    Return an `astropy.table.Table` instance where the rows are correctly sorted.
    """
    theaders = table_from_headers(headers)
    theaders["filenames"] = filenames
    theaders["headers"] = headers
    dataset_axes = headers[0]["DNAXIS"]
    array_axes = headers[0]["DAAXES"]
    keys = [f"DINDEX{k}" for k in range(dataset_axes, array_axes, -1)]
    t = np.array(theaders[keys])
    return theaders[np.argsort(t, order=keys)]


def sort_headers(headers, filenames):
    table_headers = make_sorted_table(headers, filenames)

    validate_headers(table_headers)

    # Sort the filenames into DS order.
    sorted_filenames = np.array(table_headers["filenames"])
    sorted_headers = np.array(table_headers["headers"])

    table_headers.remove_columns(["headers", "filenames"])

    return table_headers, sorted_filenames, sorted_headers


def _inventory_from_wcs(wcs):
    """
    Parse the gWCS and extract any inventory keys needed.

    This assumes all WCSes have a celestial and temporal component.

    Keys for wavelength will not be added if there is no spectral component,
    stokes keys are always added (defaulting to just I if not in the WCS).
    """
    if not isinstance(wcs.output_frame, cf.CompositeFrame):
        raise TypeError("Can't parse this WCS as expected.")  # pragma: no cover

    bottom_left_array = [0] * wcs.pixel_n_dim
    top_right_array = np.array(wcs.array_shape) - 1

    bottom_left_world = wcs.array_index_to_world_values(*bottom_left_array)
    top_right_world = wcs.array_index_to_world_values(*top_right_array)

    time_frame = list(filter(lambda f: isinstance(f, cf.TemporalFrame), wcs.output_frame.frames))[0]
    temporal_axes = time_frame.axes_order[0] - wcs.pixel_n_dim
    temporal_unit = time_frame.unit[0]
    start_time = time_frame.reference_frame + bottom_left_world[temporal_axes] * temporal_unit
    end_time = time_frame.reference_frame + top_right_world[temporal_axes] * temporal_unit
    celestial_frame = list(filter(lambda f: isinstance(f, cf.CelestialFrame), wcs.output_frame.frames))[0]
    lon_axes = celestial_frame.axes_order[0] - wcs.pixel_n_dim
    lat_axes = celestial_frame.axes_order[1] - wcs.pixel_n_dim

    bounding_box = ((bottom_left_world[lon_axes], bottom_left_world[lat_axes]),
                    (top_right_world[lon_axes], top_right_world[lat_axes]))

    inventory = {'boundingBox': bounding_box,
                 'startTime': start_time.datetime.isoformat('T'),
                 'endTime': end_time.datetime.isoformat('T')}

    spec_frame = list(filter(lambda f: isinstance(f, cf.SpectralFrame), wcs.output_frame.frames))
    if spec_frame:
        spectral_axes = spec_frame[0].axes_order[0] - wcs.pixel_n_dim
        inventory["wavelengthMin"] = bottom_left_world[spectral_axes]
        inventory["wavelengthMax"] = top_right_world[spectral_axes]

    stokes_frame = list(filter(lambda f: isinstance(f, cf.StokesFrame), wcs.output_frame.frames))
    if stokes_frame:
        stokes_axes = stokes_frame[0].axes_order[0]
        pixel_coords = [0] * wcs.pixel_n_dim
        pixel_coords[stokes_axes] = (0, 1, 2, 3)
        all_stokes = wcs.pixel_to_world(*np.broadcast_arrays(*pixel_coords))
        stokes_components = all_stokes[stokes_axes - 1]

        inventory["stokesParameters"] = list(map(str, stokes_components))
        inventory["hasAllStokes"] = len(stokes_components) > 1

    else:
        inventory["stokesParameters"] = ['I']
        inventory["hasAllStokes"] = False

    return inventory


def _get_unique(column, singular=False):
    uniq = list(set(column))
    if singular:
        if len(uniq) == 1:
            if isinstance(uniq[0], np.str_):
                return str(uniq[0])
            return uniq[0]
        else:
            raise ValueError("Column does not result in a singular unique value")

    return uniq


def _get_number_apply(column, func):
    return func(column)


def _get_keys_matching(headers, pattern):
    """
    Get all the values from all the keys matching the given re pattern.

    Assumes that each matching column is singular (all values are the same)

    Parameters
    ----------
    headers : `astropy.table.Table`
        All the headers

    pattern : `str`
        A regex pattern
    """
    results = []

    prog = re.compile(pattern)
    for key in headers.colnames:
        if prog.match(key):
            results.append(_get_unique(headers[key], singular=True))
    return list(set(results))


def _inventory_from_headers(headers):
    inventory = {}

    mode = partial(scipy.stats.mode, axis=None, nan_policy="raise")

    # These keys might get updated by parsing the gwcs object.
    inventory["wavelengthMin"] = inventory["wavelengthMax"] = _get_unique(headers['LINEWAV'])[0]

    inventory["datasetId"] = _get_unique(headers["DSETID"], singular=True)
    inventory["exposureTime"] = _get_number_apply(headers['TEXPOSUR'], mode).mode[0]
    inventory["filterWavelengths"] = _get_unique(headers['LINEWAV'])
    inventory["instrumentName"] = _get_unique(headers['INSTRUME'], singular=True)
    inventory["recipeId"] = int(_get_unique(headers['RECIPEID'], singular=True))
    inventory["recipeInstanceId"] = int(_get_unique(headers['RINSTID'], singular=True))
    inventory["recipeRunId"] = int(_get_unique(headers['RRUNID'], singular=True))
    inventory["targetTypes"] = list(map(str, _get_unique(headers['OBJECT'])))
    inventory["primaryProposalId"] = _get_unique(headers['PROP_ID'], singular=True)
    inventory["primaryExperimentId"] = _get_unique(headers['EXPER_ID'], singular=True)
    inventory["dataset_size"] = _get_number_apply(headers['FRAMEVOL'], np.sum)
    inventory["contributingExperimentIds"] = list(map(str, (_get_keys_matching(headers, r"EXPERID\d\d$") +
                                                            [_get_unique(headers["EXPER_ID"], singular=True)])))
    inventory["contributingProposalIds"] = list(map(str, (_get_keys_matching(headers, r"PROPID\d\d$") +
                                                          [_get_unique(headers["PROP_ID"], singular=True)])))
    friedval = np.nan
    if 'FRIEDVAL' in headers.colnames:
        friedval = _get_number_apply(headers['FRIEDVAL'], np.mean)

    inventory["qualityAverageFriedParameter"] = friedval

    polacc = np.nan
    if 'POL_ACC' in headers.colnames:
        polacc = _get_number_apply(headers['POL_ACC'], np.mean)
    inventory["qualityAveragePolarimetricAccuracy"] = polacc

    return inventory


def extract_inventory(headers, transform_builder, **extra_inventory):
    """
    Generate the inventory record for an asdf file from an asdf tree.

    Parameters
    ----------
    tree : `dict`
        The incomplete asdf tree. Needs to contain the dataset object.

    transform_builder
        The thing that makes gWCSes.

    extra_inventory : `dict`
        Additional inventory keys that can not be computed from the headers or the WCS.

    Returns
    -------
    tree: `dict`
        The updated tree with the inventory.

    """
    wcs = transform_builder.gwcs
    # The headers will populate passband info for VBI and then wcs will
    # override it if there is a wavelength axis in the dataset,
    # any supplied kwargs override things extracted from dataset.
    inventory = {**_inventory_from_headers(headers), **_inventory_from_wcs(wcs), **extra_inventory}

    inventory['hasSpectralAxis'] = transform_builder.spectral_sampling is not None
    inventory['hasTemporalAxis'] = transform_builder.temporal_sampling is not None
    inventory['averageDatasetSpectralSampling'] = transform_builder.spectral_sampling
    inventory['averageDatasetSpatialSampling'] = transform_builder.spatial_sampling
    inventory['averageDatasetTemporalSampling'] = transform_builder.temporal_sampling

    instrument = inventory['instrumentName'].upper()
    start_time = datetime.datetime.fromisoformat(inventory['startTime'])
    asdf_filename = f"{instrument}_L1_{start_time:%Y%m%dT%H%M%S}_{inventory['datasetId']}.asdf"
    inventory["asdfObjectKey"] = f"{inventory['primaryProposalId']}/{inventory['datasetId']}/{asdf_filename}"

    return inventory


def generate_inventory_from_frame_inventory(bucket, json_headers):
    """
    Generate the complete inventory record from frame inventory.

    Parameters
    ----------
    bucket: `str`
        The bucket in which the dataset resides.
    json_headers : `list` of `dict
        A list of dicts containing the JSON version of the headers as stored in inventory.

    Returns
    -------
    dataset_inventory
        The complete dataset inventory
    """
    filenames, fits_headers, extra_inventory = process_json_headers(bucket, json_headers)
    table_headers, sorted_filenames, sorted_headers = sort_headers(fits_headers, filenames)

    transform_builder = TransformBuilder(sorted_headers)

    return extract_inventory(table_headers, transform_builder, **extra_inventory)
