# -*- coding: utf-8 -*-
"""
Functions for mapping AHBA microarray dataset to atlases and and parcellations
"""

from functools import reduce

import nibabel as nib
import numpy as np
import pandas as pd

from . import correct, datasets, io, probes_, samples_, utils
from .utils import first_entry, flatten_dict

import logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
lgr = logging.getLogger('abagen')
lgr_levels = dict(zip(range(3), [40, 20, 10]))


def get_expression_data(atlas,
                        atlas_info=None,
                        *,
                        ibf_threshold=0.5,
                        probe_selection='diff_stability',
                        donor_probes='aggregate',
                        lr_mirror=False,
                        exact=True,
                        tolerance=2,
                        sample_norm='srs',
                        gene_norm='srs',
                        norm_matched=True,
                        region_agg='donors',
                        agg_metric='mean',
                        corrected_mni=True,
                        reannotated=True,
                        return_counts=False,
                        return_donors=False,
                        donors='all',
                        data_dir=None,
                        verbose=1,
                        n_proc=1):
    """
    Assigns microarray expression data to ROIs defined in `atlas`

    This function aims to provide a workflow for generating pre-processed,
    microarray expression data from the Allen Human Brain Atlas ([A2]_) for
    abitrary `atlas` designations. First, some basic filtering of genetic
    probes is performed, including:

        1. Intensity-based filtering of microarray probes to remove probes that
           do not exceed a certain level of background noise (specified via the
           `ibf_threshold` parameter), and
        2. Selection of a single, representative probe (or collapsing across
           probes) for each gene, specified via the `probe_selection`
           parameter.

    Tissue samples are then matched to parcels in the defined `atlas` for each
    donor. If `atlas_info` is provided then this matching is constrained by
    both hemisphere and tissue class designation (e.g., cortical samples from
    the left hemisphere are only matched to ROIs in the left cortex,
    subcortical samples from the right hemisphere are only matched to ROIs in
    the left subcortex); see the `atlas_info` parameter description for more
    information.

    Matching of microarray samples to parcels in `atlas` is done via a multi-
    step process:

        1. Determine if the sample falls directly within a parcel,
        2. Check to see if there are nearby parcels by slowly expanding the
           search space to include nearby voxels, up to a specified distance
           (specified via the `tolerance` parameter),
        3. If there are multiple nearby parcels, the sample is assigned to the
           closest parcel, as determined by the parcel centroid.

    If at any step a sample can be assigned to a parcel the matching process is
    terminated. If multiple sample are assigned to the same parcel they are
    aggregated with the metric specified via the `metric` parameter. More
    control over the sample matching can be obtained by setting the `exact`
    parameter; see the parameter description for more information.

    Once all samples have been matched to parcels for all supplied donors, the
    microarray expression data are optionally normalized via the provided
    `sample_norm` and `gene_norm` functions before being combined within
    parcels and across donors via the supplied `agg_metric`.

    Parameters
    ----------
    atlas : niimg-like object or dict
        A parcellation image in MNI space, where each parcel is identified by a
        unique integer ID. Alternatively, a dictionary where keys are donor IDs
        and values are parcellation images in the native space of each donor.
    atlas_info : os.PathLike or pandas.DataFrame, optional
        Filepath to or pre-loaded dataframe containing information about
        `atlas`. Must have at least columns 'id', 'hemisphere', and 'structure'
        containing information mapping atlas IDs to hemisphere (i.e, "L", "R")
        and broad structural class (i.e., "cortex", "subcortex", "cerebellum").
        If provided, this will constrain matching of tissue samples to regions
        in `atlas`. Default: None
    ibf_threshold : [0, 1] float, optional
        Threshold for intensity-based filtering. This number specifies the
        ratio of samples, across all supplied donors, for which a probe must
        have signal significantly greater background noise in order to be
        retained. Default: 0.5
    probe_selection : str, optional
        Selection method for subsetting (or collapsing across) probes that
        index the same gene. Must be one of 'average', 'max_intensity',
        'max_variance', 'pc_loading', 'corr_variance', 'corr_intensity', or
        'diff_stability', 'rnaseq'; see Notes for more information on different
        options. Default: 'diff_stability'
    donor_probes : str, optional
        Whether specified `probe_selection` method should be performed with
        microarray data from all donors ('aggregate'), independently for each
        donor ('independent'), or based on the most common selected probe
        across donors ('common'). Not all combinations of `probe_selection`
        and `donor_probes` methods are viable. Default: 'aggregate'
    lr_mirror : bool, optional
        Whether to mirror microarray expression samples across hemispheres to
        increase spatial coverage. This will duplicate samples across both
        hemispheres (i.e., L->R and R->L), approximately doubling the number of
        available samples. Default: False
    exact : bool, optional
        Whether to use exact matching of donor tissue samples to parcels in
        `atlas`. If True, this function will ONLY match tissue samples to
        parcels within `threshold` mm of the sample; any samples that are
        beyond `threshold` mm of a parcel will be discarded. This may result
        in some parcels having no assigned sample / expression data. If False,
        the default matching procedure will be performed and followed by a
        check for parcels with no assigned samples; any such parcels will be
        matched to the nearest sample (defined as the sample with the closest
        Euclidean distance to the parcel centroid). Default: True
    tolerance : int, optional
        Distance (in mm) that a sample must be from a parcel for it to be
        matched to that parcel. This is only considered if the sample is not
        directly within a parcel. Default: 2
    sample_norm : {'rs', 'srs', 'minmax', 'center', 'zscore', None}, optional
        Method by which to normalize microarray expression values for each
        sample. Expression values are normalized separately for each sample and
        donor across all genes; see Notes for more information on different
        methods. If None is specified then no normalization is performed.
        Default: 'srs'
    gene_norm : {'rs', 'srs', 'minmax', 'center', 'zscore', None}, optional
        Method by which to normalize microarray expression values for each
        donor. Expression values are normalized separately for each gene and
        donor across all samples; see Notes for more information on different
        methods. If None is specified then no normalization is performed.
        Default: 'srs'
    norm_matched : bool, optional
        Whether to perform gene normalization (`gene_norm`) across only those
        samples matched to regions in `atlas` instead of all available samples.
        If `atlas` is very small (i.e., only a few regions of interest), using
        `norm_matched=False` is suggested. Default: True
    region_agg : {'samples', 'donors'}, optional
        When multiple samples are identified as belonging to a region in
        `atlas` this determines how they are aggegated. If 'samples',
        expression data from all samples for all donors assigned to a given
        region are combined. If 'donors', expression values for all samples
        assigned to a given region are combined independently for each donor
        before being combined across donors. See `agg_metric` for mechanism by
        which samples are combined. Default: 'donors'
    agg_metric : {'mean', 'median'} or callable, optional
        Mechanism by which to reduce sample-level expression data into region-
        level expression (see `region_agg`). If a callable, should be able to
        accept an `N`-dimensional input and the `axis` keyword argument and
        return an `N-1`-dimensional output. Default: 'mean'
    corrected_mni : bool, optional
        Whether to use the "corrected" MNI coordinates shipped with the
        `alleninf` package instead of the coordinates provided with the AHBA
        data when matching tissue samples to anatomical regions. Default: True
    reannotated : bool, optional
        Whether to use reannotated probe information provided by [A1]_ instead
        of the default probe information from the AHBA dataset. Using
        reannotated information will discard probes that could not be reliably
        matched to genes. Default: True
    return_counts : bool, optional
        Whether to return dataframe containing information on how many samples
        were assigned to each parcel in `atlas` for each donor. Default: False
    return_donors : bool, optional
        Whether to return donor-level expression arrays instead of aggregating
        expression across donors with provided `agg_metric`. Default: False
    donors : list, optional
        List of donors to use as sources of expression data. Can be either
        donor numbers or UID. If not specified will use all available donors.
        Note that donors '9861' and '10021' have samples from both left + right
        hemispheres; all other donors have samples from the left hemisphere
        only. Default: 'all'
    data_dir : os.PathLike, optional
        Directory where expression data should be downloaded (if it does not
        already exist) / loaded. If not specified will use the current
        directory. Default: None
    verbose : int, optional
        Specifies verbosity of status messages to display during workflow.
        Higher numbers increase verbosity of messages while zero suppresses all
        messages. Default: 1
    n_proc : int, optional
        Number of processors to use to download AHBA data. Can parallelize up
        to six times. Default: 1

    Returns
    -------
    expression : (R, G) pandas.DataFrame
        Microarray expression for `R` regions in `atlas` for `G` genes,
        aggregated across donors, where the index corresponds to the unique
        integer IDs of `atlas` and the columns are gene names. If
        ``return_donors=True`` then this is a list of (R, G) dataframes, one
        for each donor.
    counts : (R, D) pandas.DataFrame
        Number of samples assigned to each of `R` regions in `atlas` for each
        of `D` donors (if multiple donors were specified); only returned if
        ``return_counts=True``.

    Notes
    -----
    The following methods can be used for collapsing across probes when
    multiple probes are available for the same gene:

        1. ``probe_selection='average'``

        Takes the average of expression data across all probes indexing the
        same gene. Providing 'mean' as the input method will return the same
        thing. This method can only be used when `donor_probes='aggregate'`.

        2. ``probe_selection='max_intensity'``

        Selects the probe with the maximum average expression across samples
        from all donors.

        3. ``probe_selection='max_variance'``

        Selects the probe with the maximum variance in expression across
        samples from all donors.

        4. ``probe_selection='pc_loading'``

        Selects the probe with the maximum loading along the first principal
        component of a decomposition performed across samples from all donors.

        5. ``probe_selection='corr_intensity'``

        Selects the probe with the maximum correlation to other probes from the
        same gene when >2 probes exist; otherwise, uses the same procedure as
        `max_intensity`.

        6. ``probe_selection='corr_variance'``

        Selects the probe with the maximum correlation to other probes from the
        same gene when >2 probes exist; otherwise, uses the same procedure as
        `max_varance`.

        7. ``probe_selection='diff_stability'``

        Selects the probe with the most consistent pattern of regional
        variation across donors (i.e., the highest average correlation across
        brain regions between all pairs of donors). This method can only be
        used when `donor_probes='aggregate'`.

        8. ``method='rnaseq'``

        Selects probes with most consistent pattern of regional variation to
        RNAseq data (across the two donors with RNAseq data). This method can
        only be used when `donor_probes='aggregate'`.

    Note that for incompatible combinations of `probe_selection` and
    `donor_probes` (as detailed above), the `probe_selection choice will take
    precedence. For example, providing ``probe_selection='diff_stability'`` and
    ``donor_probes='independent'`` will cause `donor_probes` to be reset to
    `'aggregate'`.

    The following methods can be used for normalizing microarray expression
    values prior to aggregating:

        1. ``{sample,gene}_norm=='rs'``

        Uses a robust sigmoid function as in [A3]_ to normalize values

        2. ``{sample,gene}_norm='srs'``

        Same as 'rs' but scales output to the unit normal (i.e., range 0-1)

        3. ``{sample,gene}_norm='minmax'``

        Scales data to the unit normal (i.e., range 0-1)

        4. ``{sample,gene}_norm='center'``

        Removes the mean of expression values

        5. ``{sample,gene}_norm='zscore'``

        Applies a basic z-score (subtract mean, divide by standard deviation);
        uses degrees of freedom equal to one for standard deviation

    References
    ----------
    .. [A1] Arnatkevic̆iūtė, A., Fulcher, B. D., & Fornito, A. (2019). A
       practical guide to linking brain-wide gene expression and neuroimaging
       data. NeuroImage, 189, 353-367.
    .. [A2] Hawrylycz, M.J. et al. (2012) An anatomically comprehensive atlas
       of the adult human transcriptome. Nature, 489, 391-399.
    .. [A3] Fulcher, B. D., & Fornito, A. (2016). A transcriptional signature
       of hub connectivity in the mouse connectome. Proceedings of the National
       Academy of Sciences, 113(5), 1435-1440.
    """

    # set logging verbosity level
    lgr.setLevel(lgr_levels.get(int(verbose), 1))

    # load atlas and atlas_info, if provided, and coerce to dict
    atlas, atlas_info, same = coerce_atlas_to_dict(atlas, donors, atlas_info)

    # get combination functions
    agg_metric = utils.check_metric(agg_metric)

    # check probe_selection input
    if probe_selection not in probes_.SELECTION_METHODS:
        raise ValueError('Provided probe_selection method is invalid, must be '
                         f'one of {list(probes_.SELECTION_METHODS)}. Received '
                         f'value: \'{probe_selection}\'')
    if donor_probes not in ['aggregate', 'independent', 'common']:
        raise ValueError('Provided donor_probes method is invalid, must be '
                         f'one of [\'aggregate\', \'independent\']. Received '
                         f'value: \'{donor_probes}\'')

    # fetch files (downloading if necessary) and unpack to variables
    files = datasets.fetch_microarray(data_dir=data_dir, donors=donors,
                                      verbose=verbose, n_proc=n_proc)

    if probe_selection == 'diff_stability' and len(files) == 1:
        raise ValueError('Cannot use diff_stability for probe_selection with '
                         'only one donor. Please specify a different probe_'
                         'selection method or use more donors.')
    elif probe_selection == 'rnaseq':  # fetch RNAseq if we're gonna need it
        datasets.fetch_rnaseq(data_dir=data_dir, donors=donors,
                              verbose=verbose)

    # get some info on labels in `atlas_img`
    all_labels = utils.get_unique_labels(utils.first_entry(atlas))
    n_gb = (8 * len(all_labels) * 30000) / (1024 ** 3)
    if n_gb > 1:
        lgr.warning(f'Output region x gene matrix may require up to {n_gb:.2f}'
                    'GB RAM.')
    if not exact and same:
        lgr.info(f'Pre-calculating centroids for {len(all_labels)} regions in '
                 'provided atlas')
        centroids = utils.get_centroids(utils.first_entry(atlas),
                                        labels=all_labels,
                                        image_space=True)

    # update the annotation "files". this handles updating the MNI coordinates,
    # dropping mistmatched samples (where MNI coordinates don't match the
    # provided ontology), and mirroring samples across hemispheres, if desired
    for donor, data in files.items():
        annot, ontol = data['annotation'], data['ontology']
        t1w = None
        if not same:
            t1w = datasets.fetch_raw_mri(donors=donor,
                                         data_dir=data_dir,
                                         verbose=verbose)[donor]['t1w']
        annot = samples_.update_coords(annot, corrected_mni=corrected_mni,
                                       native_space=t1w)
        annot = samples_.drop_mismatch_samples(annot, ontol)
        if lr_mirror:
            annot = samples_.mirror_samples(annot, ontol)
        data['annotation'] = annot
    annotation = flatten_dict(files, 'annotation')

    # get dataframe of probe information (reannotated or otherwise)
    # the Probes.csv files are the same for every donor so just grab the first
    probe_info = io.read_probes(first_entry(files, 'probes'))
    if reannotated:
        probe_info = probes_.reannotate_probes(probe_info)

    # drop probes with no/invalid Entrez ID
    probe_info = probe_info.dropna(subset=['entrez_id'])

    # intensity-based filtering of probes
    probe_info = probes_.filter_probes(flatten_dict(files, 'pacall'),
                                       annotation, probe_info,
                                       threshold=ibf_threshold)

    # get probe-reduced microarray expression data for all donors based on
    # selection method; this will be a list of gene x sample dataframes (one
    # for each donor)
    microarray = probes_.collapse_probes(flatten_dict(files, 'microarray'),
                                         annotation, probe_info,
                                         method=probe_selection,
                                         donor_probes=donor_probes)
    missing = []
    counts = pd.DataFrame(np.zeros((len(all_labels) + 1, len(microarray)),
                                   dtype=int),
                          index=np.append([0], all_labels),
                          columns=microarray.keys())
    for subj in microarray:
        if lr_mirror:  # reset index (duplicates will cause issues if we don't)
            # TODO: come up with alternative sample IDs for mirrored samples
            annotation[subj] = annotation[subj].reset_index(drop=True)
            microarray[subj] = microarray[subj].reset_index(drop=True)

        # assign samples to regions
        labels = samples_.label_samples(annotation[subj], atlas[subj],
                                        atlas_info, tolerance=tolerance)

        # if we're doing exact matching and want to aggregate samples w/i
        # regions, remove the non-labelled samples prior to normalization.
        # otherwise, we'll remove the non-labelled samples after normalization
        nz = np.asarray(labels != 0).squeeze()
        if norm_matched:
            microarray[subj] = microarray[subj].loc[nz]
            annotation[subj] = annotation[subj].loc[nz]
            labels = labels.loc[nz]

        if sample_norm is not None:
            microarray[subj] = correct.normalize_expression(microarray[subj].T,
                                                            norm=sample_norm,
                                                            ignore_warn=True).T
        if gene_norm is not None:
            microarray[subj] = correct.normalize_expression(microarray[subj],
                                                            norm=gene_norm,
                                                            ignore_warn=True)

        # get counts of samples collapsed into each ROI
        labs, num = np.unique(labels, return_counts=True)
        counts.loc[labs, subj] = num
        lgr.info(f'{counts.iloc[1:][subj].sum():>3} / {len(nz)} '
                 f'samples matched to regions for donor #{subj}')

        # if we don't want to do exact matching then cache which parcels are
        # missing data and the expression data for the closest sample to that
        # parcel; we'll use this once we've iterated through all donors
        if not exact:
            if not same:
                centroids = utils.get_centroids(atlas[subj], labels=all_labels,
                                                image_space=True)
            empty = np.logical_not(np.in1d(all_labels, labs))
            cols = ['mni_x', 'mni_y', 'mni_z']
            idx, dist = utils.closest_centroid(annotation[subj][cols],
                                               centroids[empty],
                                               return_dist=True)
            if not hasattr(idx, '__len__'):  # TODO: better way to check this?
                idx, dist = np.array([idx]), np.array([dist])
            idx = microarray[subj].loc[annotation[subj].iloc[idx].index]
            empty = all_labels[empty]
            idx.index = pd.Series(empty, name='label')
            missing += [(idx, dict(zip(empty, np.diag(dist))))]

        microarray[subj].index = labels['label']

    if not exact:  # check for missing ROIs and fill in, as needed
        # labels that are missing across all donors
        empty = reduce(set.intersection, [set(f.index) for f, d in missing])
        lgr.info(f'Matching {len(empty)} regions w/no data to nearest samples')
        for roi in empty:
            # find donor with sample closest to centroid of empty parcel
            ind = np.argmin([dist.get(roi) for micro, dist in missing])
            subj = list(microarray.keys())[ind]
            lgr.debug(f'Assigning sample from donor {subj} to region #{roi}')
            # assign expression data from that sample and add to count
            exp = missing[ind][0].loc[roi]
            microarray[subj] = microarray[subj].append(exp)
            counts.loc[roi, subj] += 1

    # if we don't want to aggregate over regions return voxel-level results
    if region_agg is None:
        # don't return samples that aren't matched to a region in the `atlas`
        mask = {d: m.index != 0 for d, m in microarray.items()}
        microarray = pd.concat([m[mask[d]] for d, m in microarray.items()])
        # set index to well_id for all remaining tissue samples
        microarray.index = pd.Series(np.asarray(
            pd.concat([a[mask[d]] for d, a in annotation.items()])['well_id']
        ), name='well_id')
        # return expression data (remove NaNs)
        return microarray.dropna(axis=1, how='any')

    microarray = samples_.aggregate_samples(microarray.values(),
                                            labels=all_labels,
                                            region_agg=region_agg,
                                            agg_metric=agg_metric,
                                            return_donors=return_donors)

    # drop the "zero" label from the counts dataframe (this is background)
    if return_counts:
        return microarray, counts.iloc[1:]

    return microarray


