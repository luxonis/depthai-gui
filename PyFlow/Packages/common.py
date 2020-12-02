import json
import queue
import threading

from PyFlow.Core.Common import PinDirection

from PyFlow.Core import NodeBase


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


def get_property_value(node, name):
    return next(filter(lambda obj: obj.name == name, node.inputs.values())).currentData()


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
            node_out = self.connection_map[out.name]
            print(out.linkedTo)
            for link in out.linkedTo:
                connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
                inp = get_pin_by_index(connected_node.pins, link['inPinId'])
                node_in = connected_node.connection_map[inp.name]
                print(out.name, inp.name, self.connection_map[out.name], connected_node.connection_map[inp.name])
                try:
                    node_out.link(node_in)
                except:
                    print()
                    raise


class PreviewNode:
    pass


class DeviceNode(DepthaiNode):
    def run_pipeline(self, *args, **kwargs):
        raise RuntimeError("Device nodes cannot be run!")


class HostNode(DepthaiNode):
    def build_pipeline(self, *args, **kwargs):
        raise RuntimeError("Host nodes cannot build pipeline!")
    EXIT_MESSAGE = "exit_message"

    def run_node(self, device):
        self.queue = queue.Queue(16)
        self.thread = threading.Thread(target=self._thread_fun, args=(self.queue, device), daemon=True)
        self.thread.start()

    def _thread_fun(self, queue, device):
        self.queue = queue
        self.start(device)
        self.run()

    def start(self, device):
        pass

    def run(self):
        pass

    def send(self, output_name, data):
        nodes = self.getWrapper().canvasRef().graphManager.findRootGraph().getNodesList()
        out = next(filter(lambda output: output.name == output_name, self.outputs.values()))
        for link in out.linkedTo:
            connected_node = get_node_by_uid(nodes, link['rhsNodeUid'])
            connected_node.queue.put(data)

    def receive(self, input_name):
        data = self.queue.get()
        self.queue.task_done()
        return data

        # connections = [
        #     {
        #         "node1Id": node_id(self),
        #         "node2Id": node_id(get_node_by_uid(nodes, link['rhsNodeUid'])),
        #         "node1Output": out.name,
        #         "node2Input": get_pin_by_index(get_node_by_uid(nodes, link['rhsNodeUid']).pins, link['inPinId']).name
        #     }
        #     for out in self.outputs.values()
        #     for link in out.linkedTo
        # ]
        # return node_data, connections


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
