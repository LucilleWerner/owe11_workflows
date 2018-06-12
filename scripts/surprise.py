import sys
from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('Geef 10 martijn!', font='starwars'), 'white', 'on_blue', attrs=['bold'])
