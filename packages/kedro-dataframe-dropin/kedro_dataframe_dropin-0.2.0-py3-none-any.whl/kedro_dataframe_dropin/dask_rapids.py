"""The dask-cuDF dropin for Kedro"""
try:
    import dask_cudf  # pylint: disable=import-error
except ImportError as ex:
    raise ImportError(
        "You need to install dask-cuDF before using this dropin. "
        "See the dask-cuDF documentation at https://rapids.ai/start.html."
    ) from ex

from kedro_dataframe_dropin.core import (
    DATASET_METHOD_MAPPINGS,
    patch_datasets,
    patch_io_methods,
)

datasets = patch_datasets(dask_cudf)
for dataset_name, dataset in datasets:
    globals()[dataset_name] = (
        patch_io_methods(dataset, dask_cudf)
        if dataset_name in DATASET_METHOD_MAPPINGS
        else dataset
    )
