import json
import os


class RecipeManager:

    def __init__(self):

        self.recipe_folder = "recipes"

        os.makedirs(
            self.recipe_folder,
            exist_ok=True
        )

    def save_recipe(
        self,
        recipe_name,
        data
    ):

        path = os.path.join(
            self.recipe_folder,
            f"{recipe_name}.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def load_recipe(
        self,
        recipe_name
    ):

        path = os.path.join(
            self.recipe_folder,
            f"{recipe_name}.json"
        )

        if not os.path.exists(path):

            return None

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)