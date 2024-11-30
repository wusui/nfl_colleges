# Copyright (C) 2024 Warren Usui, MIT License
"""
Scrape ESPN for NFL player alumni data
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas

def start_selenium(in_page):
    """
    Selenium start routine.
        in_page -- path to webpage
        returns driver
    """
    def ex_w_driver(driver):
        driver.get(in_page)
        return driver
    def add_opts(options):
        options.add_argument("--headless")
        return options
    return ex_w_driver(webdriver.Chrome(options=add_opts(Options())))

def get_roster_pages():
    """
    Return a list of roster pages (one for each NFL team)
    """
    def grp_content(content):
        return list(map(lambda a: a.get_attribute('href'),
                        list(filter(lambda a: a.text == 'Roster', content))))
    def grp_drvr(driver):
        return grp_content(driver.find_elements(By.CLASS_NAME, 'AnchorLink'))
    def grp_page(page):
        return grp_drvr(start_selenium(page))
    return grp_page("https://www.espn.com/nfl/teams")

def get_ptables():
    """
    Extract data from the team rosters
    """
    def get_team(hroster):
        return ' '.join(hroster.split('/')[-1].split('-')).title()
    def gp_inner(rosters):
        return list(zip(list(map(get_team, rosters)),
                        list(map(pandas.read_html, rosters))))
    return gp_inner(get_roster_pages())
