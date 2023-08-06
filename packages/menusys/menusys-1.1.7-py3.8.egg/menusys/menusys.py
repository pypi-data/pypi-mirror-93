#!/usr/bin/env python3
"""
##########################################################
# Script Name: menusys.py                                #
# Script Type: Python                                    #
# Updated By: Benjamin P. Trachtenberg                   #
# Date Written 1/11/2015                                 #
#                                                        #
# Description:                                           #
# Menu system tools                                      #
#                                                        #
##########################################################
"""
import logging
import os as __os
import sys as __sys
import platform as __platform
import textwrap as __textwrap


LOGGER = logging.getLogger(__name__)


yes_no_dict = {
    1: {"MENU": "Yes"},
    2: {"MENU": "No"}}

prim_sec_dict = {
    1: {"MENU": "Primary"},
    2: {"MENU": "Secondary"}}


def word_wrap_string_and_print(string_to_wrap):
    """
    Function to word wrap a string depending on the console
    and print it

    :type string_to_wrap: String
    :param string_to_wrap: The string you want to wrap

    :rtype: None
    :return: None but it does call the print function

    """
    try:
        term_width, term_height = __os.get_terminal_size()
    except OSError:
        LOGGER.critical('Function word_wrap_string_and_print OSError')
        term_width = 80
    print(__textwrap.fill(string_to_wrap, term_width - 10))


def word_wrap_string(string_to_wrap):
    """
    Function to word wrap a string depending on the console

    :type string_to_wrap: String
    :param string_to_wrap: The string you want to wrap

    :rtype: String
    :return: A word wrapped string

    """
    try:
        term_width, term_height = __os.get_terminal_size()
    except OSError:
        LOGGER.critical('Function word_wrap_string OSError')
        term_width = 80
    return __textwrap.fill(string_to_wrap, term_width - 10)


def chunk_up_string(string_to_chunk, size_of_chunk=100):
    """
    Function to chunk up a string, and make a list of chunks

    :type string_to_chunk: String
    :param string_to_chunk: The string you want to chunk up

    :type size_of_chunk: Integer
    :param size_of_chunk: The size of the chunks in characters

    :rtype: List
    :return: A list containing the chunks.

    """
    temp_list = list()
    for chunk in range(0, len(string_to_chunk), size_of_chunk):
        temp_list.append(string_to_chunk[chunk:chunk + size_of_chunk])
    return temp_list


def menu(menu_dictionary, menu_header, back_function=None, no_quit=None, allow_sys_exit=None):
    """
    Function to create a menu from a dictionary with a back option

    :type menu_dictionary: Dict
    :param menu_dictionary: Dictionary in the following format {1: {'MENU': 'Yes'}, 2: {'MENU': 'No'}
    :type menu_header: String
    :param menu_header: The header of the menu
    :type back_function: Function
    :param back_function: The callback Function
    :type no_quit: Boolean
    :param no_quit: Set to True if you do not want a quit option
    :type allow_sys_exit: Boolean
    :param allow_sys_exit: Set to true if you want the menu to quit the app, default returns q

    :rtype: String
    :return: The selected option

    """
    max_menu_entries = 0
    options_list = list(menu_dictionary.keys())
    options_list.sort()
    word_wrap_string_and_print(menu_header)

    for options_list_line in options_list:
        if len(str(options_list_line)) == 1:
            print("%i ) %s" % (options_list_line, menu_dictionary[options_list_line]["MENU"]))
        elif len(str(options_list_line)) == 2:
            print("%i) %s" % (options_list_line, menu_dictionary[options_list_line]["MENU"]))
        max_menu_entries += 1

    if back_function:
        print("B ) Back")

    if not no_quit:
        print("Q ) Quit")

    selected_option = input("Please make a selection: ")
    selected_option = selected_option.lower()

    if back_function:
        if selected_option == "b":
            return back_function()

    if not no_quit:
        if selected_option == "q":
            if allow_sys_exit:
                __sys.exit('Application Quit')
            else:
                return "q"

    try:
        int(selected_option)
    except ValueError:
        selected_option = "0"

    if int(selected_option) == 0:
        good_selection = False
    elif int(selected_option) > max_menu_entries:
        good_selection = False
    else:
        good_selection = True

    while not good_selection:
        print("That selection is no good!!")
        selected_option = input("Please make a selection: ")
        selected_option = selected_option.lower()
        if back_function:
            if selected_option == "b":
                return back_function()
        if not no_quit:
            if selected_option == "q":
                if allow_sys_exit:
                    __sys.exit('Application Quit')
                else:
                    return "q"
        try:
            int(selected_option)
        except ValueError:
            selected_option = "0"

        if int(selected_option) == 0:
            good_selection = False
        elif int(selected_option) > max_menu_entries:
            good_selection = False
        else:
            good_selection = True

    return selected_option


