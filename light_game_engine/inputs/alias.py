"""
Named input aliases: map one or more keys/buttons - across any number
of Keyboard/Joystick inputs - onto one simple name, like "jump". Game
code can then just ask "was jump pressed?", without caring which key
or which controller button was used.
"""
from typing import Dict, List

from light_game_engine.inputs.game_input import InputModel, Keys, Buttons


class Alias:
    """
    Holds a group of inputs (Keyboard, Joystick, ...) and a group of
    named key/button aliases, and reports which aliases were pressed
    on the last frame.

    Does not call detect_buttons() on the inputs it holds. Each input
    must be refreshed by the caller (once per frame, the same as you
    would to read it directly). This keeps aliases in sync with any
    other code reading that same Keyboard/Joystick.
    """

    def __init__(self):
        """
        Start with no inputs and no aliases.
        """
        self.__inputs: List[InputModel] = []
        self.__input_alias: Dict[str, List['Keys | Buttons']] = {}

    def add_input(self, input_instance: InputModel):
        """
        Add an input source to read aliases from.

        :param input_instance: The Keyboard/Joystick (or other
            InputModel) to add.
        :return: This instance, for chaining.
        """
        self.__inputs.append(input_instance)
        return self

    def remove_input(self, input_instance: InputModel):
        """
        Stop reading aliases from an input source.

        :param input_instance: The input to remove. It must have been
            added before.
        :return: This instance, for chaining.
        :raises ValueError: If it was never added.
        """
        self.__inputs.remove(input_instance)
        return self

    def add_alias(self, alias_name: str, key: 'Keys | Buttons'):
        """
        Map a key/button onto a named alias. If you call this again
        with the same alias_name, the new key/button is added to it,
        not replacing the old one.

        :param alias_name: Name for this action, like "jump".
        :param key: A Keys or Buttons member that should trigger it.
        :return: This instance, for chaining.
        """
        alias = self.__input_alias.get(alias_name,[])
        alias.append(key)
        self.__input_alias[alias_name] = alias
        return self

    def remove_alias(self,alias_name:str):
        """
        Remove an alias completely.

        :param alias_name: The alias to remove.
        :return: This instance, for chaining.
        :raises KeyError: If it does not exist.
        """
        del self.__input_alias[alias_name]
        return self

    def remove_key_in_alias(self, alias_name:str, key: 'Keys | Buttons'):
        """
        Remove one key/button from an alias, keeping the rest.

        :param alias_name: The alias to change.
        :param key: The Keys or Buttons member to remove from it.
        :return: This instance, for chaining.
        :raises ValueError: If that key/button is not part of the
            alias.
        """
        alias = self.__input_alias.get(alias_name, [])
        alias.remove(key)
        self.__input_alias[alias_name] = alias
        return self

    def get_alias_triggered(self) -> List[str]:
        """
        Check each input's currently pressed keys/buttons against the
        registered aliases.

        This reads state that must already be refreshed - it does not
        call detect_buttons() itself. Call that on each input (once
        per frame) before this, the same as you would to read it
        directly.

        :return: The name of every alias that has at least one of its
            keys/buttons pressed, on some input. If more than one
            input triggers the same alias, its name appears more than
            once.
        :rtype: List[str]
        """
        alias_triggered = []

        for current_input in self.__inputs:
            if current_input.user_is_pressing:
                buttons = current_input.get_user_interaction
                for alias_name, alias_value in self.__input_alias.items():
                    triggered = [button for button in buttons if button in alias_value]
                    if len(triggered) > 0:
                        alias_triggered.append(alias_name)

        return alias_triggered
