import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

class ArmController(Node):
    def __init__(self):
        super().__init__("arm_controller_client")
        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            '/arm_controller/follow_joint_trajectory'
        )
    def move_arm(self,base_angle,forearm_angle,duration):
        self.get_logger().info('waiting for arm controller ....')
        self.client.wait_for_server()
        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names  =[
            'base_joint',
            'forearm_joint'
        ]
        point = JointTrajectoryPoint()
        point.positions = [
            base_angle,
            forearm_angle
        ]
        point.time_from_start.sec = duration
        goal.trajectory.points.append(point)
        self.get_logger().info('Sending trajectory...')
        future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self,future)
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error("Trajectory rejected")
            return
        self.get_logger().info("trajectory Accepted")
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self,result_future)
        self.get_logger().info('Movement finished!')


def main():
    rclpy.init()
    node = ArmController()

    try:
        while rclpy.ok():

            # Move from 0° to 90°
            node.get_logger().info('Moving to 90 degrees')
            node.move_arm(
                base_angle=1.5708,
                forearm_angle=0.0,
                duration=2
            )

            # Move back from 90° to 0°
            node.get_logger().info('Returning to 0 degrees')
            node.move_arm(
                base_angle=0.0,
                forearm_angle=0.0,
                duration=2
            )

    except KeyboardInterrupt:
        node.get_logger().info('Stopping robot movement')

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

