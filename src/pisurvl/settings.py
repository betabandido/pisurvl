import os.path
import yaml

PISURVL_PATH = os.path.join(os.path.expanduser('~'), '.pisurvl')

with open(os.path.join(PISURVL_PATH, 'settings.yaml')) as f:
    settings = yaml.load(f)
