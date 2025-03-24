import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PlasticPublisher(Node):
    def __init__(self):
        super().__init__('plastic_publisher')
        self.publisher_ = self.create_publisher(String, 'plastic_type', 10)

    def publish_plastic_type(self, plastic_type):
        msg = String()
        msg.data = plastic_type
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent: {plastic_type}')

def main(args=None):
    rclpy.init(args=args)
    plastic_publisher = PlasticPublisher()

    try:
        while True:
            # Example: Sending detected plastic types
            plastic_type = 'PET'  # Dummy data for now
            plastic_publisher.publish_plastic_type(plastic_type)

    except KeyboardInterrupt:
        plastic_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
