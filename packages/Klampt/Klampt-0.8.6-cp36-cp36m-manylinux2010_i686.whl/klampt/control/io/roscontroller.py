"""Defines control interfaces between Klamp't and ROS.

- :class:`RosRobotController` is a Klampt
  :class:`~klampt.control.controller.ControllerBlock` that accepts inputs from
  a ROS controller.  This can be used to drive a simulation.
- :class:`RosRobotInterface` is a Klampt Robot Interface Layer
  (:class:~klampt.control.robotinterface.RobotInterfaceBase`) implementation 
  that outputs commands to a ROS controller.

This also implements the make() protocol for use in klampt_sim.  The returned
controller accepts ROS JointTrajectory messages from the ROS topic
'/[robot_name]/joint_trajectory' and writes out JointState messages to the ROS
topic '/[robot_name]/joint_state'.  It also acts as a ROS clock server.
"""

from .. import robotinterface
from .. import controller
from .. import blocks
import rospy
from klampt.trajectory import Trajectory,HermiteTrajectory
from trajectory_msgs.msg import JointTrajectory,JointTrajectoryPoint
from sensor_msgs.msg import JointState
from rosgraph_msgs.msg import Clock


#test
"""
class Time:
    def __init__(self):
        self.secs = 0
        self.nsecs = 0

class Clock:
    def __init__(self):
        self.clock = Time()

class JointTrajectory:
    def __init__(self):
        pass

class JointState:
    def __init__(self):
        pass

class PublisherProxy:
    def __init__(self,name,message_type):
        self.name = name
        self.message_type = message_type
        return
    def publish(self,object):
        print("Publishing on topic "+self.name+":")
        for k,v in object.__dict__.iteritems():
            if k[0]=='_': continue
            print("  ",k,":",v)
        return

class SubscriberProxy:
    def __init__(self,name,message_type,callback):
        self.name = name
        self.message_type = message_type
        self.callback = callback

class RospyProxy:
    def init_node(self,name):
        print("init_node("+name+") called")
        return
    def Publisher(self,topic,message_type):
        print("Making publisher on topic "+topic)
        return PublisherProxy(topic,message_type)
    def Subscriber(self,topic,message_type,callback):
        print("Making subscriber on topic "+topic)
        return SubscriberProxy(topic,message_type,callback)
rospy = RospyProxy()
"""

