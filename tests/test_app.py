from app import app


def _collect_texts(comp):
    """Recursively collect all string children from a Dash component tree."""
    texts = []
    children = getattr(comp, "children", None)
    if isinstance(children, (list, tuple)):
        for child in children:
            if isinstance(child, (str, int)):
                texts.append(str(child))
            elif child is None:
                continue
            else:
                texts.extend(_collect_texts(child))
    else:
        if isinstance(children, (str, int)):
            texts.append(str(children))
        elif children is not None:
            texts.extend(_collect_texts(children))
    return texts


def _find_by_id(comp, target_id):
    """Recursively search for a component with a specific id."""
    if getattr(comp, "id", None) == target_id:
        return True
    children = getattr(comp, "children", None)
    if isinstance(children, (list, tuple)):
        for child in children:
            if child is None:
                continue
            if isinstance(child, (str, int)):
                continue
            if _find_by_id(child, target_id):
                return True
    else:
        if children is not None and not isinstance(children, (str, int)):
            if _find_by_id(children, target_id):
                return True
    return False


def test_header_present():
    """Ensure the main header text is present in the layout."""
    texts = _collect_texts(app.layout)
    assert any("Soul Foods Pink Morsels Sales Dashboard" in t for t in texts), "Header text not found in layout"


def test_visualisation_present():
    """Ensure the main visualisation (graph) is present with id 'sales-graph'."""
    assert _find_by_id(app.layout, "sales-graph"), "Graph with id 'sales-graph' not found in layout"


def test_region_picker_present():
    """Ensure the region picker radio items are present with id 'region-radio'."""
    assert _find_by_id(app.layout, "region-radio"), "RadioItems with id 'region-radio' not found in layout"
