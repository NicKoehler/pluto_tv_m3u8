import logging
import argparse
from .pluto import Pluto

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("pluto_tv_m3u8")

# Parse command line arguments
parser = argparse.ArgumentParser(
    "python -m pluto_tv_m3u8",
    description="Pluto TV M3U8 Generator"
)

parser.add_argument(
    "-o", "--output",
    type=str,
    help="The output file name",
    required=False
)

# Parse arguments
args = parser.parse_args()
filename = args.output or "pluto_tv"

pluto = Pluto()
logger.info("Generating m3u8 file...")
pluto.write_m3u8(filename)
logger.info(f"File {filename}.m3u8 generated.")
