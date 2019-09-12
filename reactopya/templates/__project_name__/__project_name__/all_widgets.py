####################################################################
# This file is automatically generated
# Do not edit manually
####################################################################

import base64
import os
from .reactopyacolabwidget import ReactopyaColabWidget
from .reactopyaelectronwidget import ReactopyaElectronWidget
from .init import _get_init_info
import importlib
import logging
import time
# logging.basicConfig(filename='/tmp/reactopya_debug', level=logging.INFO)
# logging.basicConfig(filename='/tmp/reactopya_debug', level=logging.CRITICAL)

{% for widget in widgets -%}
from .widgets import {{ widget.type }} as {{ widget.type }}Orig
{% endfor %}

{% for widget in widgets %}
class {{ widget.type }}:
    """Jupyter widget for {{ widget.type }}"""

    def __init__(self, *args, **kwargs):
        self._props = dict(**kwargs)
        self._children = {}
        self._child_ids = []
        for i, ch in enumerate(list(args)):
            self._children[i] = ch
            self._child_ids.append(str(i))
        self._connect_children(self._children)
        self._component = {{ widget.type }}Orig()
        self._component.on_python_state_changed(
            lambda state: self._handle_python_state_changed(state))
        self._reactopya_widget = None
        self._javascript_state = dict()  # for snapshot
        self._python_state = dict()  # for snapshot
        self._running_process = False  # for run_process_mode
        self._python_state_changed_handlers = []
        # self._component._initial_update()

    def _connect_children(self, children):
        for child_id, ch in children.items():
            self._connect_child(str(child_id), ch)

    def _connect_child(self, child_id, child):
        child_id = str(child_id)
        child.on_python_state_changed(
            lambda state: self._handle_python_state_changed(dict(_childId=child_id, state=state)))

    def _handle_python_state_changed(self, state):
        for key, val in state.items():
            self._python_state[key] = val  # for snapshot
        # if self._reactopya_widget:
        #     self._reactopya_widget.set_python_state(state)
        if self._running_process:
            msg = {"name": "setPythonState", "state": state}
            self._send_message_to_parent_process(msg)
        for handler in self._python_state_changed_handlers:
            handler(state)
    
    def on_python_state_changed(self, handler):
        self._python_state_changed_handlers.append(handler)

    
    # internal function to send message to javascript component
    def _send_message_to_parent_process(self, msg):
        import simplejson
        txt = simplejson.dumps(msg, ignore_nan=True)
        msg_path = os.path.join(self._run_process_mode_dirpath, '{}.msg-from-python'.format(self._run_process_mode_message_index))
        self._run_process_mode_message_index = self._run_process_mode_message_index + 1
        write_text_file(msg_path + '.tmp', txt)
        os.rename(msg_path + '.tmp', msg_path)

    def _handle_javascript_state_changed(self, state):
        for key, val in state.items():
            self._javascript_state[key] = val  # for snapshot
        if '_childId' in state:
            child_id = str(state['_childId'])
            self._children[child_id]._handle_javascript_state_changed(state['state'])
            return
        self._component._handle_javascript_state_changed(state)
    
    def _handle_add_child(self, child_id, project_name, type):
        child_id = str(child_id)
        mod = importlib.import_module(project_name)
        WIDGET = getattr(mod, type)
        W = WIDGET()
        self._connect_child(child_id, W)
        self._children[child_id] = W
        self._child_ids.append(child_id)
        return W

    def _serialize(self, include_javascript_state=False, include_python_state=False, include_bundle_fname=False):
        obj = dict(
            project_name='{{ project_name }}',
            type='{{ widget.type }}',
            children=[
                self._children[child_id]._serialize(include_javascript_state=include_javascript_state,
                              include_python_state=include_python_state, include_bundle_fname=include_bundle_fname)
                for child_id in self._child_ids
            ],
            props=_json_serialize(self._props)
        )
        if include_javascript_state:
            obj['javascript_state'] = _json_serialize(self._javascript_state)
        if include_python_state:
            obj['python_state'] = _json_serialize(self._python_state)
        if include_bundle_fname:
            dirname = os.path.dirname(os.path.realpath(__file__))
            obj['bundle_fname'] = os.path.join(dirname, 'dist', 'bundle.js')

        return obj

    def _reactopya_widget(self):
        return self._reactopya_widget

    def show(self):
        init_info = _get_init_info()
        if init_info['mode'] == 'jupyter':
            from reactopya_jup import ReactopyaJupyterWidget
            RW = ReactopyaJupyterWidget
        elif init_info['mode'] == 'colab':
            RW = ReactopyaColabWidget
        elif init_info['mode'] == 'electron':
            RW = ReactopyaElectronWidget
        self._reactopya_widget = RW(
            project_name='{{ project_name }}',
            type='{{ widget.type }}',
            children=[
                self._children[child_id]._serialize()
                for child_id in self._child_ids
            ],
            props=self._props
        )
        if init_info['mode'] == 'colab':
            self._reactopya_widget._set_bundle_js(
                init_info['bundle_js'], store_bundle_in_notebook=init_info['store_bundle_in_notebook'])
        elif init_info['mode'] == 'electron':
            self._reactopya_widget._set_bundle_fname(init_info['bundle_fname'])
            self._reactopya_widget._set_electron_src(init_info['electron_src'])
        self._reactopya_widget.on_javascript_state_changed(
            self._handle_javascript_state_changed)
        self._reactopya_widget.on_add_child(
            self._handle_add_child
        )

        self._reactopya_widget.show()

    def run_process_mode(self, dirpath):
        self._run_process_mode_dirpath = dirpath
        self._run_process_mode_message_index = 100000
        import simplejson
        import select
        self._running_process = True
        self._quit = False
        # self._component.on_python_state_changed(lambda state: self._handle_python_state_changed(state))
        while True:
            messages = self._read_messages(self._run_process_mode_dirpath)
            if len(messages) > 0:
                for msg in messages:
                    self._handle_message_process_mode(msg)
            else:
                self._component.iterate()
            if self._quit:
                break
            time.sleep(0.01)
            # time.sleep(1)
    
    def _read_messages(self, dirname):
        import simplejson
        messages = []
        files = os.listdir(dirname)
        files = sorted(files)
        for file in files:
            if file.endswith('.msg-from-js'):
                fname = os.path.join(dirname, file)
                with open(fname, 'r') as f:
                    msg = simplejson.load(f)
                messages.append(msg)
                os.remove(fname)
                break  # only one at a time for now
        return messages

    
    def _initial_update(self):
        self._component._initial_update()
        for ch in self._children.values():
            ch._initial_update()
    
    def add_serialized_children(self, children):
        for i, child in enumerate(children):
            W = self._handle_add_child(i, child.get('project_name', '{{ project_name }}'), child['type'])
            child_children = child.get('children', [])
            if len(child_children) > 0:
                W.add_serialized_children(child_children)
    
    def _handle_add_child_data(self, data):
        if '_childId' in data:
            child_id = str(data['_childId'])
            self._children[child_id]._handle_add_child_data(data['data'])
            return
        self._handle_add_child(data['childId'], data['projectName'], data['type'])
    
    # internal function to handle incoming message (coming from javascript component)
    def _handle_message_process_mode(self, msg):
        if msg['name'] == 'setJavaScriptState':
            self._handle_javascript_state_changed(msg['state'])
        elif msg['name'] == 'addChild':
            self._handle_add_child_data(msg['data'])
        elif msg['name'] == 'quit':
            self._quit = True
        else:
            print(msg)
            raise Exception('Unexpectected message in _handle_message_process_mode')

    def export_snapshot(self, output_fname, *, format):
        import simplejson
        if format is not 'html':
            raise Exception('Unsupported format: {}'.format(format))
        serialized_widget = self._serialize(
            include_javascript_state=True, include_python_state=True, include_bundle_fname=True)
        project_names = _get_all_project_names(serialized_widget)
        project_bundle_fnames = _get_project_bundle_fnames(serialized_widget)
        snapshot = dict(
            serialized_widget=serialized_widget,
            project_names=project_names,
            project_bundles=[_read_text_file(
                project_bundle_fnames[project_name]) for project_name in project_names]
        )

        html = '''
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />

    <!-- Disable caching by browser -->
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">

    <title></title>

    <style>
        body {
            font-family: sans-serif;
            margin: 0;
            padding: 0;
        }

        #root {
            height: 100vh;
            width: 100vw;

            display: flex;
            flex-direction: column;
            overflow: auto;

            /* background: #b8c1c3; */
        }
        .main-container-column {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 180px);
        }
    </style>
</head>

<body>
    <script type="text/javascript">

        var snapshot = get_snapshot_json_b64();
        snapshot = JSON.parse(atob(snapshot));
        for (let js of snapshot.project_bundles) {
            eval(js);
        }
        window.snapshot=snapshot;

        var sw = snapshot.serialized_widget;
        set_init_state_on_props(sw);

        window.reactopya.disable_python_backend = true;

        var div = document.createElement('div');
        div.id = 'root';
        document.body.appendChild(div);
        window.reactopya.widgets[sw.project_name][sw.type].render(div, sw.children, sw.props, sw.key || '', null);

        function set_init_state_on_props(serialized_widget) {
            let init_state = {};
            for (let key in serialized_widget.javascript_state) {
                init_state[key] = serialized_widget.javascript_state[key];
            }
            for (let key in serialized_widget.python_state) {
                init_state[key] = serialized_widget.python_state[key];
            }
            serialized_widget.props.reactopya_init_state = init_state;
            for (let child of serialized_widget.children) {
                set_init_state_on_props(child);
            }
        }

        function get_snapshot_json_b64() {
            return "[snapshot_json_b64]";
        }

    </script>
</body>

</html>
        '''
        html = html.replace('[snapshot_json_b64]', base64.b64encode(simplejson.dumps(snapshot, ignore_nan=True).encode('utf-8')).decode())
        with open(output_fname, 'w') as f:
            f.write(html)

