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
                              ("Wavelength","@x"),
                              ("Flux Density", "@y Jy"),
                              ("AB magnitude", "@ymag")])
TOOLS = ['box_zoom',hover,'reset']

colors = {'wfi':ColorPalette[8][1]}

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
    for mode in data.keys():
        for i,lim_flux in enumerate(data[mode]['sat_limits']):
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

            label = instrument+' '+mode
            x = data[mode]['wavelengths'][i]
            y = data[mode]['sat_limits'][i]/1000 #to Jy

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

            source = ColumnDataSource({'x':x[gsubs],'y':y[gsubs], 'label':[label]*x[gsubs].size, 'instrument':[instrument]*x[gsubs].size,
                                'config':[config]*x[gsubs].size, 'y_backup':y[gsubs], 'y_hidden':[1e18]*y[gsubs].size,
                                'ymag':-2.5*np.log10(y[gsubs]/3631.0)})

            if x.size==1:
                glyph = plot.circle(x='x',y='y', source=source,color=colors[instrument],size=7)
            else:
                glyph = plot.line(x='x',y='y', line_alpha=0.7, source=source, line_width=3,color=colors[instrument])

            # Store a reference to every data source
            sources[(label+config).replace(" ", "")] = glyph.data_source

# http://bokeh.pydata.org/en/1.1.0/docs/user_guide/interaction/callbacks.html#userguide-interaction-jscallbacks
scode = """
        var active_labels = [];
        for (let i = 0; i < this.active.length; i++) {
            active_labels.push(this.labels[this.active[i]].toLowerCase());
            }

        // the last two arguments are Bokeh-related, and have no data
        for (let i = 0; i < arguments.length - 2; i++) {
               console.log(arguments[i])
               let instrument = arguments[i].data.instrument[0];
               let ins_in_array = (active_labels.indexOf(instrument) > -1);
               console.log(ins_in_array, instrument);
               if (ins_in_array) {
                  arguments[i].data.y=arguments[i].data.y_backup;
               } else {
                  arguments[i].data.y=arguments[i].data.y_hidden;
               }
               arguments[i].change.emit();
           }

        """

callback = CustomJS(args=sources, code=scode)

checkbox_group = CheckboxButtonGroup(
        labels=["WFI"], active=[0],
        sizing_mode="scale_width", width=800)
#checkbox_group.js_on_event("button_click", callback)

spacer1 = Spacer()
spacer2 = Spacer()

l = layout([[spacer1,checkbox_group,spacer2], [plot]],sizing_mode='scale_width')
show(l)

script, div = autoload_static(l, CDN, "sat_plot.js")

#script, div = components(l)

f = open('sat_plot.js', 'w')
f.write(script)
f.close()
f = open('sat_div.html', 'w')
f.write(div)
f.close()