def get_samples_in_mask(mask=None, **kwargs):
    """
    Returns preprocessed microarray expression data for samples in `mask`

    Uses the same processing workflow as :func:`abagen.get_expression_data` but
    instead of aggregating samples within regions simply returns sample-level
    expression data for all samples that fall within boundaries of `mask`.

    Parameters
    ----------
    mask : niimg-like object, optional
        A mask image in MNI space (where 0 is the background). Alternatively, a
        dictionary where keys are donor IDs and values are mask images in the
        native space of each donor. If not supplied, all available samples will
        be returned. Default: None
    kwargs : key-value pairs
        All key-value pairs from :func:`abagen.get_expression_data` except for:
        `atlas`, `atlas_info`, `region_agg`, and `agg_metric`, which will be
        ignored. If `atlas` is supplied instead of `mask` then `atlas` will be
        used instead as a modified binary image. If both `atlas` and `mask` are
        supplied then `mask` will be usedin

    Returns
    -------
    expression : (S, G) pandas.DataFrame
        Microarray expression for `S` samples for `G` genes, aggregated across
        donors, where the columns are gene names
    coords : (S,) numpy.ndarray
        MNI coordinates of samples in `expression`. Even if donor-specific
        masks are provided MNI coordinates will be returned to ensure
        comparability between subjects
    """

    # fetch files (downloading if necessary) to get coordinates
    files = datasets.fetch_microarray(data_dir=kwargs.get('data_dir', None),
                                      donors=kwargs.get('donors', 'all'),
                                      verbose=kwargs.get('verbose', 1),
                                      n_proc=kwargs.get('n_proc', 1))

    # get updated coordinates
    for donor, data in files.items():
        annot, ontol = data['annotation'], data['ontology']
        if kwargs.get('corrected_mni', True):
            annot = samples_.update_mni_coords(annot)
        annot = samples_.drop_mismatch_samples(annot, ontol)
        if kwargs.get('lr_mirror', False):
            annot = samples_.mirror_samples(annot, ontol)
        data['annotation'] = annot
    cols = ['well_id', 'mni_x', 'mni_y', 'mni_z']
    coords = np.asarray(pd.concat(flatten_dict(files, 'annotation'))[cols])
    well_id, coords = np.asarray(coords[:, 0], 'int'), coords[:, 1:]

    # in case people mix things up and use atlas instead of mask, use that
    if kwargs.get('atlas') is not None and mask is None:
        mask = kwargs['atlas']
    elif mask is None:
        # create affine for "full" mask
        affine = np.eye(4)
        affine[:-1, -1] = np.floor(coords).min(axis=0)

        # downsample coordinates to specified resolution and convert to ijk
        ijk = np.unique(
            np.asarray(
                np.floor(
                    nib.affines.apply_affine(np.linalg.inv(affine), coords),
                ), dtype='int'
            ), axis=0
        )

        # generate atlas image where each voxel has
        img = np.zeros(ijk.max(axis=0) + 2, dtype='int')
        img[tuple(map(tuple, ijk.T))] = 1
        mask = nib.Nifti1Image(img, affine=affine)

    # reset these parameters
    kwargs['atlas'] = mask
    kwargs['atlas_info'] = None
    kwargs['region_agg'] = None
    # soft reset this parameter
    kwargs.setdefault('norm_matched', False)

    # get expression data + drop sample coordinates that weren't in atlas
    exp = get_expression_data(**kwargs)
    coords = coords[np.isin(well_id, exp.index)]

    return exp, coords