class RosRobotController(controller.RobotControllerBase):
    """A controller that reads JointTrajectory messages from a given ROS topic,
    maintains the trajectory for use in a Klamp't simulation, and writes
    JointState messages to another ROS topic.

    Uses PID control with optional feedforward torques in the effort term.

    Acts very much like a ROS JointTrajectoryActionController
    (http://wiki.ros.org/robot_mechanism_controllers/JointTrajectoryActionController)
    Currently does not support:
        * Setting PID gain constants,
        * Setting PID integral term bounds,
        * Parsing of FollowJointTrajectoryActions or reporting completion
          of the action.
        * Partial commands for subsets of joints are supported, but you
          cannot interleave separate messages to subsets of joints (i.e.,
          you must let one joint group finish before sending messages to
          another).
    
    Note: trajectory messages start execution exactly at the *Klamp't time*
    given in the time stamp in the header.  Hence, any nodes connected to this
    must have the /use_sim_time flag set to 1.
    """
    def __init__(self,joint_trajectory_sub_topic,joint_state_pub_topic,link_list):
        """Sets the controller to subscribe to JointTrajectory messages from
        joint_trajectory_sub_topic, and publishes JointState messages from
        joint_state_pub_topic.  The link_list argument is the ordered list
        of link names in the Klamp't robot model."""
        self.state = JointState()
        n = len(link_list)
        self.state.header.seq = 0
        self.state.name = link_list[:]
        self.state.position     = []
        self.state.velocity     = []
        self.state.effort       = []

        # fast indexing structure for partial commands
        self.nameToIndex = dict(zip(self.state.name,range(n)))

        # Setup publisher of robot states
        self.pub = rospy.Publisher(joint_state_pub_topic, JointState)
        
        # set up the command subscriber
        self.jointTrajectoryRosMsgQueue = []
        rospy.Subscriber(joint_trajectory_sub_topic, JointTrajectory,self.jointTrajectoryCallback)

        # these are parsed in from the trajectory message
        self.currentTrajectoryStart = 0
        self.currentTrajectoryNames = []
        self.currentPhaseTrajectory = None
        self.currentPositionTrajectory = None
        self.currentVelocityTrajectory = None
        self.currentEffortTrajectory = None
        return

    def jointTrajectoryCallback(self,msg):
        self.jointTrajectoryRosMsgQueue.append(msg)
        return

    def set_index(self,name,index):
        self.nameToIndex[name] = index

    def advance(self,**inputs):       
        res = {}
        for msg in self.jointTrajectoryRosMsgQueue:
            #parse in the message -- are positions, velocities, efforts specified?
            self.currentTrajectoryStart = inputs['t']
            self.currentTrajectoryNames = msg.joint_names
            #read in the start time according to the msg time stamp, as
            #specified by the ROS JointTrajectoryActionController
            starttime = msg.header.stamp.to_sec()
            #read in the relative times 
            times = [p.time_from_start.to_sec() for p in msg.points]
            milestones = [p.positions for p in msg.points]
            velocities = [p.velocities for p in msg.points]
            accels = [p.accelerations for p in msg.points]
            efforts = [p.efforts for p in msg.points]
            #TODO: quintic interpolation with accelerations
            if any(len(x) != 0 for x in accels):
                print("RosRobotController: Warning, acceleration trajectories not handled")
            if all(len(x) != 0 for x in milestones):
                if all(len(x) != 0 for x in velocities):
                    #Hermite interpolation
                    traj = HermiteTrajectory(times,milestones,velocities)
                    if self.currentPhaseTrajectory == None:
                        self.currentPhaseTrajectory = traj
                    else:
                        self.currentPhaseTrajectory=self.currentPhaseTrajectory.splice(traj,time=starttime,relative=True,jumpPolicy='blend')
                else:
                    #linear interpolation
                    self.currentPhaseTrajectory = None
                    traj = Trajectory(times,milestones)
                    if self.currentPositionTrajectory == None:
                        self.currentPositionTrajectory = traj
                    else:
                        self.currentPositionTrajectory = self.currentPositionTrajectory.splice(traj,time=starttime,relative=True,jumpPolicy='blend')
            else:
                self.currentPositionTrajectory = None
                self.currentPhaseTrajectory = None
                if all(len(x) != 0 for x in velocities):
                    #velocity control
                    traj = Trajectory(times,velocities)
                    if self.currentVelocityTrajectory == None:
                        self.currentVelocityTrajectory = traj
                    else:
                        self.currentVelocityTrajectory = self.currentVelocityTrajectory.splice(traj,time=starttime,relative=True,jumpPolicy='blend')
                else:
                    self.currentVelocityTrajectory = None
            if all(len(x) != 0 for x in efforts):
                traj = Trajectory(times,efforts)
                if self.currentEffortTrajectory == None:
                    self.currentEffortTrajectory = traj
                else:
                    self.currentEffortTrajectory.splice(traj,time=starttime,relative=True,jumpPolicy='blend')
            else:
                self.currentEffortTrajectory = None
        #clear the message queue
        self.jointTrajectoryRosMsgQueue = []
            
        #evaluate the trajectory and send it to controller's output
        t = inputs['t']
        if self.currentPhaseTrajectory != None:
            #hermite trajectory mode
            qdqcmd = self.currentPhaseTrajectory.eval(t,'halt')
            qcmd = qdqcmd[:len(qdqcmd)/2]
            dqcmd = qdqcmd[len(qdqcmd)/2:]
            self.map_output(qcmd,self.currentTrajectoryNames,res,'qcmd')
            self.map_output(dqcmd,self.currentTrajectoryNames,res,'dqcmd')
        elif self.currentPositionTrajectory != None:
            #piecewise linear trajectory mode
            qcmd = self.currentPositionTrajectory.eval(t,'halt')
            self.map_output(qcmd,self.currentTrajectoryNames,res,'qcmd')
            #automatic differentiation
            dqcmd = self.currentPositionTrajectory.deriv(t,'halt')
            self.map_output(dqcmd,self.currentTrajectoryNames,res,'dqcmd')
        elif self.currentVelocityTrajectory != None:
            #velocity trajectory mode
            dqcmd = self.currentVelocityTrajectory.deriv(t,'halt')
            self.map_output(dqcmd,self.currentTrajectoryNames,res,'dqcmd')
            #TODO: compute actual time of velocity
            res['tcmd'] = 1.0
        if self.currentEffortTrajectory != None:
            torquecmd = self.currentEffortTrajectory.eval(t,'halt')
            self.map_output(torquecmd,self.currentTrajectoryNames,res,'torquecmd')

        #sense the configuration and velocity, possibly the effort
        self.state.header.stamp = rospy.get_rostime()
        self.state.header.seq += 1
        if 'q' in inputs:
            self.state.position = inputs['q']
        if 'dq' in inputs:
            self.state.velocity = inputs['dq']
        if 'torque' in inputs:
            self.state.effort = inputs['torque']
        self.pub.publish(self.state)
        #print("ROS control result is",res)
        return res

    def map_output(self,vector,names,output_map,output_name):
        """Maps a partial vector to output_map[output_name].
        If output_name exists in output_map, then only the named values
        are overwritten.  Otherwise, the missing values are set to zero.
        """
        val = []
        if output_name in output_map:
            val = output_map[output_name]
        else:
            val = [0.0]*len(self.state.name)
        for n,v in zip(names,vector):
            val[self.nameToIndex[n]] = v
        output_map[output_name] = val
        return


class RosTimeBlock(controller.ControllerBlock):
    """A controller that simply publishes the simulation time to ROS.
    Doesn't output anything.
    """
    def __init__(self):
        self.clockpub = rospy.Publisher("/clock", Clock)
        
    def advance(self,**inputs):
        t = inputs['t']
        time = Clock()
        time.clock = rospy.Time.from_sec(t)
        self.clockpub.publish(time)
        return {}


