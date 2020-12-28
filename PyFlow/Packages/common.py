import json
import queue
import threading
import time
import traceback

from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.Core.Common import PinDirection
from PyFlow.Core import NodeBase
from Qt.QtWidgets import QMessageBox

from config import DEBUG


def stop_pipeline(instance):
    run_tool = next(filter(lambda tool: tool.name() == "RunTool", instance._tools), None)
    if run_tool is not None:
        if DEBUG:
            print("STOPPING!")
        run_tool._stop_pipeline()


def node_id(node: NodeBase):
    return node.uid.int >> 64


def get_node_by_uid(nodes, uid):
    for node in nodes:
        if str(node.uid) == str(uid):
            return node


def get_pin_by_index(pins, index, direction=PinDirection.Input):
    for pin in pins:
        if pin.pinIndex == index and pin.direction == direction:
            return pin


def get_property_value(node, name, default=None):
    prop = next(filter(lambda obj: obj.name == name, node.inputs.values()), None)
    return (prop.currentData() or default) if prop is not None else default


def get_enum_values(enum):
    return list(filter(lambda var: var[0].isupper() and not var.startswith('_'), vars(enum)))


class DepthaiNode(NodeBase):
    def __init__(self, name):
        super(DepthaiNode, self).__init__(name)
        self.node_map = {}
        self.connection_map = {}

    def compute(self, *args, **kwargs):
        pass

    def build_pipeline(self, pipeline):
        raise NotImplementedError("Method build_pipeline not implemented!")

    def run_pipeline(self, device):
        raise NotImplementedError("Method run_pipeline not implemented!")

    def build_connections(self):
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        for out in self.outputs.values():
            for link in out.linkedTo:
                connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
                if not isinstance(connected_node, DeviceNode):
                    continue
                inp = get_pin_by_index(connected_node.pins, link['inPinId'])
                node_in = connected_node.connection_map[inp.name]
                self.connection_map[out.name].link(node_in)


class PreviewNode:
    pass


class DeviceNode(DepthaiNode):
    def __init__(self, name):
        super().__init__(name)
        self.headerColor = Colors.NodeNameRectGreen.getRgb()

    def run_pipeline(self, *args, **kwargs):
        raise RuntimeError("Device nodes cannot be run!")


def _receive_postprocess(ret_data):
    if not isinstance(ret_data, list):
        return ret_data

    if len(ret_data) == 0:
        return None
    elif len(ret_data) == 1:
        return ret_data[0]
    else:
        return ret_data


class CameraNode(DeviceNode):
    def getId(self):
        pass
        # nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        # cameras = list(sorted(map(lambda node: node.name, filter(lambda node: isinstance(node, CameraNode), nodes))))
        # cam_id = cameras.index(self.name)
        # return cam_id



class StopNodeException(Exception):
    pass


