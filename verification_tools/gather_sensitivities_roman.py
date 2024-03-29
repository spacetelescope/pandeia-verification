import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html, components, autoload_static
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, HoverTool, CustomJS, LogTickFormatter
from bokeh.layouts import column,layout, Spacer
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.models.axes import LinearAxis,LogAxis
from bokeh.models.ranges import Range1d
from bokeh.io import output_file, show
from bokeh.palettes import Set1 as ColorPalette


wfi_imaging = dict(np.load('../outputs/wfi_imaging_sensitivity.npz', fix_imports=True, encoding='latin1', allow_pickle=True))
wfi_spectroscopy = dict(np.load('../outputs/wfi_spectroscopy_sensitivity.npz', fix_imports=True, encoding='latin1', allow_pickle=True))

wfi = {'imaging':wfi_imaging,'spectroscopy':wfi_spectroscopy}

frame = {'wfi':wfi}

hover = HoverTool(tooltips = [("Mode","@label"),
                              ("Configuration", "@config"),
                              ("Wavelength","@x micron"),
                              ("Flux Density", "@y microJy"),
                              ("AB magnitude", "@ymag")])
TOOLS = ['box_zoom',hover,'reset']

colors = {'wfi':ColorPalette[8][1]}

yrange = (10**-3.0, 10**4.9)
plot = figure(x_axis_type="log",y_axis_type="log",y_range=yrange,x_range=(0.4,3.),
              x_axis_label="Wavelength [micron]", y_axis_label="Flux Density (S/N=10 in 10,000 s) [microJy]",
              width=600, height=400,tools=TOOLS,background_fill_color=None,
              border_fill_color = None, toolbar_location='above')

plot.xaxis.axis_label_text_font_size = '12pt'
plot.xaxis.major_label_text_font_size = '12pt'
plot.yaxis.axis_label_text_font_size = '12pt'
plot.yaxis.major_label_text_font_size = '12pt'

# Setting the second y axis range name and range
plot.extra_y_ranges = {"ABmag": Range1d(start=(-5.0/2.0)*np.log10(yrange[0]/3631e6), end=(-5.0/2.0)*np.log10(yrange[1]/3631e6))}
# Adding the second axis to the plot.
#plot.add_layout(LogAxis(y_range_name="ABmag", axis_label="AB mag"), 'right')

for axis in plot.axis:
    axis.axis_label_text_font_size = '12pt'
    axis.major_label_text_font_size = '12pt'


# Plot glyphs
sources = {}
for instrument in frame.keys():
    data = frame[instrument]
    for mode in data.keys():
        for i,lim_flux in enumerate(data[mode]['lim_fluxes']):
            config = ''
            if 'configs' in data[mode].keys():
                if 'aperture' in data[mode]['configs'][i].keys():
                    config += data[mode]['configs'][i]['aperture']
                    config += ' '
                print(mode,data[mode]['configs'][i].keys())
                if 'filter' in data[mode]['configs'][i].keys():
                    if data[mode]['configs'][i]['filter'] != None:
                        config += data[mode]['configs'][i]['filter']
                        config += ' '
                if 'disperser' in data[mode]['configs'][i].keys():
                    config += data[mode]['configs'][i]['disperser']
                    config += ' '
                if 'orders' in data[mode].keys():
                    config += str(data[mode]['orders'][i])
                    config += ' '
                if 'subarray' in data[mode]['configs'][i].keys():
                    if data[mode]['configs'][i]['subarray'] != "full":
                        continue


            label = instrument+' '+mode
            x = np.asarray(data[mode]['wavelengths'][i], dtype=float)
            y = np.asarray((data[mode]['lim_fluxes'][i]*1000), dtype=float) #to microJy

            x=x[np.isfinite(y)]
            y=y[np.isfinite(y)]

            if 'bounds' in data[mode]['configs'][i].keys():
                bounds = data[mode]['configs'][i]['bounds']
                gsubs = np.where((x>bounds[0]) & (x<bounds[1]))
            else:
                jumpl = [y[k]/y[k+1] if y[k]/y[k+1] > 1 else y[k+1]/y[k] for k in range(len(y)-1) ]
                jumpr = [y[k]/y[k-1] if y[k]/y[k-1] > 1 else y[k-1]/y[k] for k in range(1, len(y)) ]
                jumpl.insert(-1,1e99)
                jumpr.insert(0,1e99)
                if len(y) == 1:
                    gsubs = np.where(y > -7)
                else:
                    gsubs = [k for k in range(len(y)) if (jumpl[k] < 1.2 and jumpr[k] < 1.2) and (y[k] > -7)]

            source = ColumnDataSource({'x':x[gsubs],'y':y[gsubs], 'label':[label]*x[gsubs].size, 'instrument':[instrument]*x[gsubs].size,
                                       'config':[config]*x[gsubs].size, 'y_backup':y[gsubs], 'y_hidden':[1e18]*y[gsubs].size,
                                       'ymag':-2.5*np.log10(y[gsubs]/3631e6)})




            if len(x)==1:
                glyph = plot.circle(x='x',y='y', source=source,color=colors[instrument],size=7)
            else:
                glyph = plot.line(x='x',y='y', line_alpha=0.7, source=source, line_width=3,color=colors[instrument])
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
               let instrument = sourceargs[argval].data.instrument[0];
               let ins_in_array = (active_labels.indexOf(instrument) > -1);

               if (ins_in_array) {
                  sourceargs[argval].data.y=sourceargs[argval].data.y_backup;
               } else {
                  sourceargs[argval].data.y=sourceargs[argval].data.y_hidden;
               }
               sourceargs[argval].change.emit();
           })

        """

checkbox_group = CheckboxButtonGroup(
        labels=["WFI"], active=[0],
        sizing_mode="scale_width", width=800)
callback = CustomJS(args={"btns": checkbox_group, "sourceargs": sources}, code=scode)
checkbox_group.js_on_event("button_click", callback)


spacer1 = Spacer()
spacer2 = Spacer()

l = layout([[spacer1,checkbox_group,spacer2], [plot]],sizing_mode='scale_width')
show(l)

script, div = autoload_static(l, CDN, "etc_plot.js")

#script, div = components(l)

f = open('etc_plot.js', 'w')
f.write(script)
f.close()
f = open('etc_div.html', 'w')
f.write(div)
f.close()
