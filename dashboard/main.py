from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import curdoc, figure
from bokeh.document import without_document_lock
from tornado import gen
import time
from functools import partial
from concurrent.futures import ThreadPoolExecutor
import sys
import os
import pathlib

sys.path.append(str(pathlib.Path(os.getcwd())))

import config  # MapR settings
from offset_tracker import OffsetTracker
import mapr_kafka_rest as mapr_kafka

BOKEH_MINIFIED = True


def _get_topic_datas(a_topic_name, an_offset, a_count=10):
    print('Dashboard:DEBUG: _get_topic_datas()')
    offset = an_offset
    xs = []
    ys = []

    print(
        'Dashboard:DEBUG: _get_topic_datas() calling mapr_kafka.get_topic_messages a_topic_name:{topic}, offset:{offset}, count:{count}...'.format(
            topic=a_topic_name, offset=offset, count=a_count))
    sensor_events = mapr_kafka.get_topic_messages(a_topic_name, offset, a_count=a_count)
    print(sensor_events)
    if sensor_events:
        for event in sensor_events:
            x = int(event['x'])
            y = int(event['value'])
            print('Dashboard:DEBUG: _get_topic_datas() - messages from topic {topic} has x={x}, y={y}'.format(
                topic=a_topic_name, x=x,
                y=y))
            xs.append(x)
            ys.append(y)
    else:
        print('Dashboard:DEBUG: _get_topic_datas() – No Data returned.')

    return xs, ys


def sleeping_task():
    print('DASHBOARD:DEBUG - sleeping_task()')
    time.sleep(1)
    return 1


@gen.coroutine
def locked_update():
    print('DASHBOARD:DEBUG - locked_update()')

    # Advanced:
    for sensor in sensors:
        offset_tracker = offset_trackers.get(sensor)
        x, y = _get_topic_datas(sensor, offset_tracker.offset)
        if x and y:
            offset_tracker.offset += len(x)
            new_data = dict(
                time=x,
                value=y
            )
            print(
                'DASHBOARD:DEBUG - update_all_sensor_graphs() - {sensor} – streaming new data...'.format(sensor=sensor))
            data_sources[sensor].stream(new_data, 20)


@without_document_lock
@gen.coroutine
def update_all_sensor_graphs():
    print('DASHBOARD:DEBUG - update_all_sensor_graphs()')
    res = yield executor_sleep.submit(sleeping_task)
    doc.add_next_tick_callback(partial(locked_update))


executor_sleep = ThreadPoolExecutor(max_workers=2)
sensors = [  # config.MAPR_STREAM_PATH_TOPIC,
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_01,
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_02,
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_03,
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_04]

plot_properties = {  # config.MAPR_STREAM_PATH_TOPIC: {'y_axis_label': config.YAXIS_LABEL_SENSOR_01,
    # 'title.text': config.MAPR_STREAM_TOPIC_NAME_DYNAMIC_01,
    # 'color': config.LINE_COLOR_SENSOR_01},
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_01: {'y_axis_label': config.YAXIS_LABEL_SENSOR_01,
                                               'title.text': config.MAPR_STREAM_TOPIC_NAME_DYNAMIC_01,
                                               'color': config.LINE_COLOR_SENSOR_01},
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_02: {'y_axis_label': config.YAXIS_LABEL_SENSOR_02,
                                               'title.text': config.MAPR_STREAM_TOPIC_NAME_DYNAMIC_02,
                                               'color': config.LINE_COLOR_SENSOR_02},
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_03: {'y_axis_label': config.YAXIS_LABEL_SENSOR_03,
                                               'title.text': config.MAPR_STREAM_TOPIC_NAME_DYNAMIC_03,
                                               'color': config.LINE_COLOR_SENSOR_03},
    config.MAPR_STREAM_TOPIC_PATH_DYNAMIC_04: {'y_axis_label': config.YAXIS_LABEL_SENSOR_04,
                                               'title.text': config.MAPR_STREAM_TOPIC_NAME_DYNAMIC_04,
                                               'color': config.LINE_COLOR_SENSOR_04}, }

offset_trackers = {}
data_sources = {}
for sensor in sensors:
    offset_trackers[sensor] = OffsetTracker()
    data_sources[sensor] = ColumnDataSource(dict(time=[0, ], value=[0]))

plots = {}
for sensor in sensors:
    sensor_plot = figure(tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_label='time', y_axis_location="left",
                         y_axis_label=plot_properties.get(sensor).get('y_axis_label'))
    sensor_plot.x_range.follow = "end"
    sensor_plot.x_range.follow_interval = 10
    sensor_plot.x_range.range_padding = 0
    sensor_plot.title.text = plot_properties.get(sensor).get('title.text')
    sensor_plot.title.text_color = plot_properties.get(sensor).get('color')
    sensor_plot.title.text_font_size = "25px"
    sensor_plot.title.align = 'center'
    sensor_plot.yaxis.axis_label_text_font_style = 'bold'
    sensor_plot.yaxis.axis_label_text_font_size = "15px"
    sensor_plot.line(x='time', y='value', alpha=1.0, line_width=3,
                     color=plot_properties.get(sensor).get('color'), source=data_sources[sensor])
    plots[sensor] = sensor_plot

doc = curdoc()
doc.add_root(gridplot(list(plots.values()), toolbar_location="left", ncols=2, plot_width=500, plot_height=500))

doc.title = "Sensor Streaming"

print("DASHBOARD DEBUG: adding - doc.add_periodic_callback(update_all_sensor_graphs, 500)")
doc.add_periodic_callback(update_all_sensor_graphs, 500)
print("DASHBOARD DEBUG: done - doc.add_periodic_callback(update_all_sensor_graphs, 500)")
