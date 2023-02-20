"""Alchemy."""


class AlchemicalElement:
    """
    AlchemicalElement class.

    Every element must have a name.
    """

    def __init__(self, name: str) -> None:
        """Initialize class."""
        self.name = name

    def __repr__(self) -> str:
        """Represent class."""
        return f"<AE: {self.name}>"


class AlchemicalStorage:
    """AlchemicalStorage class."""

    def __init__(self):
        """
        Initialize the AlchemicalStorage class.

        You will likely need to add something here, maybe a list?
        """
        self.storage = []

    def add(self, element: AlchemicalElement):
        """
        Add element to storage.

        Check that the element is an instance of AlchemicalElement, if it is not, raise the built-in TypeError exception.

        :param element: Input object to add to storage.
        """
        if isinstance(element, AlchemicalElement):
            self.storage.append(element)
        else:
            raise TypeError

    def pop(self, element_name: str):
        """
        Remove and return previously added element from storage by its name.

        If there are multiple elements with the same name, remove only the one that was added most recently to the
        storage. If there are no elements with the given name, do not remove anything and return None.

        :param element_name: Name of the element to remove.
        :return: The removed AlchemicalElement object or None.
        """
        for i in range(len(self.storage) - 1, -1, -1):
            if self.storage[i].name == element_name:
                return self.storage.pop(i)
        return None

    def extract(self) -> list[AlchemicalElement]:
        """
        Return a list of all of the elements from storage and empty the storage itself.

        Order of the list must be the same as the order in which the elements were added.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            storage.extract() # -> [<AE: Water>, <AE: Fire>]
            storage.extract() # -> []

        In this example, the second time we use .extract() the output list is empty because we already extracted everything.

        :return: A list of all of the elements that were previously in the storage.
        """
        ret = self.storage
        self.storage = []
        return ret

    def get_content(self) -> str:
        """
        Return a string that gives an overview of the contents of the storage.

        Example:
            storage = AlchemicalStorage()
            storage.add(AlchemicalElement('Water'))
            storage.add(AlchemicalElement('Fire'))
            print(storage.get_content())

        Output in console:
            Content:
             * Fire x 1
             * Water x 1

        The elements must be sorted alphabetically by name.

        :return: Content as a string.
        """
        dic = dict()
        for element in self.storage:
            dic[element.name] = dic.get(element.name, 0) + 1
        lst = []
        for key in dic:
            lst.append(f"* {key} x {dic[key]}")
        ret = "Content:\n "
        if len(lst) > 0:
            ret += "\n ".join(sorted(lst))
        else:
            ret += "Empty."
        return ret


class AlchemicalRecipes:
    """AlchemicalRecipes class."""

    def __init__(self):
        """
        Initialize the AlchemicalRecipes class.

        Add whatever you need to make this class function.
        """
        self.recipes = dict()
        self.reverse_recipes = dict()

    def add_recipe(self, first_component_name: str, second_component_name: str, product_name: str):
        """
        Determine if recipe is valid and then add it to recipes.

        A recipe consists of three strings, two components and their product.
        If any of the parameters are the same, raise the 'DuplicateRecipeNamesException' exception.
        If there already exists a recipe for the given pair of components, raise the 'RecipeOverlapException' exception.

        :param first_component_name: The name of the first component element.
        :param second_component_name: The name of the second component element.
        :param product_name: The name of the product element.
        """
        if first_component_name == second_component_name or first_component_name == product_name or second_component_name == product_name:
            raise DuplicateRecipeNamesException
        recipe = self.get_recipe(first_component_name, second_component_name)
        if recipe in self.recipes:
            raise RecipeOverlapException
        self.recipes[recipe] = product_name
        self.reverse_recipes[product_name] = recipe

    def get_product_name(self, first_component_name: str, second_component_name: str):
        """
        Return the name of the product for the two components.

        The order of the first_component_name and second_component_name is interchangeable, so search for combinations of (first_component_name, second_component_name) and (second_component_name, first_component_name).

        If there are no combinations for the two components, return None

        Example:
            recipes = AlchemicalRecipes()
            recipes.add_recipe('Water', 'Wind', 'Ice')
            recipes.get_product_name('Water', 'Wind')  # ->  'Ice'
            recipes.get_product_name('Wind', 'Water')  # ->  'Ice'
            recipes.get_product_name('Fire', 'Water')  # ->  None
            recipes.add_recipe('Water', 'Fire', 'Steam')
            recipes.get_product_name('Fire', 'Water')  # ->  'Steam'

        :param first_component_name: The name of the first component element.
        :param second_component_name: The name of the second component element.
        :return: The name of the product element or None.
        """
        recipe = self.get_recipe(first_component_name, second_component_name)
        return self.recipes.get(recipe, None)

    def get_component_names(self, result):
        """Get component names given their result."""
        return self.reverse_recipes.get(result, None)

    @staticmethod
    def get_recipe(first, second):
        """Get recipe of 2 elements."""
        return (min(first, second), max(first, second))

    def __contains__(self, key):
        """Check if element is in recipes."""
        return key in self.recipes

    def __getitem__(self, key):
        """Get item from recipes."""
        return self.recipes[key]


