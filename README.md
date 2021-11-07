
# Qcolor

## This is a little script to change the color from to bar in qtile!

this is simple, the script generates a json file in the qtile configuration, [my configuration from qtile](https://github.com/Rufi512/dotfiles/tree/main/.config/qtile) reads the generated json, the color bar and the text seen write to the file, you can configure the color manually or choose it from a image file

### Example
You can set the general color from the text in your config in based from the JSON
```python
try:
  from settings.colors import read_json
  color = read_json()
  color_text = color['text']
except:
color_text = '#ffffffFF'
```
and use it in the widgets
```python
widget.TextBox(text='|',fontsize=40,padding=2,foreground=color_text)
```
### Options

```
usage: qcolor [-h] [-s SOURCE] [-p PALLETE] [-c COLOR] [-t TEXT] [-o OPACITY] [-r] [-v]

Change the color from bar Qtile

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Image path
  -p PALLETE, --pallete PALLETE
                        Place a number and you will get the color palette of the image
  -c COLOR, --color COLOR
                        Set color for bar in format HexCode. 'ffffff'
  -t TEXT, --text TEXT  Set color text for bar in format HexCode. 'ffffff'
  -o OPACITY, --opacity OPACITY
                        Set the opacity of the color 0 ~ 100
  -r, --read            Read file json
  -v, --verbose         Get verbosity
  
```

##### is necessary restart qtile to see changes!