def menu_multi_select(menu_dictionary, menu_header, back_function=None, no_quit=None, allow_sys_exit=None):
    """
    Function to create a menu from a dictionary with a back option

    :type menu_dictionary: Dict
    :param menu_dictionary: Dictionary in the following format {1: {'MENU': 'Yes'}, 2: {'MENU': 'No'}
    :type menu_header: String
    :param menu_header: The header of the menu
    :type back_function: Function
    :param back_function: The callback Function
    :type no_quit: Boolean
    :param no_quit: Set to True if you do not want a quit option
    :type allow_sys_exit: Boolean
    :param allow_sys_exit: Set to true if you want the menu to quit the app, default returns q

    :rtype: List
    :return: The selected options in a list

    """
    selections_list = []
    selected_option = None
    max_menu_entries = 0
    options_list = list(menu_dictionary.keys())
    options_list.sort()
    word_wrap_string_and_print(menu_header)

    for options_list_line in options_list:
        max_menu_entries += 1

    while selected_option != "c":
        for options_list_line in options_list:
            if len(str(options_list_line)) == 1:
                try:
                    print("%i ) %s" % (options_list_line, menu_dictionary[options_list_line]["MENU"]))
                except:
                    pass
            elif len(str(options_list_line)) == 2:
                try:
                    print("%i) %s" % (options_list_line, menu_dictionary[options_list_line]["MENU"]))
                except:
                    pass

        if back_function:
            print("B ) Back")
        print("C ) Continue")
        if not no_quit:
            print("Q ) Quit")
        selected_option = input("Please make a selection: ")
        selected_option = selected_option.lower()
        if back_function:
            if selected_option == "b":
                return back_function()
        if selected_option == "c":
            return selections_list
        if not no_quit:
            if selected_option == "q":
                if allow_sys_exit:
                    __sys.exit('Application Quit')
                else:
                    return "q"
        try:
            int(selected_option)
        except ValueError:
            selected_option = "0"

        if int(selected_option) == 0:
            good_selection = False
        elif int(selected_option) > max_menu_entries:
            good_selection = False
        else:
            good_selection = True

        while not good_selection:
            print("That selection is no good!!")
            selected_option = input("Please make a selection: ")
            selected_option = selected_option.lower()
            if back_function:
                if selected_option == "b":
                    return back_function()
            if selected_option == "c":
                return selections_list
            if not no_quit:
                if selected_option == "q":
                    if allow_sys_exit:
                        __sys.exit('Application Quit')
                    else:
                        return "q"
            try:
                int(selected_option)
            except ValueError:
                selected_option = "0"

            if int(selected_option) == 0:
                good_selection = False
            elif int(selected_option) > max_menu_entries:
                good_selection = False
            else:
                good_selection = True

        try:
            del menu_dictionary[int(selected_option)]
        except KeyError:
            print('You have already made that selection!!  Please try again.')

        already_selected = False

        for options_check in selections_list:
            if selected_option == options_check:
                already_selected = True
                break

        if not already_selected:
            selections_list.append(selected_option)


def make_menu_dict_from_dict(orig_dict, dict_key_for_display):
    """
    Function to create a menu dictionary with sub dictionary

    :type orig_dict: Dict
    :param orig_dict: Dictionary you want to make a menu from
    :type dict_key_for_display: String
    :param dict_key_for_display: Dictionary item to become the menu

    :rtype: Dict
    :return: A dictionary with menu and dictionary in line

    """
    temp_dict = dict()
    menu_new_key = 1

    for orig_dict_key in orig_dict:
        temp_dict[menu_new_key] = {'MENU': orig_dict[orig_dict_key][dict_key_for_display],
                                   'SUBDIC': orig_dict[orig_dict_key]}
        menu_new_key += 1

    return temp_dict


def make_menu_dict_from_list(orig_list):
    """
    Function to create a menu dictionary from a list

    :type orig_list: List
    :param orig_list: List you want to make a menu from

    :rtype: Dict
    :return: A dictionary with menu

    """
    temp_dict = dict()
    menu_new_key = 1

    for orig_list_line in orig_list:
        temp_dict[menu_new_key] = {'MENU': orig_list_line}
        menu_new_key += 1

    return temp_dict


def clear_screen():
    """
    Function to do a clear screen in Linux or Windows

    :rtype: None
    :return: None it clears the screen

    """
    if __platform.system() == "Windows":
        __os.system("cls")

    elif __platform.system() == "Linux":
        __os.system("clear")

    else:
        print("Your OS doesn't seem to be supported!")


if __name__ == "__main__":
    help(__name__)