class DuplicateRecipeNamesException(Exception):
    """Raised when attempting to add a recipe that has same names for components and product."""


class RecipeOverlapException(Exception):
    """Raised when attempting to add a pair of components that is already used for another existing recipe."""


class Cauldron(AlchemicalStorage):
    """
    Cauldron class.

    Extends the 'AlchemicalStorage' class.
    """

    def __init__(self, recipes: AlchemicalRecipes):
        """Initialize the Cauldron class."""
        super().__init__()
        self.recipebook = recipes

    def add(self, element: AlchemicalElement):
        """
        Add element to storage and check if it can combine with anything already inside.

        Use the 'recipes' object that was given in the constructor to determine the combinations.

        Example:
            recipes = AlchemicalRecipes()
            recipes.add_recipe('Water', 'Wind', 'Ice')
            cauldron = Cauldron(recipes)
            cauldron.add(AlchemicalElement('Water'))
            cauldron.add(AlchemicalElement('Wind'))
            cauldron.extract() # -> [<AE: Ice>]

        :param element: Input object to add to storage.
        """
        if isinstance(element, AlchemicalElement):
            if isinstance(element, Catalyst) and element.uses <= 0:
                self.storage.append(element)
                return
            for i in range(len(self.storage) - 1, -1, -1):
                el = self.storage[i]
                recipe = AlchemicalRecipes.get_recipe(element.name, el.name)
                if recipe in self.recipebook:
                    if isinstance(el, Catalyst):
                        if el.uses > 0:
                            el.uses -= 1
                        else:
                            continue
                    if isinstance(element, Catalyst):
                        element.uses -= 1
                        self.storage.append(element)

                    if not isinstance(el, Catalyst):
                        self.pop(el.name)
                    self.add(AlchemicalElement(self.recipebook[recipe]))
                    return
            self.storage.append(element)
        else:
            raise TypeError


class Purifier(AlchemicalStorage):
    """Purifier class."""

    def __init__(self, recipes: AlchemicalRecipes):
        """Initialize purifier class."""
        super().__init__()
        self.recipebook = recipes

    def add(self, element: AlchemicalElement):
        """Add element to storage."""
        if isinstance(element, AlchemicalElement):
            if element.name not in self.recipebook.reverse_recipes:
                self.storage.append(element)
            else:
                for el in self.recipebook.get_component_names(element.name):
                    self.add(AlchemicalElement(el))
        else:
            raise TypeError


class Catalyst(AlchemicalElement):
    """Catalyst class."""

    def __init__(self, name: str, uses: int) -> None:
        """Initialize class."""
        super().__init__(name)
        self.uses = uses

    def __repr__(self) -> str:
        """Class representation."""
        return f"<C: {self.name} ({self.uses})>" # Tes
