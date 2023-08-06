# altair_morberg



## Install

`pip install altair_morberg`

## How to use

```python
#hide_output
import altair as alt
import altair_morberg.core as morberg

alt.themes.register("morberg_theme", morberg.theme)
alt.themes.enable("morberg_theme")
```

[Examples](https://morberg.github.io/altair_morberg/examples.html) using this theme are available in [the documentation](https://morberg.github.io/altair_morberg/).

## Development

Built using [nbdev](https://nbdev.fast.ai). When you have done modifications you should [rebuild the lib](https://nbdev.fast.ai/example.html#Step-4:--Convert-Notebooks-To-Python-Modules-&-Docs) and test it with:

```
make all
make test
```

If you are happy with the results push a new version to pypi:

```