class HostNode(DepthaiNode):
    def __init__(self, name):
        super(HostNode, self).__init__(name)
        self.headerColor = Colors.NodeNameRectBlue.getRgb()
        self.queue = queue.Queue(1)

    def setup_connections(self):
        self._connections = {}
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        for output in self.outputs.values():
            self._connections[output.name] = []
            for link in output.linkedTo:
                connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
                inp = get_pin_by_index(connected_node.pins, link['inPinId'])
                self._connections[output.name].append((inp.name, connected_node))


    def send(self, output_name, data):
        for name, node in self._connections.get(output_name, []):
            try:
                node.queue.put_nowait({"name": name, "data": data})
            except queue.Full:
                pass

    def run(self, device):
        return

    def _fun(self, device):
        try:
            self.setup_connections()
            self.run(device)
        except Exception as e:
            traceback.print_exc()
            self._terminate()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error occured during node execution!")
            msg.setInformativeText(str(e))
            msg.setDetailedText(traceback.format_exc())
            msg.setWindowTitle("Node execution error!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def run_node(self, device):
        self._running = True
        self.t = threading.Thread(target=self._fun, args=(device, ), daemon=True)
        self.t.start()

    def stop_node(self):
        for connected_nodes in self._connections.values():
            for _, connected_node in connected_nodes:
                if isinstance(connected_node, HostNode):
                    connected_node.stop_node()
        self._running = False
        self.t.join(10)

    def _terminate(self):
            instance = self.getWrapper().canvasRef().pyFlowInstance
            threading.Thread(target=stop_pipeline, args=(instance,)).start()
            for connected_nodes in self._connections.values():
                for name, connected_node in connected_nodes:
                    if isinstance(connected_node, HostNode) and hasattr(connected_node, 'queue'):
                            connected_node.queue.put(None)


class OldHostNode:
    use_buffer = False

    def __init__(self, name):
        super().__init__(name)
        self.headerColor = Colors.NodeNameRectBlue.getRgb()

    def build_pipeline(self, *args, **kwargs):
        raise RuntimeError("Host nodes cannot build pipeline!")
    EXIT_MESSAGE = "exit_message"

    def run_node(self, device, show_q):
        self.queue = queue.Queue(1)
        self.thread = threading.Thread(target=self._thread_fun, args=(self.queue, device, show_q), daemon=True)
        self.thread.start()

    def stop_node(self, wait=True):
        if DEBUG:
            print(f"Stopping {self.name}")
        self.queue.put(self.EXIT_MESSAGE)
        if wait:
            self.join()

    def join(self):
        self.thread.join()
        if DEBUG:
            print(f"Stopped {self.name}")

    def _thread_fun(self, queue, device, show_q):
        self.queue = queue
        self.show_q = show_q
        if self.use_buffer:
            self.input_buffer = {}
        try:
            self.setup_connections()
            self.start(device)
            if DEBUG:
                print(f"{self.name} starting...")
            try:
                while True:
                    try:
                        FPS.update(self.name)
                        if self.use_buffer:
                            self.consume_queue_data()
                        self.run()
                    except StopNodeException:
                        break
            finally:
                self.end(device)
        except Exception as e:
            traceback.print_exc()
            instance = self.getWrapper().canvasRef().pyFlowInstance
            threading.Thread(target=stop_pipeline, args=(instance, )).start()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error occured during node execution!")
            msg.setInformativeText(str(e))
            msg.setDetailedText(traceback.format_exc())
            msg.setWindowTitle("Node execution error!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

    def setup_connections(self):
        self._connections = {}
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        for output in self.outputs.values():
            self._connections[output.name] = []
            for link in output.linkedTo:
                connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
                inp = get_pin_by_index(connected_node.pins, link['inPinId'])
                self._connections[output.name].append((inp.name, connected_node))

    def _get_queue_data(self):
        in_data = self.queue.get()
        self.queue.task_done()
        if not isinstance(in_data, dict):
            if in_data == self.EXIT_MESSAGE:
                if DEBUG:
                    print(f"{self.name} received exit message, exiting...")
                raise StopNodeException()
            if DEBUG:
                print(f"{self.name} received malformed data packet: {in_data}")
        return in_data

    def consume_queue_data(self):
        while not self.queue.empty():
            in_data = self._get_queue_data()
            self.input_buffer[in_data["name"]] = in_data["data"]


    def start(self, device):
        pass

    def end(self, device):
        pass

    def run(self):
        pass

    def display(self, frame):
        try:
            self.show_q.put_nowait(frame)
        except Exception as e:
            print(e)


    def send(self, output_name, data):
        for name, node in self._connections.get(output_name, []):
            try:
                if not hasattr(node, 'queue'):
                    repeat = 5
                    while repeat > 0:
                        time.sleep(1)
                        if hasattr(node, 'queue'):
                            break
                        else:
                            repeat -= 1

                node.queue.put_nowait({"name": name, "data": data})
            except queue.Full:
                if DEBUG:
                    print(f"Node {node.name} queue is full, skipping data from {self.name}...")

    def get_default(self, name):
        return None

    def receive(self, input_name, *input_names):
        if self.use_buffer:
            data = [
                self.input_buffer.get(key, self.get_default(key))
                for key in [input_name, *input_names]
            ]
        else:
            data = None
            while data is None:
                in_data = self._get_queue_data()
                if in_data['name'] == input_name:
                    data = in_data['data']
        return _receive_postprocess(data)


class ExportableNode:
    def export(self):
        if not isinstance(self, NodeBase):
            raise ValueError("Cannot export node if not an instance of NodeBase")

        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        node_data = {
            "id": node_id(self),
            "name": self.name,
            "properties": {
                prop.name: prop.currentData()
                for prop in self.inputs.values()
                if not prop.hasConnections()
            },
        }
        connections = [
            {
                "node1Id": node_id(self),
                "node2Id": node_id(get_node_by_uid(nodes, link['rhsNodeUid'])),
                "node1Output": out.name,
                "node2Input": get_pin_by_index(get_node_by_uid(nodes, link['rhsNodeUid']).pins, link['inPinId']).name
            }
            for out in self.outputs.values()
            for link in out.linkedTo
        ]
        return node_data, connections


class SchemaPropertiesNode:
    def get_properties_file(self):
        raise NotImplementedError()

    def add_properties(self):
        if not isinstance(self, NodeBase):
            raise ValueError("Cannot export node if not an instance of NodeBase")

        with open(self.get_properties_file(), 'r') as f:
            data = json.load(f)

        for key, value in data['properties'].items():
            if 'type' not in value:
                continue
            pin = self._resolve_pin(key, value['type'])
            if pin is None:
                continue
            if 'default' in value:
                pin.setData(value['default'])
            setattr(self, key, pin)

    def _resolve_pin(self, value_name, value_type):
        if value_type == "string":
            return self.createInputPin(value_name, 'StringPin')
        elif value_type == "number":
            return self.createInputPin(value_name, 'FloatPin')
        elif value_type == "integer":
            return self.createInputPin(value_name, 'IntPin')
        elif value_type == "boolean":
            return self.createInputPin(value_name, 'BoolPin')
        else:
            return None
