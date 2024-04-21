from flask import send_file, request, Response
from toy_dicom_api.services.instances import InstanceSvc
import os
from toy_dicom_api.exceptions import (
    FileExistsException,
    FileDoesNotExistException,
    DicomKeyError,
)
import connexion
import logging

absolute_path = os.path.dirname(__file__)
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config = {"data_dir": os.path.join(absolute_path, "data")}

app = connexion.FlaskApp(__name__, specification_dir="./")
app.add_api("openapi.yaml")
app.app.config["data_dir"] = os.path.join(absolute_path, "data")


def get_instance_element(instance_id: str):
    """
    Fetch a single element from an instance
    """
    group = request.args.get("group")
    element = request.args.get("element")
    log.info(
        f"get instance instance_id={instance_id}, group={group}, element = {element}"
    )
    try:
        instance_element = InstanceSvc().get_instance_element(
            instance_id=instance_id, group=group, element=element
        )
    except FileDoesNotExistException as exc:
        return Response(str(exc), 404)
    except DicomKeyError as exc:
        return Response(str(exc), 400)
    return Response(instance_element, 200)


def get_instance_image(instance_id: str):

    """
    Fetch a PNG of an instance
    """
    try:
        instance_image = InstanceSvc().get_instance_image(instance_id=instance_id)
    except FileDoesNotExistException as exc:
        return Response(str(exc), 404)
    return send_file(instance_image, mimetype="image/png")


def create_instance(instance_id: str):
    """
    Create a new instance
    """
    try:
        InstanceSvc().create_instance(instance_id=instance_id, instance=request.data)
    except FileExistsException as exc:
        return Response(str(exc), status=409)
    except Exception as exc:
        print("OMG", exc)
    return Response(None, status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