def coerce_atlas_to_dict(atlas, donors, atlas_info=None):
    """
    Coerces `atlas` to dict with keys `donors`

    If already a dictionary, confirms that `atlas` has entries for all values
    in `donors`

    Parameters
    ----------
    atlas : niimg-like object
        A parcellation image in MNI space, where each parcel is identified by a
        unique integer ID
    donors : array_like
        Donors that should have entries in returned `atlas` dictionary
    atlas_info : os.PathLike or pandas.DataFrame, optional
        Filepath to or pre-loaded dataframe containing information about
        `atlas`. Must have at least columns 'id', 'hemisphere', and 'structure'
        containing information mapping atlas IDs to hemisphere (i.e, "L", "R")
        and broad structural class (i.e., "cortex", "subcortex", "cerebellum").
        If provided, this will constrain matching of tissue samples to regions
        in `atlas`. Default: None

    Returns
    -------
    atlas : dict
        Dict where keys are `donors` and values are `atlas`. If a dict was
        provided it is checked to ensure
    atlas_info : pandas.DataFrame
        Loaded dataframe with information on atlas
    same : bool
        Whether one atlas was provided for all donors (True) instead of
        donor-specific atlases (False)
    """

    donors = datasets.fetchers.check_donors(donors)
    same = True

    # FIXME: so that we're not depending on type checks so much :grimacing:
    if isinstance(atlas, dict):
        atlas = {
            datasets.WELL_KNOWN_IDS.subj[d]: utils.check_img(a)
            for d, a in atlas.items()
        }
        same = False
        missing = set(donors) - set(atlas)
        if len(missing) > 0:
            raise ValueError('Provided `atlas` does not have entry for all '
                             f'requested donors. Missing donors: {donors}.')
        lgr.info('Donor-specific atlases provided; using native MRI '
                 'coordinates for tissue samples')
    else:
        atlas = utils.check_img(atlas)
        atlas = {donor: atlas for donor in donors}
        lgr.info('Group-level atlas provided; using MNI coordinates for '
                 'tissue samples')

    if atlas_info is not None:
        for donor, atl in atlas.items():
            atlas_info = utils.check_atlas_info(atlas[donor], atlas_info)

    return atlas, atlas_info, same
