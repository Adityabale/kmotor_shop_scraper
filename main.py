import os
import time
import requests
import warnings
import pandas as pd

from pathlib import Path
from typing import Optional
from datetime import datetime
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains


class KMotorShopScraper:
    main_page = 'https://www.kmotorshop.com/en/device/manu-car-list'

    def __init__(self):
        """ Initialize the webdriver"""
        self.driver: Optional[WebDriver] = None
        self.session = None

