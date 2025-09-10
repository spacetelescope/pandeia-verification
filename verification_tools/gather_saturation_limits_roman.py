import json
from jinja2 import Template
import numpy as np
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, autoload_static, json_item
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, HoverTool, CustomJS, InlineStyleSheet
from bokeh.layouts import column,layout, Spacer
from bokeh.models.widgets import CheckboxGroup
from bokeh.models.axes import LinearAxis,LogAxis
from bokeh.models.ranges import Range1d
from bokeh.io import output_file, show, curdoc
from bokeh.palettes import Category20 as ColorPalette



page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>

<body>
  <div id="satplot"></div>
  <script>
        const response = await fetch('/roman_sat_data.json');
        const item = await response.json();
        Bokeh.embed.embed_item(item, "satplot");
  </script>
</body>
""")

wfi_imaging = dict(np.load('../outputs/wfi_imaging_sensitivity.npz', fix_imports=True, encoding='latin1', allow_pickle=True))
wfi_spectroscopy = dict(np.load('../outputs/wfi_spectroscopy_sensitivity.npz', fix_imports=True, encoding='latin1', allow_pickle=True))

wfi = {'imaging':wfi_imaging,'spectroscopy':wfi_spectroscopy}

frame = {'wfi':wfi}

hover = HoverTool(tooltips = [("Mode","@label"),
                              ("Configuration", "@config"),
                              ("Wavelength","@x"),
                              ("Flux Density", "@y Jy"),
                              ("AB magnitude", "@ymag")])
TOOLS = ['box_zoom',hover,'reset']

colors = {
    'wfi01':ColorPalette[18][0],
    'wfi02':ColorPalette[18][1],
    'wfi03':ColorPalette[18][2],
    'wfi04':ColorPalette[18][3],
    'wfi05':ColorPalette[18][4],
    'wfi06':ColorPalette[18][5],
    'wfi07':ColorPalette[18][6],
    'wfi08':ColorPalette[18][7],
    'wfi09':ColorPalette[18][8],
    'wfi10':ColorPalette[18][9],
    'wfi11':ColorPalette[18][10],
    'wfi12':ColorPalette[18][11],
    'wfi13':ColorPalette[18][12],
    'wfi14':ColorPalette[18][13],
    'wfi15':ColorPalette[18][14],
    'wfi16':ColorPalette[18][15],
    'wfi17':ColorPalette[18][16],
    'wfi18':ColorPalette[18][17],
          }

yrange = (10**-4, 10**3.2)
plot = figure(x_axis_type="log",y_axis_type="log",y_range=yrange,x_range=(0.4,3.),
              x_axis_label="Wavelength [micron]", y_axis_label="Saturation limit [Jy]",
              width=600, height=400,tools=TOOLS,background_fill_color=None,
              border_fill_color = None, toolbar_location='above')

plot.xaxis.axis_label_text_font_size = '12pt'
plot.xaxis.major_label_text_font_size = '12pt'
plot.yaxis.axis_label_text_font_size = '12pt'
plot.yaxis.major_label_text_font_size = '12pt'

# Setting the second y axis range name and range
plot.extra_y_ranges = {"ABmag": Range1d(start=(-5.0/2.0)*np.log10(yrange[0]/3631.0), end=(-5.0/2.0)*np.log10(yrange[1]/3631.0))}
# Adding the second axis to the plot. Does not currently work properly - Bokeh has trouble mixing linear and log axes.
#plot.add_layout(LinearAxis(y_range_name="ABmag", axis_label="AB mag"), 'right')

for axis in plot.axis:
    axis.axis_label_text_font_size = '12pt'
    axis.major_label_text_font_size = '12pt'

# Plot glyphs
sources = {}
for instrument in frame.keys():
    data = frame[instrument]
    for xidx, x in enumerate(data['imaging']['configs']):
        print(xidx, x["detector"])
    for mode in data.keys():
        # pull out detectors
        detectors = sorted(list(set([x["detector"] for x in data[mode]["configs"]])))
        for detector in detectors:
            good = [x for x in range(len(data[mode]['lim_fluxes'])) if data[mode]['configs'][x]['detector'] == detector]
            for i,lim_flux in zip(good, data[mode]['lim_fluxes'][good]):
                config = ''
                if 'configs' in data[mode].keys():
                    if 'aperture' in data[mode]['configs'][i].keys():
                        config += data[mode]['configs'][i]['aperture']
                        config += ' '
                    if 'filter' in data[mode]['configs'][i].keys():
                        if data[mode]['configs'][i]['filter']:
                            # filter is defined, but None for some modes
                            config += data[mode]['configs'][i]['filter']
                            config += ' '
                    if 'disperser' in data[mode]['configs'][i].keys():
                        config += data[mode]['configs'][i]['disperser']
                        config += ' '
                    if 'orders' in data[mode].keys():
                        config += 'order '
                        config += str(data[mode]['orders'][i])
                        config += ' '

                label = instrument+' '+mode+ ' ' + detector
                x = np.asarray(data[mode]['wavelengths'][i], dtype=float)
                y = np.asarray(data[mode]['sat_limits'][i]/1000, dtype=float) #to Jy

                x=x[np.isfinite(y)]
                y=y[np.isfinite(y)]

                if instrument == 'nirspec':
                    jumpl = [y[k]/y[k+1] if y[k]/y[k+1] > 1 else y[k+1]/y[k] for k in range(len(y)-1) ]
                    jumpr = [y[k]/y[k-1] if y[k]/y[k-1] > 1 else y[k-1]/y[k] for k in range(1, len(y)) ]
                    jumpl.insert(-1,1e99)
                    jumpr.insert(0,1e99)
                    if len(y) == 1:
                        bsubs = np.where(y > 7)
                    else:
                        bsubs = [k for k in range(len(y)) if (jumpl[k] > 1.1 and jumpr[k] > 1.1) or (y[k] > 7)]
                    y[bsubs] = np.nan

                if mode == 'soss':
                    bsubs = np.where(y>10)
                    y[bsubs] = np.nan

                if mode == 'ami':
                    bsubs = np.where(y>20)
                    y[bsubs] = np.nan

                if 'bounds' in data[mode]['configs'][i].keys():
                    bounds = data[mode]['configs'][i]['bounds']
                    gsubs = np.where((x>bounds[0]) & (x<bounds[1]) & (y>-6))
                else:
                    gsubs = np.where(y>-6)

                source = ColumnDataSource({'x':x[gsubs],'y':y[gsubs], 'label':[label]*x[gsubs].size, 'instrument':[detector]*x[gsubs].size,
                                    'config':[config]*x[gsubs].size, 'y_backup':y[gsubs], 'y_hidden':[1e18]*y[gsubs].size,
                                    'ymag':-2.5*np.log10(y[gsubs]/3631.0)})

                if x.size==1:
                    glyph = plot.scatter(x='x',y='y', source=source,color=colors[detector],size=7)
                else:
                    glyph = plot.line(x='x',y='y', line_alpha=0.7, source=source, line_width=3,color=colors[detector])

                # Store a reference to every data source
                sources[(label+config).replace(" ", "")] = glyph.data_source

# http://bokeh.pydata.org/en/1.1.0/docs/user_guide/interaction/callbacks.html#userguide-interaction-jscallbacks
# https://docs.bokeh.org/en/3.2.2/docs/examples/interaction/js_callbacks/js_on_event.html
# https://www.freecodecamp.org/news/how-to-iterate-over-objects-in-javascript/
scode = """
        var active_labels = [];
        for (let i = 0; i < btns.active.length; i++) {
            active_labels.push(btns.labels[btns.active[i]].toLowerCase());
            }

        let sourceitem = Object.keys(sourceargs)
        
        // the last two arguments are Bokeh-related, and have no data
        sourceitem.forEach((argval) => {
               console.log(sourceargs[argval])
               let detector = sourceargs[argval].data.instrument[0];
               let ins_in_array = (active_labels.indexOf(detector) > -1);

               if (ins_in_array) {
                  sourceargs[argval].data.y=sourceargs[argval].data.y_backup;
               } else {
                  sourceargs[argval].data.y=sourceargs[argval].data.y_hidden;
               }
               sourceargs[argval].change.emit();
           })

        """

btnstyl = InlineStyleSheet(css="""  
                            div.bk-input-group span {
                           color: white;
                           }
    """)
checkbox_group = CheckboxGroup(
        labels=["WFI01", "WFI02", "WFI03", "WFI04", "WFI05", "WFI06", "WFI07", "WFI08", "WFI09", "WFI10", "WFI11", "WFI12", "WFI13", "WFI14", "WFI15", "WFI16", "WFI17", "WFI18"], 
        active=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
        sizing_mode="scale_width", stylesheets=[btnstyl])
callback = CustomJS(args={"btns": checkbox_group, "sourceargs": sources}, code=scode)
checkbox_group.js_on_change("active", callback)

spacer1 = Spacer()
spacer2 = Spacer()

l = layout([[plot, checkbox_group]], sizing_mode='scale_width')
curdoc().theme = 'dark_minimal'
curdoc().add_root(l)

show(l)

script, div = autoload_static(l, CDN, "sat_plot.js")

# script, div = components(l)

data_output = json.dumps(json_item(l, "plotdiv"))
f = open('roman_sat_data.json', 'w')
f.write(data_output)
f.close()
f = open('sat_div.html', 'w')
f.write(div)
f.close()
