#  -*- coding: utf-8 -*-
#  @filename animals_web_generator.py
#  @author Marcel Bobolz
#  @last_modified 2025-03-14T14:13:44.479Z
"""write animal data into animals.html"""

from pathlib import Path
from typing import Any, Dict, List

from data_fetcher import fetch_data

Animal = Dict[str, str]


def get_html_template(html_file: str) -> str:
    """
    Loads a HTML template
    """
    path = Path(html_file)
    with path.open(encoding="utf-8") as fd:
        return fd.read()


def sanitize_animals(data: List[Dict[str, Any]]) -> List[Animal]:
    """
    Returns a sanitized list of animals from the given data.
    """
    animals: list = []
    for elem in data:
        animal = {
            "Name": elem.get("name", ""),
            "Scientific Name": elem.get("taxonomy", {}).get("scientific_name", ""),
            "Lifespan": elem.get("characteristics", {}).get("lifespan", ""),
            "Diet": elem.get("characteristics", {}).get("diet", ""),
            "Location": dict(enumerate(elem.get("locations", []))).get(0, ""),
            "Type": elem.get("characteristics", {}).get("type", ""),
        }
        animals.append(animal)
    return animals


def serialize_animal(animal: Animal) -> str:
    """
    Returns a serialized animal to a html-string.
    """
    name = f'<div class="card__title">{animal["Name"]}</div>'
    info = "\n".join(
        [  # list-item per key-value pair except "Name"
            f"<li>{key}: {value}</li>"  #
            for key, value in animal.items()
            if key != "Name" and value
        ]
    )
    return f'<li class="cards__item">{name}<p class="card__text"><ul>{info}</ul></p></li>'


def main():
    """
    Main function
    """
    work_dir = Path(__file__).parent
    animals_info: str = ""
    animal_name = input("Enter an animal's name: ")
    animals_data = fetch_data(animal_name)

    if len(animals_data) == 0:
        animals_info = (
            '<li class="cards__item"><div class="card__title error">INVALID NAME!</div>'
            '<p class="card__text">Sorry, the animal <span class="error">'
            f"{animal_name}</span> doesn't exist !</p></li>"
        )
    else:
        animals = sanitize_animals(animals_data)
        animals_info = "\n".join(serialize_animal(animal) for animal in animals)

    template_file = work_dir.joinpath("html", "animals_template.html").as_posix()
    template_html = get_html_template(template_file)

    output_file = work_dir.joinpath("html", "animals.html")
    with output_file.open("w", encoding="utf-8") as fd:
        fd.write(template_html.replace("__REPLACE_ANIMALS_INFO__", animals_info))

    print("Done.")


if __name__ == "__main__":
    main()
