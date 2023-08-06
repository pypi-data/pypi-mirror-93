import traceback

import numpy as np
import os
import pafy
import pathlib
import typing as t

import sep.loaders
from sep._commons.movies import StreamReader
from sep._commons.utils import *
from sep.loaders.loader import Loader


class YoutubeLoader(Loader):
    """
    This one loads frames from youtube video and tags them so that can be used in processing or in dataset extraction.
    """

    def __init__(self, urls, video_quality, framerate, clips_len, clips_skip, skip_first=0, max_frames=1000000, verbose=0):
        super().__init__()
        self.verbose = verbose
        self.video_quality = video_quality
        self.max_frames = max_frames
        self.skip_first = skip_first
        self.youtube_urls = urls
        self.direct_urls = {}

        self.clips_skip = clips_skip
        self.clips_len = clips_len
        self.framerate = framerate
        self.video_image_reader: t.Optional[StreamReader] = None

        self.input_paths = {}
        self.annotation_paths = {}
        self.json_tags = {}

        for url in urls:
            youtube_video = pafy.new(url)
            streams = [v for v in youtube_video.videostreams if v.notes == video_quality and v.extension == 'mp4']
            if not streams:
                print(f"{url} has no video_quality: {video_quality} version. Skipping...")
                continue

            self.info = {'title': youtube_video.title, 'author': youtube_video.author, 'id': youtube_video.videoid}
            movie_path = streams[0].url
            movie_id = youtube_video.videoid
            movie_tag = self.info
            self.direct_urls[movie_id] = movie_path

            # Process input data movies.
            movie_frames = sep.loaders.MoviesLoader.load_movie_images(movie_path, self.framerate,
                                                                      clips_len=self.clips_len, clips_skip=self.clips_skip)
            frame_from_that_movie = 0
            left_to_skip = self.skip_first
            for frame_id, tag in zip(movie_frames['images'], movie_frames['tags']):
                if left_to_skip > 0:
                    left_to_skip -= 1
                    continue
                if frame_from_that_movie >= self.max_frames:
                    continue
                frame_path = f"{movie_path}{frame_id}"
                frame_id = f"{movie_id}{frame_id}"
                tag['id'] = frame_id
                update_with_suffix(tag, movie_tag, prefix=sep.loaders.MoviesLoader.MOVIE_TAG_PREFIX)

                self.input_paths[frame_id] = frame_path
                self.json_tags[frame_id] = tag
                frame_from_that_movie += 1

        self.input_order = sorted(self.input_paths.keys())

    def list_movies(self):
        return self.direct_urls.keys()

    def list_movies_paths(self):
        return self.direct_urls.values()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self.close()

    def close(self):
        if self.video_image_reader:
            self.video_image_reader.close()
            self.video_image_reader = None

    def list_images_paths(self):
        return [self.input_paths[p] for p in self.input_order]

    def list_images(self):
        return list(self.input_order)

    def __get_frame_path(self, path_set, name_or_num):
        if isinstance(name_or_num, int):
            name_or_num = self.input_order[name_or_num]
        if isinstance(name_or_num, str):
            return path_set.get(name_or_num, None)
        else:
            raise NotImplemented(type(name_or_num))

    def load_image(self, name_or_num) -> np.ndarray:
        path_to_frame = self.__get_frame_path(self.input_paths, name_or_num)
        if path_to_frame is None:
            raise Exception(f"{name_or_num} does not exist in the loader.")
        path_to_movie, frame_nr = path_to_frame.rsplit("_", maxsplit=1)
        self.video_image_reader = sep.loaders.MoviesLoader.prepare_reader(self.video_image_reader, path_to_movie)
        return self.video_image_reader[int(frame_nr)]

    def load_tag(self, name_or_num):
        if isinstance(name_or_num, int):
            name_or_num = self.input_order[name_or_num]
        return self.json_tags.get(name_or_num, None)

    def load_annotation(self, name_or_num) -> t.Optional[pathlib.Path]:
        path_to_frame = self.__get_frame_path(self.annotation_paths, name_or_num)
        if path_to_frame is None:
            return None
        # TODO read from reader
        path_to_movie, frame_nr = path_to_frame.rsplit("_", maxsplit=1)

        return None

    def get_relative_path(self, name_or_num):
        if isinstance(name_or_num, int):
            name_or_num = self.input_order[name_or_num]
        youtube_id = self.load_tag(name_or_num)['movie_id']
        return os.path.join(youtube_id, name_or_num)

    def __str__(self):
        return f"YoutubeLoader for: {self.youtube_urls}"
