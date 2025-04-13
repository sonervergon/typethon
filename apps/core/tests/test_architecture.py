import ast
from pathlib import Path


def get_import_modules(file_path):
    """Extract all import statements from a Python file"""
    with open(file_path, "r") as f:
        file_content = f.read()

    tree = ast.parse(file_content)
    imports = []

    for node in ast.walk(tree):
        # Check for import statements (import x, import x.y)
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(name.name)
        # Check for from import statements (from x import y)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.append(node.module)

    return imports


def check_imports(directory, forbidden_imports, error_msg_template):
    """Helper function to check imports in a directory against forbidden ones"""
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    target_dir = project_root / directory

    # Get all Python files in the target directory
    py_files = [f for f in target_dir.glob("*.py") if f.is_file()]

    # Verify there are files to check
    assert len(py_files) > 0, f"No Python files found in the {directory} directory"

    violations = []
    for file_path in py_files:
        imports = get_import_modules(file_path)

        for forbidden_prefix in forbidden_imports:
            illegal_imports = [
                imp for imp in imports if imp.startswith(forbidden_prefix)
            ]
            if illegal_imports:
                violation = {
                    "file": file_path.name,
                    "forbidden_prefix": forbidden_prefix,
                    "imports": illegal_imports,
                }
                violations.append(violation)
                print(
                    error_msg_template.format(
                        file=file_path.name,
                        layer=forbidden_prefix,
                        imports=illegal_imports,
                    )
                )

    return violations


def test_api_layer_architecture():
    """
    Test that the API layer follows architectural boundaries by
    not importing directly from operations or models
    """
    violations = check_imports(
        directory="api",
        forbidden_imports=["operations", "models"],
        error_msg_template="File {file} directly imports from {layer} layer: {imports}",
    )

    assert (
        not violations
    ), "API layer should not import directly from operations or models layers"


def test_service_layer_architecture():
    """
    Test that the Service layer follows architectural boundaries by
    not importing directly from models layer (should use operations layer)
    """
    violations = check_imports(
        directory="services",
        forbidden_imports=["models"],
        error_msg_template="File {file} directly imports from {layer} layer: {imports}",
    )

    assert (
        not violations
    ), "Service layer should not import directly from models layer (use operations layer instead)"


def test_all_architectural_boundaries():
    """Comprehensive test of all architectural boundaries in the layered design"""
    # Define the layer boundaries
    layer_boundaries = {
        "api": [
            "operations",
            "models",
        ],  # API should not import from operations or models
        "services": ["models"],  # Services should not import from models
    }

    all_violations = []

    for layer, forbidden in layer_boundaries.items():
        violations = check_imports(
            directory=layer,
            forbidden_imports=forbidden,
            error_msg_template=f"Architectural violation in {layer}: {{file}} imports from {{layer}} layer: {{imports}}",
        )
        all_violations.extend(violations)

    # Detailed report of violations
    if all_violations:
        violation_report = "\n".join(
            [
                f"- {v['file']} imports from {v['forbidden_prefix']}: {v['imports']}"
                for v in all_violations
            ]
        )
        assert False, f"Architectural boundary violations found:\n{violation_report}"