{% endfor %}

def _get_all_project_names(serialized_widget):
    ret = []
    ret.append(serialized_widget['project_name'])
    for ch in serialized_widget.get('children', []):
        ret = ret + _get_all_project_names(ch)
    return list(set(ret))  # unique elements of array


def _get_project_bundle_fnames(serialized_widget):
    ret = dict()
    ret[serialized_widget['project_name']] = serialized_widget['bundle_fname']
    for ch in serialized_widget.get('children', []):
        a = _get_project_bundle_fnames(ch)
        for key, val in a.items():
            ret[key] = val
    return ret


def _read_text_file(fname):
    with open(fname, 'r') as f:
        return f.read()


def _listify_ndarray(x):
    if x.ndim == 1:
        if np.issubdtype(x.dtype, np.integer):
            return [int(val) for val in x]
        else:
            return [float(val) for val in x]
    elif x.ndim == 2:
        ret = []
        for j in range(x.shape[1]):
            ret.append(_listify_ndarray(x[:, j]))
        return ret
    elif x.ndim == 3:
        ret = []
        for j in range(x.shape[2]):
            ret.append(_listify_ndarray(x[:, :, j]))
        return ret
    elif x.ndim == 4:
        ret = []
        for j in range(x.shape[3]):
            ret.append(_listify_ndarray(x[:, :, :, j]))
        return ret
    else:
        raise Exception('Cannot listify ndarray with {} dims.'.format(x.ndim))


def _json_serialize(x):
    import numpy as np
    if isinstance(x, np.ndarray):
        return _listify_ndarray(x)
    elif isinstance(x, np.integer):
        return int(x)
    elif isinstance(x, np.floating):
        return float(x)
    elif type(x) == dict:
        ret = dict()
        for key, val in x.items():
            ret[key] = _json_serialize(val)
        return ret
    elif type(x) == list:
        ret = []
        for i, val in enumerate(x):
            ret.append(_json_serialize(val))
        return ret
    else:
        return x

def write_text_file(fname, txt):
    with open(fname, 'w') as f:
        f.write(txt)