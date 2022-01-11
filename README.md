# Pluto TV m3u8 generator
### A simple m3u8 generator for pluto-tv

---

## Installation

```bash
python -m pip install git+https://github.com/nickoehler/pluto_tv_m3u8
```

## Usage

```python
from pluto_tv_m3u8 import Pluto

# Automatically gets the channels data from pluto.tv
pluto = Pluto()

# list of dicts with the channels data
print(len(pluto.channels))

# you can generates a m3u8 string with the channels
m3u8_str = pluto.generate_m3u8()

# and also write the m3u8 file directly to disk
pluto.write_m3u8()
```
