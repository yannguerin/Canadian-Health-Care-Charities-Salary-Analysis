import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


def get_revenue_expenses_dicts(main):
    """Parses the Revenue and Expenses of the Charity from the Quick View Website's Main Section

    Args:
        main (bs4.element): The main section of the Quick View for the charity

    Returns:
        dict: A dictionary of Revenue for the charity
        dict: A dictionary of Expenses for the charity
    """
    sections = main.find_all("section")
    print(len(sections))
    revenue_section = sections[2]
    expenses_section = sections[3]
    revenue_legend = revenue_section.find_all("td", class_="legendLabel")
    print(len(revenue_legend))
    revenue_total = revenue_section.find("p", class_="h5")
    expenses_legend = expenses_section.find_all("td", class_="legendLabel")
    expenses_total = expenses_section.find("p", class_="h5")
    revenue_legend_dict = {}
    expenses_legend_dict = {}

    if revenue_legend != None and revenue_total != None:
        # Revenue Dict
        revenue_text = [label.text for label in revenue_legend]
        print(revenue_text)
        revenue_legend_dict["Legend"] = {
            text.split("$")[0].strip(): text.split("$")[1] for text in revenue_text
        }
        revenue_legend_dict["Total revenue"] = revenue_total.text.split("$")[1]
    else:
        print(type(revenue_legend))
        print(type(revenue_total))
        revenue_legend_dict = {"Error Encountered": revenue_section.text}

    if expenses_legend != None and expenses_total != None:
        # Expenses Dict
        expenses_text = [label.text for label in expenses_legend]
        expenses_legend_dict["Legend"] = {
            text.split("$")[0].strip(): text.split("$")[1] for text in expenses_text
        }
        expenses_legend_dict["Total expenses"] = expenses_total.text.split("$")[1]
    else:
        print(type(expenses_legend))
        print(type(expenses_total))
        expenses_legend_dict = {"Error Encountered": expenses_section.text}

    return revenue_legend_dict, expenses_legend_dict


def get_total_compensation_dict(main):
    """Parses the Total Compensation of the Charity from the Quick View Website's Main Section

    Args:
        main (bs4.element): The main section of the Quick View for the charity

    Returns:
        dict: A dictionary of Total Compensation for the charity
    """
    ul = main.find_all("ul")[2]
    total_compensation = [
        text.replace("\t", "")
        for text in ul.text.split("\n")
        if text.replace("\t", "") != ""
    ]
    if len(total_compensation) % 2 == 0:
        details = {
            total_compensation[index]: total_compensation[index + 1]
            for index in range(0, len(total_compensation), 2)
        }
        return details
    else:
        return total_compensation


def get_salary_info_dict(main):
    """Parses the Salary Info of the Charity from the Quick View Website's Main Section

    Args:
        main (bs4.element): The main section of the Quick View for the charity

    Returns:
        dict: A dictionary of Salary Info for the charity
    """
    additional = main.find("div", id="Additional")
    salary_html = (
        additional.previous_sibling.previous_sibling.previous_sibling.previous_sibling
    )
    # info_list = salary_html.text.split("\n")
    salary_list = [text for text in salary_html.text.split("\n") if text != ""]
    details = {
        salary_list[index]: salary_list[index + 1]
        for index in range(0, len(salary_list), 2)
    }
    return details


def get_program_info(main):
    """Parses the Ongoing Program Info of the Charity from the Quick View Website's Main Section

    Args:
        main (bs4.element): The main section of the Quick View for the charity

    Returns:
        str: A string of Ongoing Programs at the charity
    """
    program_para = main.find("p", id="ongoingprograms")
    return program_para.text.strip()


def parse_charity_details(detailed_text):
    details = {}
    formatted = (
        detailed_text.replace("  ", ": ")
        .replace("Sanction: Note: this link will load in another window or tab", "")
        .split(": ")
    )
    listed = [item.strip(" ") for item in formatted if item != ""]
    try:
        details = {
            listed[index]: listed[index + 1] for index in range(0, len(listed), 2)
        }
    except IndexError:
        details = {"Error Encountered": detailed_text}
        print("Failed due to Index error, formatted the text incorrectly.")
    return details
