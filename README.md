# A Toy DICOM API

This is a Python (Flask) app with three toy endpoints for interacting with DICOM files.

## Running the Application

This app is setup with `docker`, but not `docker-compose`.  Sorry about that.  Assuming docker is installed, run `docker build . -t toy_dicom_api` to build the image and `docker run -p 8000:8000 toy_dicom_api` to run it.

Swagger API docs are available at `http://localhost:8000/ui`.

Test images named `test_image_<1-3>` are included in the docker image.

* Images are at http://localhost:8000/instances/test_image_1/image
* Elements are at http://localhost:8000/instances/test_image_1?group=0010&element=0010
* Adding a new image is a POST request to http://localhost:8000/instances/foobar with the file attached as raw binary (`application/octet-stream`).  In Postman, setup your POST request and select `Body > binary > attach_file`

## Shortcuts

There are a lot of things about this toy API that relegate it to toy status:

1. The `repo` functions blindly save images to a directory within the running container, but I chose not to volume mount that directory.  This means that files are not persisted after a container restart.
2. There's no database.  The question set only required saving and retrieving specific files, so any searching was unnecessary.
3. unit test coverage is... sparse.
4. The OpenAPI documentation is sub-par.  Adding full details & examples for each schema would be helpful for any future developers.
5. The APIs deal only with instances and have no concept of a study or series.
6. There are no proper DTOs (data transfer objects).
7. There's no input sanitation beyond the OpenAPI schema validation.
8. Logs are not annotated with important information like host, pid, or container version.  That's fine in a toy application, but would need to be implemented in any productionalized deployment.
