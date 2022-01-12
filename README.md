# Pluto TV m3u8 generator
### A simple m3u8 generator for pluto-tv

---

## Installation

```sh
python -m pip install git+https://github.com/nickoehler/pluto_tv_m3u8
```

## Usage

Use the following command to generate a new m3u8 file

```sh
python -m pluto_tv_m3u8
```

If you want to integrate the lib in your script just import it

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
