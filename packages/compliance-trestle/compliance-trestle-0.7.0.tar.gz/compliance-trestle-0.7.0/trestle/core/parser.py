# -*- mode:python; coding:utf-8 -*-
# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Model parsing for use when models themselves must be infered and are not known.

Under most use cases trestle.core.base_model.OscalBaseModel provides functionality for loading Oscal models from files.
However, under some circumstances are unknown. Use of functionality in this module should be avoided and inspected
when used as to it's appropriateness.
"""

import importlib
import logging
import pathlib
from typing import Any, Dict, Optional

from trestle.core import const
from trestle.core.base_model import OscalBaseModel
from trestle.core.err import TrestleError
from trestle.utils import fs

logger = logging.getLogger(__name__)


def _parse_dict(data: Dict[str, Any], model_name: str) -> OscalBaseModel:
    """Load a model from the data dict.

    This functionality is provided for situations when the OSCAL data type is not known ahead of time. Here the model
    has been loaded into memory using json loads or similar and passed as a dict.

    Args:
        data: Oscal data loaded into memory in a dictionary with the `root key` removed.
        model_name: it should be of the form <module>.<class> from trestle.oscal.* modules

    Returns:
        The oscal model of the desired model.
    """
    if data is None:
        raise TrestleError('data name is required')

    if model_name is None:
        raise TrestleError('model_name is required')

    parts = model_name.split('.')
    class_name = parts.pop()
    module_name = '.'.join(parts)

    logger.debug(f'Loading class "{class_name}" from "{module_name}"')
    module = importlib.import_module(module_name)
    mclass = getattr(module, class_name)
    if mclass is None:
        raise TrestleError(f'class "{class_name}" could not be found in "{module_name}"')

    instance = mclass.parse_obj(data)
    return instance


def root_key(data: Dict[str, Any]) -> str:
    """Find root model name in the data."""
    if len(data.items()) == 1:
        return next(iter(data))

    raise TrestleError('data does not contain a root key')


def to_class_name(name: str) -> str:
    """Convert to pascal class name."""
    if name.find('-') != -1:
        parts = name.split('-')

        for i, part in enumerate(parts):
            parts[i] = part.capitalize()

        name = ''.join(parts)
        return name

    chars = list(name)
    chars[0] = chars[0].upper()
    return ''.join(chars)


def to_full_model_name(root_key: str, name: str = None) -> Optional[str]:
    """Find model name from the root_key in the file."""
    try:
        # process root key and extract model name
        module_name = root_key.lower()
        if root_key.find('-') != -1:
            parts = root_key.split('-')
            module_name = parts[0]

            for i, part in enumerate(parts):
                parts[i] = part.capitalize()

            name = ''.join(parts)

        # check for module with the root-key
        module = importlib.import_module(f'{const.PACKAGE_OSCAL}.{module_name}')

        # prepare class name
        if name is None:
            name = module_name
        class_name = to_class_name(name)

        # check if class exists in the module or not
        if getattr(module, class_name) is not None:
            return f'{const.PACKAGE_OSCAL}.{module_name}.{class_name}'
    except ModuleNotFoundError as ex:
        logger.error(f'Module {module_name} not found: {ex}')
        pass

    return None


def parse_file(file_name: pathlib.Path, model_name: Optional[str]) -> OscalBaseModel:
    """
    Load an oscal file from the file system where the oscal model type is not known.

    Args:
        file_name: File path
        model_name: it should be of the form module.class which is derived from OscalBaseModel
    """
    if file_name is None:
        raise TrestleError('file_name is required')

    data = fs.load_file(file_name)
    rkey = root_key(data)
    if model_name is None:
        model_name = to_full_model_name(rkey)
    return _parse_dict(data[rkey], model_name)
