import spb_label
import json
import urllib
import os

from spb_label.image_sdk import DataHandle
from spb_label.utils.utils import requests_retry_session
from spb_label.exceptions import (
    NotSupportedException,
)
from spb_label.utils import (
    deprecated,
    retrieve_file,
)


class VideoDataHandle(DataHandle):
    def _upload_to_suite(self, info=None):
        command = spb_label.Command(type="update_videolabel")
        if info is None:
            _ = spb_label.run(command=command, option=self._data)
        else:
            _ = spb_label.run(
                command=command,
                option=self._data,
                optional={"info": json.dumps(info)},
            )

    ##############################
    # Immutable variables
    ##############################
    def get_image_url(self):
        raise NotSupportedException("The video data does not support get_image_url.")

    def get_frame_url(self, idx, data_url=None):
        self._describe_data_detail()
        if self._is_expired_url():
            return None

        if data_url is None:
            data_url = json.loads(self._data.data_url)
        
        if type(data_url) is list:
            return data_url[idx]
        else:
            file_ext = data_url["file_infos"][idx]["file_name"].split(".")[-1].lower()
            file_name = f"image_{(idx+1):08}.{file_ext}"
            return f"{data_url['base_url']}{file_name}?{data_url['query']}"

    def get_frame_urls(self):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        if self._data.data_url is None:
            return None

        data_url = json.loads(self._data.data_url)

        if type(data_url) is list:
            for frame_idx in range(len(data_url)):
                yield self.get_frame_url(frame_idx, data_url)
        else:
            for frame_idx in range(len(data_url["file_infos"])):
                yield self.get_frame_url(frame_idx, data_url)

    def get_frame(self, idx):
        return self.get_frame_url(idx)

    ##############################
    # Simple SDK functions
    ##############################

    def download_image(self, download_to=None, print_log=False):
        raise NotSupportedException(
            "Does not support download label image."
        )

    def get_image(self):
        raise NotSupportedException(
            "Does not support describe label image."
        )

    def download_video(self, download_to=None, print_log=False):
        self._describe_data_detail()
        if self._is_expired_url():
            return None
        if self._data.data_url is None:
            return None

        if download_to is None:
            download_to = self._data.data_key
            if print_log:
                print("[INFO] Downloaded to {}".format(download_to))

        data_url = json.loads(self._data.data_url)
        if type(data_url) is list:
            for frame_idx in range(len(data_url)):
                url = self.get_frame_url(frame_idx, data_url)
                try:
                    parts = url.split("://", 1)
                    if len(parts) < 2:
                        raise ValueError("Invalid URL format: missing '://' separator")

                    path_parts = parts[1].split("/", 2)
                    if len(path_parts) < 3:
                        raise ValueError("Invalid URL format: insufficient '/' parts for path extraction")

                    url_path = path_parts[2].split("?", 1)[0]

                except ValueError as e:
                    raise ValueError("Invalid URL format")
                retrieve_file(
                    url=url,
                    file_path=os.path.join(download_to, url_path)
                )
        else:
            for frame_idx, file_info in enumerate(data_url["file_infos"]):
                url = self.get_frame_url(frame_idx, data_url)
                retrieve_file(
                    url=url,
                    file_path=os.path.join(download_to, file_info["file_name"])
                )
        return True

    def get_frames(self):
        for url in self.get_frame_urls():
            yield url

    def add_object_label(self, class_name, annotation, properties=None, id=None):
        raise NotSupportedException("Does not support add_object_label. Use set_object_labels instead.")

    @deprecated("Use [update_info] or [update_tag]")
    def update_data(self):
        self._upload_to_suite(info={"tags": self._data.get("result", {})["tags"]})
        with requests_retry_session() as session:
            _ = session.put(
                self._data.info_write_presigned_url,
                data=json.dumps(self._data.result),
            )
        self.label_id_only = False
        return True

    @deprecated("Use [update_tags].")
    def set_tags(self, tags: list = None):
        raise NotSupportedException("[ERROR] Video does not supported.")

    def set_category_labels(
        self, properties=None, frames=None
    ):
        self._label_build_params.set_categories(
            properties=properties,
            frames=frames,
        )
        info = self._label_build_params.build_info()
        categories = {"properties": [], "frames": []}
        if "result" in info and "categories" in info["result"]:
            categories = info["result"]["categories"]
        self._data.result = {
            **(self._data.result or {}),
            "categories": categories,
        }
