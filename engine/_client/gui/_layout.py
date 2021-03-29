from . import _elements


class Layout:
    def __init__(self, data, manager):
        self._elements = {}

        for elem, kwargs in data.items():
            classname = data[elem].pop('class')
            class_ = getattr(_elements, classname)
            element = class_(elem, manager, kwargs)
            self._elements[elem] = element

    def elements_list(self) -> list[_elements.BaseElement]:
        return list(self._elements.values())

    def get(self, element) -> _elements.BaseElement:
        return self._elements[element]
