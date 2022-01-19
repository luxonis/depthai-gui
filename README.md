<img width="1201" alt="Screen Shot 2022-01-06 at 9 37 46 PM" src="https://user-images.githubusercontent.com/6503621/148497367-26ff816c-8a81-443c-9c4e-f598aa316885.png">

# Gen2 Visual Pipeline Editor
This experiment has two components:
1. A visual graph editor that lets you compose a DepthAI pipeline visually and save it as a JSON file.
2. A parser for those JSON files that will turn it into a usable DepthAI pipeline


## Editor 
The graph editor is a modified version of [NodeGraphQt](https://github.com/jchanvfx/NodeGraphQt) by Johnny Chan.

## Installation

To install this tool, run the following command

```
$ python3 -m pip install depthai-gui
```

## Usage

To run the **visual pipeline editor**, run the following command

```
$ depthai-gui
```

### Navigation
- Press **Tab** to create new nodes
- **Right Click** To save/load pipeline graphs
- You can find a full list of controls in the [NodeGraphQt Documentation](https://jchanvfx.github.io/NodeGraphQt/api/html/examples/ex_overview.html) 

You can also provide optional arguments, like default context path (`-p / --path`) or the project file to open (`-o / --open`)

```
$ depthai-gui --help
usage: depthai-gui [-h] [-p PATH] [-o OPEN]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to save/load default directory
  -o OPEN, --open OPEN  Path to project file to open
```

Also, you can use the **demo program** that will run the generated pipeline (or default [`ExampleGraph.json`](https://github.com/luxonis/depthai-gui/blob/master/ExampleGraph.json)) with the following command

```
$ depthai-gui-demo  # to run a default ExampleGraph.json
$ depthai-gui-demo -p <path>  # to run a custom pipeline
```

## Local development

If you want to enhance or modify this script or would like to install it without PyPi, please install all the necessary requirements with

```
$ python3 install_requirements.py
```

Next, you can check the following files:

 - `pipeline_editor.py` - Runs the visual pipeline editor (eqivalent of `depthai-gui`)
 - `demo.py`- Runs the demo script (equivalent of `depthai-gui-demo`)
 - `DAIPipelineGraph.py` is the graph parser.


## Using exported pipeline

If you want to use the generated pipeline in your application, you can do so by importing [`DAIPipelineGraph`](https://github.com/luxonis/depthai-gui/blob/master/DAIPipelineGraph.py) module.

And example integration is shown below

```
from DAIPipelineGraph import DAIPipelineGraph

pipeline_graph = DAIPipelineGraph( path=pipeline_path )

with dai.Device( pipeline_graph.pipeline ) as device:
  ...
```

The most useful fields you can use from [`DAIPipelineGraph`](https://github.com/luxonis/depthai-gui/blob/master/DAIPipelineGraph.py) class are:
- `DAIPipelineGraph.pipeline`: A reference to the DepthAI pipeline
- `DAIPipelineGraph.nodes`: A table of all the nodes. You can access them via the name you put into the "Node Name" field in the editor. Ex: `pipeline_graph.nodes["rgb_cam"].setPreviewSize(300,300)`
- `DAIPipelineGraph.xout_streams`: A list of all the names of the XLinkOut streams

You can also check [the demo script](https://github.com/luxonis/depthai-gui/blob/master/demo.py) as a reference on how to make a working scripts with this class
