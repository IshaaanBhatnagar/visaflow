import json
import os
import jinja2

templateDir = os.path.join(os.path.dirname(__file__), "templates")


def _buildPartyStyleMap(parties: list[dict]) -> dict:
    """Build a label-to-styles lookup for use in Jinja2 templates.

    Maps both the full label (e.g. "Buyer ASP") and the capitalized id
    (e.g. "Buyer") to the same style dict, so flow nodes can use either form.
    """
    styles = {}
    for party in parties:
        entry = {"bg": party["bgClass"], "text": party["textClass"]}
        styles[party["label"]] = entry
        # Also add the id (title-cased) as an alias if it differs from label
        idAlias = party["id"].title()
        if idAlias not in styles:
            styles[idAlias] = entry
    return styles


def _buildPartyColorsJson(partyStyleMap: dict) -> str:
    """Serialize partyStyleMap as JSON for JavaScript injection."""
    return json.dumps(partyStyleMap)


def _buildNodeDetailsJson(nodeDetails: dict) -> str:
    """Serialize nodeDetails dict for JS injection."""
    return json.dumps(nodeDetails)


def renderDeck(contentData: dict) -> str:
    """Render a complete pitch deck HTML from content data."""
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templateDir),
        autoescape=False,
    )

    # Compute derived template variables
    partyStyleMap = _buildPartyStyleMap(contentData.get("parties", []))
    contentData["partyStyleMap"] = partyStyleMap
    contentData["partyColorsJson"] = _buildPartyColorsJson(partyStyleMap)
    contentData["nodeDetailsJson"] = _buildNodeDetailsJson(
        contentData.get("nodeDetails", {})
    )

    template = env.get_template("base.html")
    return template.render(**contentData)


def renderDeckFromJson(jsonPath: str) -> str:
    """Render a pitch deck from a JSON config file."""
    with open(jsonPath, "r") as f:
        contentData = json.load(f)
    return renderDeck(contentData)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python renderer.py <config.json> [output.html]")
        sys.exit(1)

    configPath = sys.argv[1]
    outputPath = sys.argv[2] if len(sys.argv) > 2 else "pitchdeck_output.html"

    html = renderDeckFromJson(configPath)
    with open(outputPath, "w") as f:
        f.write(html)
    print(f"Pitch deck generated: {outputPath}")
