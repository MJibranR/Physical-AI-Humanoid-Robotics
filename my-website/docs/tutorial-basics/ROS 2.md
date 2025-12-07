# ROS 2 Fundamentals

## What is ROS 2?

ROS (Robot Operating System) is an open-source, meta-operating system for robots. It provides a flexible framework, a collection of tools, libraries, and conventions that simplify the task of creating complex and robust robot behaviors across diverse hardware platforms. ROS 2 is the latest iteration, engineered to address the evolving demands of modern robotics applications, including real-time performance, support for multi-robot systems, and deployment on embedded platforms. It facilitates the development of modular and distributed robotic software.

### Key Concepts in ROS 2:
*   **Nodes**: The smallest unit of computation in ROS 2. Nodes are executable processes that perform a specific task (e.g., a sensor driver, a motor controller, a navigation algorithm). A complex robot system is composed of many interconnected nodes.
*   **Topics**: The primary mechanism for asynchronous, publish/subscribe messaging. Nodes can publish data (e.g., sensor readings, command velocities) to topics, and other nodes can subscribe to these topics to receive the data.
*   **Services**: A synchronous, request/reply communication mechanism. Services are used for operations that require an immediate response, such as querying a sensor for a single reading or triggering a specific action.
*   **Actions**: Designed for long-running, goal-oriented tasks that provide periodic feedback and can be preempted. Examples include navigating to a target location or performing a complex manipulation sequence.
*   **Messages**: Data structures that define the types of information exchanged over topics, services, and actions. ROS 2 provides a rich set of standard message types, and users can define custom messages.
*   **Parameters**: Configuration values that can be set dynamically by nodes or loaded from files. They allow for flexible adjustment of node behavior without recompilation.
*   **Packages**: The fundamental unit for organizing ROS 2 code. A package contains nodes, libraries, configuration files, message definitions, and other related resources.
*   **Workspaces**: Directories that contain multiple ROS 2 packages, allowing for easy management and building of related projects.

## Why ROS 2?

ROS 2's importance in modern robotics development cannot be overstated. It provides a standardized communication infrastructure and a rich ecosystem of tools, libraries, and drivers that significantly simplify the development and deployment of complex robotic systems. Its modular and distributed design promotes code reusability, fosters collaboration within the global robotics community, and accelerates innovation. By abstracting away much of the low-level communication and hardware interaction, ROS 2 allows developers to focus on higher-level robotic behaviors and algorithms.

## Core Features and Improvements over ROS 1:

ROS 2 was a major architectural overhaul from its predecessor, ROS 1, bringing crucial enhancements to meet contemporary robotics needs:
*   **DDS (Data Distribution Service) Integration**: ROS 2 leverages DDS as its underlying communication middleware. DDS is a standardized (OMG Standard) data-centric publish/subscribe messaging system known for its real-time performance, scalability, and reliability, making ROS 2 suitable for mission-critical applications.
*   **Quality of Service (QoS) Policies**: Developers can specify QoS policies for topics and actions, controlling aspects like reliability (e.g., best effort vs. reliable), durability (e.g., transient local vs. volatile), history (e.g., keep last vs. keep all), and liveliness. This allows fine-grained control over communication behavior.
*   **Multi-robot Support**: Designed from the ground up to handle fleets of robots, ROS 2 includes features for network discovery, namespace management, and distributed resource allocation, enabling complex multi-robot coordination.
*   **Security**: ROS 2 incorporates robust security features through SROS 2 (Secure ROS 2), providing authentication, authorization, encryption, and data integrity for inter-node communication, crucial for industrial and public-facing applications.
*   **Real-time Capabilities**: While not a hard real-time operating system itself, ROS 2 is built with real-time requirements in mind, offering improved support for applications demanding strict timing guarantees by using RTOS-compatible communication and executor models.
*   **Platform Independence**: Supports a wider range of operating systems beyond Linux, including Windows and macOS, broadening its applicability.
*   **Language Agnostic Clients**: Provides client libraries for multiple languages beyond C++ and Python, such as Java and C#, enhancing development flexibility.

**Example: ROS 2 Service Client (Python)**

This example demonstrates how to create a simple ROS 2 service client that sends a request and waits for a response. We'll assume a service that adds two integers.

First, define the service interface (e.g., `example_interfaces/srv/AddTwoInts.srv`):
```
# Request
int64 a
int64 b
---
# Response
int64 sum
```

Then, the Python client node:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts # Import the service type

class MinimalServiceClient(Node):
    def __init__(self):
        super().__init__('minimal_service_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        self.get_logger().info(f'Sending request: a={a}, b={b}')

def main(args=None):
    rclpy.init(args=args)
    minimal_service_client = MinimalServiceClient()
    minimal_service_client.send_request(41, 1) # Example values

    while rclpy.ok():
        rclpy.spin_once(minimal_service_client)
        if minimal_service_client.future.done():
            try:
                response = minimal_service_client.future.result()
            except Exception as e:
                minimal_service_client.get_logger().error(f'Service call failed: {e}')
            else:
                minimal_service_client.get_logger().info(
                    f'Result of add_two_ints: {minimal_service_client.req.a} + '
                    f'{minimal_service_client.req.b} = {response.sum}'
                )
            break
    
    minimal_service_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```
To run this example, you would first need a corresponding ROS 2 service server running (e.g., the `add_two_ints_server` from the `example_interfaces` package), and the `example_interfaces` package sourced in your environment.