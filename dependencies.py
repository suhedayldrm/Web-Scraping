import csv
import urllib.request
import html.parser
from socket import error as SocketError
from http.cookiejar import CookieJar
from prettytable import PrettyTable
from flask import request
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
from requests.exceptions import HTTPError
from openpyxl import load_workbook
import requests
import re
