from toy_dicom_api.repos.instances import InstanceRepo
from io import BytesIO
import numpy as np
import png
from toy_dicom_api.exceptions import DicomKeyError


class InstanceSvc:
    def create_instance(self, instance_id, instance) -> None:
        InstanceRepo().create_instance(instance_id=instance_id, instance=instance)

    def get_instance_element(self, instance_id: str, group: str, element: str) -> str:
        """
        Get an element from an instance
        """
        instance = InstanceRepo().get_instance(instance_id=instance_id)
        try:
            return instance[group, element].value
        except KeyError:
            raise DicomKeyError("Group or element does not exist")

        return str(instance[group, element].value)

    def get_instance_image(self, instance_id: str) -> BytesIO:
        """
        Fetch a PNG of an instance
        """
        instance = InstanceRepo().get_instance(instance_id=instance_id)
        shape = instance.pixel_array.shape
        image_2d = instance.pixel_array.astype(float)
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)
        file_like_object = BytesIO()
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(file_like_object, image_2d_scaled)
        file_like_object.seek(0)
        return file_like_object