class RosRobotInterface(robotinterface.RobotInterfaceBase):
    """Implements a Klampt Robot Interface Layer for a ROS controlled
    robot that outputs JointState messages and accepts JointTrajectory
    commands.

    initialize() will create and start a ROS node.

    initialize(False) will not start ROS. Instead, you'll have to do this 
    manually before calling initialize.

    close() is optional to call before quitting. It must be called if
    you'd like to re-initialize.
    """
    def __init__(self,robot,joint_state_sub_topic,joint_trajectory_pub_topic):
        self.robot = robot
        self.link_list = [robot.link(i).getName() for i in range(robot.numLinks())]
        self.driver_list = [robot.link(robot.driver(i).getAffectedLink()).getName() for i in range(robot.numDrivers())]
        self.link_dict = dict((n,i) for i,n in enumerate(self.link_list))
        self.joint_state_sub_topic = joint_state_sub_topic
        self.joint_trajectory_pub_topic = joint_trajectory_pub_topic
        self.commandedPosition = None
        self.last_joint_state = None
        self.joint_state_sub = None
        self.joint_trajectory_sub = None
        self.pub_seq = 0
    def initialize(self,init_ros=True):
        if init_ros:
            global ros_initialized
            ros_initialized = True
            rospy.init_node('klampt_RosRobotInterface')
        self.joint_state_sub = rospy.Subscriber(self.joint_state_sub_topic, JointState,self.jointStateCallback)
        self.joint_trajectory_pub = rospy.Publisher(self.joint_trajectory_pub_topic, JointTrajectory)
    def close(self):
        self.joint_state_sub.unregister()
        self.joint_state_sub = None
        self.joint_state_pub.unregister()
        self.joint_state_pub = None
    def jointStateCallback(self,jointState):
        if len(jointState.names) > self.robot.numLinks():
            raise RuntimeError("Invalid number of links")
        for n in jointState.names:
            if n not in self.link_dict:
                raise RuntimeError("Invalid link "+n+", must match Klamp't model")
        self.last_joint_state = jointState
    def klamptModel(self):
        return self.robot
    def clock(self):
        return rospy.get_rostime().to_sec()
    def status(self):
        return 'ok'
    def commandedPosition(self):
        return self.commandedPosition
    def sensedPosition(self):
        js = self.last_joint_state
        if js is None: return None
        q = self.robot.getConfig()
        for (v,n) in zip(js.position,js.names):
            q[self.link_dict[n]] = v
        return self.configFromKlampt(q)
    def sensedVelocity(self):
        js = self.last_joint_state
        if js is None: return None
        if len(js.velocity) == 0: return None
        dq = self.robot.getVelocity()
        for (v,n) in zip(js.velocity,js.names):
            dq[self.link_dict[n]] = v
        return self.velocityFromKlampt(dq)
    def sensedTorque(self):
        js = self.last_joint_state
        if js is None: return None
        if len(js.effort) == 0: return None
        t = [0.0]*self.robot.numLinks()
        for (v,n) in zip(js.effort,js.names):
            t[self.link_dict[n]] = v
        return self.velocityFromKlampt(t)
    def setPiecewiseLinear(self,ts,qs,relative=True):
        if not relative:
            raise NotImplementedError("Can't do non-relative piecewise-linear commands")
        traj = JointTrajectory()
        traj.header.seq = self.pub_seq
        self.pub_seq += 1
        traj.header.stamp = rospy.get_rostime()
        traj.joint_names = self.driver_list
        points = []
        for t,q in zip(ts,qs):
            pt = JointTrajectoryPoint()
            pt.time_from_start = rospy.Duration.from_sec(t)
            pt.positions = q
            points.append(pt)
        traj.points = points
        self.joint_trajectory_pub.publish(traj)


ros_initialized = False

def make(klampt_robot_model):
    """Creates a RosRobotController for the given model.
    klampt_robot_model is a RobotModel instance.

    Subscribes to '/[robot_name]/joint_trajectory'.
    Publishes to '/[robot_name]/joint_state' and '/clock'
    """
    global ros_initialized
    robotName = klampt_robot_model.getName()
    linkNames = [klampt_robot_model.link(i).getName() for i in range(klampt_robot_model.numLinks())]
    if not ros_initialized:
        ros_initialized = True
        rospy.init_node('klampt_sim')
        #launch a controller to publish the simulation time to ROS, PLUS
        #the robot's controller
        c = blocks.utils.MultiBlock()
        c.launch(RosTimeBlock())
        joint_trajectory_topic = "/%s/joint_trajectory"%(robotName,)
        joint_states_topic = "/%s/joint_states"%(robotName,)
        c.launch(RosRobotController(joint_trajectory_topic,joint_states_topic,linkNames))
        return c
    #just launch the robot's controller, some other RosTimeController has been
    #launched before
    joint_trajectory_topic = "/%s/joint_trajectory"%(robotName,)
    joint_states_topic = "/%s/joint_states"%(robotName,)
    return RosRobotController(joint_trajectory_topic,joint_states_topic,linkNames)
