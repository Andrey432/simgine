from .base import *
from pygame_gui.elements import UITextEntryLine
import re

__all__ = ['InputBox']


class InputBox(BaseElement):
    def __change_text(self, text):
        if self._elem.get_text() != text:
            self._elem.set_text(text)
    text = Field(str, __change_text)

    def __change_text_limit(self, limit): self._elem.set_text_length_limit(limit)
    max_length = Field(str, __change_text_limit)

    def __change_allowed(self, allowed): self._elem.set_allowed_characters(list(allowed))
    allowed_characters = Field(str, __change_allowed)

    def __change_forbidden(self, forbidden): self._elem.set_forbidden_characters(list(forbidden))
    forbidden_characters = Field(str, __change_forbidden)

    regexp_template = Field(re.Pattern)

    def __init__(self, id_, manager, kwargs):
        super().__init__(id_, manager, UITextEntryLine, relative_rect=kwargs['rect'])

    def is_valid_input(self) -> bool:
        text = self._elem.get_text()
        valid = self._elem.validate_text_string(text)
        if self.regexp_template is not None:
            valid = self.regexp_template.fullmatch(text) & valid
        return valid

    def handle_event(self, event) -> tuple:
        return super().handle_event(event)
