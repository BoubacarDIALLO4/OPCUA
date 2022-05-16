import glob
import random
from itertools import cycle
from typing import Dict, Tuple, cast, List
from pathlib import Path

import cv2
import numpy as np

from aivi import AIVI_SHARE_DIR
from aivi.pipeline.camera.abstract_camera import AbstractCamera
from aivi.tools.exception import PipelineParameterException


class FakeCamera(AbstractCamera):
    """
    This fake camera takes a given file matching and injects in the pipeline the same result as a real camera.
    Mainly use in an environment without camera or for testing purpose.

    Params:
        position (str): the camera position
        nb_shoot (int): number of picture taken
        fake_camera_mode (str): the way to select the next image to display
        fake_camera_filter (str): the file matching pattern to select images
    """
    DEFAULT_FILTER = str(AIVI_SHARE_DIR / 'default_ui/static/fakePhotos') + '**/*.[Jj][Pp][Ee][Gg]'
    AVAILABLE_MODE = {'random', 'sequence'}

    def __init__(self, pipeline_manager: 'PipelineManager', params: Dict[str, str]) -> None:
        super().__init__(pipeline_manager, params)

        self.file_names: List[str] = []
        fake_camera_filter = cast(str, self._get_str_param('fake_camera_filter', self.DEFAULT_FILTER))
        self._load_photo_names(fake_camera_filter)

        next_photo_mode = self._get_str_param('fake_camera_mode', 'random')
        if next_photo_mode not in self.AVAILABLE_MODE:
            raise PipelineParameterException(
                f'fake_camera_mode must be among {self.AVAILABLE_MODE}')
        if next_photo_mode == 'random': 
           self.next_photo == self._random_select
        else:
           self.next_photo = self._sequence_select
        self.next_sequence_image = None
         

    def _take_photo(self, index: int) -> Tuple[bytes, bytes]:
        filename = self.next_photo()
        with open(filename, 'rb') as fake_file:
            jpeg_data = fake_file.read()
            jpeg_data = np.frombuffer(jpeg_data, dtype=np.uint8)
        raw_data = cast(bytes, cv2.imdecode(jpeg_data, cv2.IMREAD_COLOR))
        return jpeg_data, raw_data

    def _load_photo_names(self, filter_regex: str) -> None:
        """
        Expands file list from the given filter matching file

        :param filter_regex: filter matching
        :return: list of path of image
        """
        for filename in sorted(list(glob.iglob(filter_regex, recursive=True))):
            self.file_names.append(filename)
        if not self.file_names:
            raise FileNotFoundError(f'No file found in {Path(filter_regex).absolute()}. '
                                    f'Update the parameter "fake_camera_filter" in params')

    def _random_select(self) -> str:
        """
        Select a random filename as the next photo for a given FakeCamera
        :return: the next photo to display
        """
        return self.file_names[random.randint(0, len(self.file_names) - 1)]

    def _sequence_select(self) -> str:
        """
        Select a next photo in the photo list as the next photo for a given FakeCamera
        :return: the next photo to display
        """
        if not self.next_sequence_image:
            self.next_sequence_image = cycle(self.file_names)
        return next(self.next_sequence_image)
