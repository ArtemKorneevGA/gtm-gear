import os, sys, logging
import inspect



root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# Set path to folder with tagmanager.dat file
os.environ["GTM_API_CONFIG_FOLDER"] = ""

# path to parent folder
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from service import Service
from container import Container
from workspace import Workspace


account_id = ''
gtm_key = ""
workspace_name = "Test Workspace"
tag_name = 'html.test'

service = Service()
# Get container
source_container = Container(service, account_id, gtm_key)
# Get workspace

source_workspace = Workspace(source_container, workspace_name)

# Get tag
tag = source_workspace.get_tag(tag_name)
logging.info("Tag {} body: {}".format(tag.name, tag.data))

# Change tag chtml
tag.set_html('<script>consolt.log("test");</script>')
tag.update()

logging.info("tag {} updated".format(tag.name))


