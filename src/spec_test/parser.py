from openapi_spec_validator import validate_spec
from openapi_spec_validator.readers import read_from_filename


def load_spec(path: str):
    """Load and validate OpenAPI spec."""
    spec_dict, _ = read_from_filename(path)
    validate_spec(spec_dict)
    return spec_dict

def extract_endpoints(spec):
    """Yield (method, path, operation) for each endpoint."""
    paths = spec.get("paths", {})
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]:
                yield method.upper(), path, operation
