import platform
import os
import yaml
from hdv.validator import Validator


if not os.getenv('HDV_HOME'):
    if platform.system().lower() != 'windows':
        os.environ['HDV_HOME'] = os.getenv('HOME')
    else:
        os.environ['HDV_HOME'] = os.getenv('USERPROFILE')

# Create configuration
profiles_path = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator/hdv_profiles.yml")
default_profiles_path: str = os.path.join(os.path.dirname(__file__),
                                          'configurations/default_hdv_profiles.yml')

#  If the configuration path does not exist - then a default configuration will be created
if not os.path.exists(profiles_path):

    # Set the path for the default configuration if it does not exist
    hdv_profiles = os.path.join(os.getenv("HDV_HOME"), ".hashmap_data_validator")
    if not os.path.exists(hdv_profiles):
        os.mkdir(hdv_profiles)

    # Load the default configuration
    with open(default_profiles_path, 'r') as default_stream:
        profiles_configuration = yaml.safe_load(default_stream)

    # Write the default configuration
    with open(profiles_path, 'w') as stream:
        _ = yaml.dump(profiles_configuration, stream)

# give users ability to call validate method from python file
hdv = Validator().hdv
