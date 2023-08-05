# Superpower GUI
> This application provides a graphical wrapper to access functions in the superpower R pacakge.


```
from IPython.display import display, YouTubeVideo
from ipywidgets import Output

out = Output()
with out:
    display(YouTubeVideo('5cNr5Dvzvrs'))
out
```

## Installing superpower_gui

`git clone https://github.rcac.purdue.edu/brewer36/superpower_gui.git`

`cd superpower_gui`

`pip install superpower_gui`

## Installing Superpower

### From Github

This application does not run without the companion R package, Superpower. You can install it any way you like. The application will check every library location listed by `.libPaths`. If the package isn't installed, the application can do that for you, but you must provide the path to the package source file. Since the package doesn't release these yet, so you will have to create one by building it from the original repository.

```bash
git clone https://github.rcac.purdue.edu/brewer36/SuperPower.git`
R CMD build SuperPower
R CMD INSTALL Superpower_<version>.tar.gz
```

### From a source file

Open ~/.superpower_gui/config.ini source file. You can optionally provide a library location if you'd like the source file to be installed in a particular place.

```
['R']
source = <source_dir>
lib_loc = <optional_lib_loc>
```

## How to use

This application runs in a single cell of a Jupyter Notebook, or an Javascript enabled IPython environment.

```
controller = Controller()
controller
```


    <IPython.core.display.Javascript object>

