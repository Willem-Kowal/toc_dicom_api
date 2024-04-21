import os
from toy_dicom_api.exceptions import FileExistsException, FileDoesNotExistException
from flask import current_app

from pydicom import dcmread


class InstanceRepo:
    def create_instance(self, instance_id: str, instance) -> None:
        """
        Totally legit and super-secure method of saving files to disk
        """

        path = os.path.join(current_app.config.get("data_dir"), instance_id)
        print("HERE", path)
        if os.path.isfile(path):
            raise FileExistsException("An instance with that id already exists")

        with open(path, "wb") as f:
            f.write(instance)
            f.close()

    def get_instance(self, instance_id: str):
        """
        Retrieve a single instance.
        """
        path = os.path.join(current_app.config.get("data_dir"), instance_id)
        print("path", path)
        if not os.path.isfile(path):
            raise FileDoesNotExistException("An instance with that id does not exist")
        return dcmread(path)
