import sys
import cv2
import argparse
import depthai as dai

from pathlib import Path
from DAIPipelineGraph import DAIPipelineGraph

def main():
    default_json_path = (Path(__file__).parent / "ExampleGraph.json").resolve().absolute()
    if not default_json_path.exists():
        # used as module
        default_json_path = (Path(sys.prefix) / 'gui-data' / "ExampleGraph.json").resolve().absolute()
        if not default_json_path.exists():
            default_json_path = None

    parser = argparse.ArgumentParser()
    parser.add_argument( "-p", "--path", type=Path, default=default_json_path, help="Path to pipeline graph (Default: %(default)s)")
    args = parser.parse_args()

    if args.path is None:
        raise RuntimeError("Path to pipeline graph file is required.")

    # Create the pipeline
    pipeline_graph = DAIPipelineGraph( path=str(args.path) )

    # Display all XLinkOut data as CV frames
    with dai.Device( pipeline_graph.pipeline ) as device:
        queues = {}
        frames = {}

        for stream_id in pipeline_graph.xout_streams:
            queues[ stream_id ] = device.getOutputQueue( stream_id )
            frames[ stream_id ] = None

        while True:
            for stream_id in pipeline_graph.xout_streams:
                get_result = queues[ stream_id ].tryGet()

                # RGB Frame
                if get_result is not None:
                    frames[ stream_id ] = get_result.getCvFrame()

                # SHOW IMAGE
                if frames[ stream_id ] is not None:
                    cv2.imshow( stream_id, frames[ stream_id ] )

            # HANDLE QUIT
            if cv2.waitKey(1) == ord('q'):
                break


if __name__ == "__main__":
    main()