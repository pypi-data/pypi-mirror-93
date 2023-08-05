"""A collection of utility functions for dealing with sensors and sensor data.

More sophisticated operations call for the use of a full-fledged sensor
package, such as Open3D or PCL.

Sensor transforms
=================

The :func:`get_sensor_xform`/:func:`set_sensor_xform` functions are used to
interface cleanly with the klampt :mod:`klampt.math.se3` transform
representation.

Getting images and point clouds
===============================

The :func:`camera_to_images`, :func:`camera_to_points`, and
:func:`camera_to_points_world` functions convert raw CameraSensor outputs to
Python objects that are more easily operated upon, e.g., images and point
clouds.  Use these to retrieve images as Numpy arrays.

The :func:`image_to_points` function converts a depth / color image to a
point cloud, given camera intrinsic information.

Working with cameras
====================

The :class:`ProjectiveCameraModel`, :func:`camera_to_viewport`, and
:func:`camera_from_viewport` help with converting to and from the
:class:`klampt.vis.glprogram.GLViewport` class used in :mod:`klampt.vis`.

:func:`camera_ray`, and :func:`camera_project` convert to/from image points.
:func:`visible` determines whether a point or object is visible from a camera.

"""

from ..robotsim import *
from ..io import loader
from . import coordinates
import math
import sys
from ..math import vectorops,so3,se3
import time

_has_numpy = False
_tried_numpy_import = False
np = None

_has_scipy = False
_tried_scipy_import = False
sp = None

def _try_numpy_import():
    global _has_numpy,_tried_numpy_import
    global np
    if _tried_numpy_import:
        return _has_numpy
    _tried_numpy_import = True
    try:
        import numpy as np
        _has_numpy = True
        #sys.modules['numpy'] = numpy
    except ImportError:
        import warnings
        warnings.warn("klampt.model.sensing.py: numpy not available.",ImportWarning)
        _has_numpy = False
    return _has_numpy

def _try_scipy_import():
    global _has_scipy,_tried_scipy_import
    global sp
    if _tried_scipy_import:
        return _has_scipy
    _tried_scipy_import = True
    try:
        import scipy as sp
        _has_scipy = True
        #sys.modules['scipy'] = scipy
    except ImportError:
        import warnings
        warnings.warn("klampt.model.sensing.py: scipy not available.",ImportWarning)
        _has_scipy = False
    return _has_scipy

def get_sensor_xform(sensor,robot=None):
    """Extracts the transform of a SimRobotSensor.  The sensor must be
    of a link-mounted type, e.g., a CameraSensor or ForceSensor.

    Args:
        sensor (SimRobotSensor)
        robot (RobotModel, optional): if provided, returns the world
            coordinates of the sensor.  Otherwise, returns the local
            coordinates on the link to which it is mounted.

    Returns:
        klampt.se3 object: the sensor transform  
    """
    s = sensor.getSetting("Tsensor")
    Tsensor = loader.readSe3(s)
    if robot is not None:
        link = int(sensor.getSetting("link"))
        if link >= 0:
            return se3.mul(robot.link(link).getTransform(),Tsensor)
    return Tsensor


def set_sensor_xform(sensor,T,link=None):
    """Given a link-mounted sensor (e.g., CameraSensor or ForceSensor), sets 
    its link-local transform to T.

    Args:
        sensor (SimRobotSensor)
        T (se3 element or coordinates.Frame): desired local coordinates of the
            sensor on its link.
        link (int or RobotModelLink, optional): if provided, the link of the
            sensor is modified. 

    Another way to set a sensor is to give a coordinates.Frame object.  This
    frame must either be associated with a RobotModelLink or its parent should
    be associated with  one.

    (the reason why you should use this is that the Tsensor attribute has a
    particular format using the loader.writeSe3 function.)
    """
    if isinstance(T,coordinates.Frame):
        if isinstance(T._data,RobotModelLink):
            #attach it directly to the link
            return set_sensor_xform(sensor,se3.identity(),T._data)
        parent = None
        if T.parent() is None:
            parent = -1
        else:
            #assume its parent is a link?
            parent = T.parent()._data
        return set_sensor_xform(sensor,T.relativeCoordinates(),parent)
    try:
        s = sensor.getSetting("Tsensor")
    except Exception:
        raise ValueError("Sensor does not have a Tsensor attribute")
    sensor.setSetting("Tsensor",loader.writeSe3(T))
    if link != None:
        if isinstance(link,RobotModelLink):
            sensor.setSetting("link",str(link.index))
        else:
            assert isinstance(link,int),"Can only set a sensor transform to a RobotModelLink or an integer link index"
            sensor.setSetting("link",str(link))


def camera_to_images(camera,image_format='numpy',color_format='channels'):
    """Given a SimRobotSensor that is a CameraSensor, returns either the RGB
    image, the depth image, or both.

    Args:
        camera (SimRobotSensor): a sensor that is of 'CameraSensor' type
        image_format (str): governs the return type.  Can be:

            * 'numpy' (default): returns numpy arrays.  Depending on the
              value of color_format, the RGB image either has shape (h,w,3)
              and dtype uint8 or (h,w) and dtype uint32. Depth images as
              numpy arrays with shape (h,w).  Will fall back to 'native' if 
              numpy is not available.
            * 'native': returns list-of-lists arrays in the same format as
              above

        color_format (str): governs how pixels in the RGB result are packed. 
        Can be:

            * 'channels' (default): returns a 3D array with 3 channels
               corresponding to R, G, B values in the range [0,255]. 
            * 'rgb' returns a 2D array with a 32-bit integer channel, with
              R,G,B channels packed in hex format 0xrrggbb.
            * 'bgr': similar to 'rgb' but with hex order 0xbbggrr.

    (Note that image_format='native' takes up a lot of extra memory, especially
    with color_format='channels')

    Returns:
        tuple: (rgb, depth), which are either numpy arrays or list-of-lists
        format, as specified by image_format.

            * rgb: the RGB result (packed as specified by color_format)
            * depth: the depth result (floats)

    """
    assert isinstance(camera,SimRobotSensor),"Must provide a SimRobotSensor instance"
    assert camera.type() == 'CameraSensor',"Must provide a camera sensor instance"
    #import time
    #t_1 = time.time()
    w = int(camera.getSetting('xres'))
    h = int(camera.getSetting('yres'))
    has_rgb = int(camera.getSetting('rgb'))
    has_depth = int(camera.getSetting('depth'))
    #t0 = time.time()
    #print("camera.getSettings() time",t0-t_1)
    measurements = camera.getMeasurements()
    #t1 = time.time()
    #print("camera.getMeasurements() time",t1-t0)
    if image_format == 'numpy':
        if not _try_numpy_import():
            image_format = 'native'
    rgb = None
    depth = None
    if has_rgb:
        if image_format == 'numpy':
            #t0 = time.time()
            argb = np.array(measurements[0:w*h]).reshape(h,w).astype(np.uint32)
            #t1 = time.time()
            #print("Numpy array creation time",t1-t0)
            if color_format == 'rgb':
                rgb = argb
            elif color_format == 'bgr':
                rgb = np.bitwise_or.reduce((np.left_shift(np.bitwise_and(argb,0x00000ff),16),
                                        np.bitwise_and(argb,0x000ff00)),
                                        np.right_shift(np.bitwise_and(argb,0x0ff0000), 16))
            else:
                rgb = np.zeros((h,w,3),dtype=np.uint8)
                rgb[:,:,0] = np.right_shift(np.bitwise_and(argb,0x0ff0000), 16)
                rgb[:,:,1] = np.right_shift(np.bitwise_and(argb,0x00ff00), 8)
                rgb[:,:,2] =                np.bitwise_and(argb,0x00000ff)
            #t2 = time.time()
            #print("  Conversion time",t2-t1)
        else:
            if color_format == 'rgb':
                rgb = []
                for i in range(h):
                    rgb.append([int(v) for v in measurements[i*w:(i+1)*w]])
            elif color_format == 'bgr':
                def bgr_to_rgb(pixel):
                    return ((pixel & 0x0000ff) << 16) | (pixel & 0x00ff00) | ((pixel & 0xff0000) >> 16)
                rgb = []
                for i in range(h):
                    rgb.append([bgr_to_rgb(int(v)) for v in measurements[i*w:(i+1)*w]])
            else:
                rgb = []
                for i in range(h):
                    start = i*w
                    row = []
                    for j in range(w):
                        pixel = int(measurements[start+j])
                        row.append([(pixel>>16)&0xff,(pixel>>8)&0xff,pixel&0xff])
                    rgb.append(row)
    if has_depth:
        start = (w*h if has_rgb else 0)
        if image_format == 'numpy':
            #t0 = time.time()
            depth = np.array(measurements[start:start+w*h]).reshape(h,w)
            #t1 = time.time()
            #print("Numpy array creation time",t1-t0)
        else:
            depth = []
            for i in range(h):
                depth.append(measurements[start+i*w:start+(i+1)*w])
    if has_rgb and has_depth:
        return rgb,depth
    elif has_rgb:
        return rgb
    elif has_depth:
        return depth
    return None


def image_to_points(depth,color,xfov,yfov=None,depth_scale=None,depth_range=None,color_format='auto',points_format='numpy',all_points=False):
    """Given a depth and optionally color image, returns a point cloud
    representing the depth or RGB-D scene.  

    Args:
        depth (list of lists or numpy array): the w x h depth image (rectified).
        color (list of lists or numpy array, optional): the w x h color image. 
            Assumed that color maps directly onto depth pixels.  If None,
            an uncolored point cloud will be produced. 
        xfov (float): horizontal field of view, in radians.
        yfov (float, optional): vertical field of view, in radians.  If not
            given, square pixels are assumed.
        depth_scale (float, optional): a scaling from depth image values to
            absolute depth values.
        depth_range (pair of floats, optional): if given, only points within 
            this depth range (non-inclusive) will be extracted.  If
            all_points=False, points that fail the range test will be stripped
            from the output.  E.g., (0.5,8.0) only extracts points with
            z > 0.5 and z < 8 units.
        color_format (str): governs how pixels in the RGB result are packed. 
            Can be:

            * 'auto' (default): if it's a 3D array, it assumes elements are in
              'channels' format, otherwise it assumes 'rgb'.
            * 'channels': a 3D array with 3 channels corresponding to R, G,
              B values in the range [0,255] if uint8 type, otherwise in the
              range [0,1]. 
            * 'rgb' a 2D array with a 32-bit integer channel, with
              R,G,B channels packed in hex format 0xrrggbb.

        points_format (str, optional): configures the format of the return
            value. Can be:

            * 'numpy' (default): either an Nx3, Nx4, or Nx6 numpy array,
              depending on whether color is requested (and its format).  Will
              fall back to 'native' if numpy is not available.
            * 'native': same as numpy, but in list-of-lists format rather than
              numpy arrays.
            * 'PointCloud': a Klampt PointCloud object
            * 'Geometry3D': a Klampt Geometry3D point cloud object

        all_points (bool, optional): configures whether bad points should be
            stripped out.  If False (default), this strips out all pixels that
            don't have a good depth reading (i.e., the camera sensor's maximum
            reading.)  If True, these pixels are all set to (0,0,0).

    Returns:
        numpy ndarray or Geometry3D: the point cloud.  Represented as being local to the standard
        camera frame with +x to the right, +y down, +z forward.

    """
    has_numpy = _try_numpy_import()
    if not has_numpy:
        raise NotImplementedError("TODO image_to_points without numpy")
    depth = np.asarray(depth)
    assert len(depth.shape)==2
    h,w = depth.shape
    if color is not None:
        color = np.asarray(color)
        if h != color.shape[0] or w != color.shape[1]:
            raise ValueError("color and depth need to have same dimensions")
        if color_format == 'auto':
            if len(color.shape)==3:
                color_format = 'channels'
            else:
                assert len(color.shape)==2
                color_format = 'rgb'
    if depth_scale is not None:
        depth *= depth_scale
    if depth_range is not None:
        valid = np.logical_and((depth > depth_range[0]),(depth < depth_range[1]))
        if all_points:
            depth[~valid] = 0
        valid = (depth > 0)
    else:
        valid = (depth > 0)

    xshift = -w*0.5
    yshift = -h*0.5
    xscale = math.tan(xfov*0.5)/(w*0.5)
    if yfov is not None:
        yscale = -1.0/(math.tan(yfov*0.5)*h/2)
    else:
        yscale = xscale #square pixels are assumed
    xs = [(j+xshift)*xscale for j in range(w)]
    ys = [(i+yshift)*yscale for i in range(h)]
    if color_format == 'channels' and color.dtype == np.uint8:
        #scale to range [0,1]
        color = color*(1.0/255.0)

    xgrid = np.repeat(np.array(xs).reshape((1,w)),h,0)
    ygrid = np.repeat(np.array(ys).reshape((h,1)),w,1)
    assert xgrid.shape == (h,w)
    assert ygrid.shape == (h,w)
    pts = np.dstack((np.multiply(xgrid,depth),np.multiply(ygrid,depth),depth))
    assert pts.shape == (h,w,3)
    if color_format is not None:
        if len(color.shape) == 2:
            color = color.reshape(color.shape[0],color.shape[1],1)
        pts = np.concatenate((pts,color),2)
    #now have a nice array containing all points, shaped h x w x (3+c)
    #extract out the valid points from this array
    if all_points:
        pts = pts.reshape(w*h,pts.shape[2])
    else:
        pts = pts[valid]

    if points_format == 'native':
        return pts.tolist()
    elif points_format == 'numpy':
        return pts
    elif points_format == 'PointCloud' or points_format == 'Geometry3D':
        res = PointCloud()
        if all_points:
            res.setSetting('width',str(w))
            res.setSetting('height',str(h))
        res.setPoints(pts.shape[0],pts[:,0:3].flatten().tolist())
        if color_format == 'rgb':
            res.addProperty('rgb')
            res.setProperties(pts[:,3].flatten().tolist())
        elif color_format == 'channels':
            res.addProperty('r')
            res.addProperty('g')
            res.addProperty('b')
            res.setProperties(pts[:,3:6].flatten().tolist())
        if points_format == 'PointCloud':
            return res
        else:
            from klampt import Geometry3D
            g = Geometry3D()
            g.setPointCloud(res)
            return g
    else:
        raise ValueError("Invalid points_format, must be either native, numpy, PointCloud, or Geometry3D")


def camera_to_points(camera,points_format='numpy',all_points=False,color_format='channels'):
    """Given a SimRobotSensor that is a CameraSensor, returns a point cloud
    associated with the current measurements.

    Points are triangulated with respect to the camera's intrinsic coordinates,
    and are returned in the camera local frame (+z backward, +x toward the
    right, +y toward up). 

    The arguments 

    Args:
        points_format (str, optional): configures the format of the return
            value. Can be:

            * 'numpy' (default): either an Nx3, Nx4, or Nx6 numpy array,
              depending on whether color is requested (and its format).  Will
              fall back to 'native' if numpy is not available.
            * 'native': same as numpy, but in list-of-lists format rather than
              numpy arrays.
            * 'PointCloud': a Klampt PointCloud object
            * 'Geometry3D': a Klampt Geometry3D point cloud object

        all_points (bool, optional): configures whether bad points should be
            stripped out.  If False (default), this strips out all pixels that
            don't have a good depth reading (i.e., the camera sensor's maximum
            reading.)  If True, these pixels are all set to (0,0,0).

        color_format (str):  If the sensor has an RGB component, then color
            channels may be produced.  This value configures the output format,
            and can take on the values:

            * 'channels': produces individual R,G,B channels in the range
              [0,1]. (note this is different from the interpretation of
              camera_to_images)
            * 'rgb': produces a single 32-bit integer channel packing the 8-bit
              color channels together in the format 0xrrggbb.
            * None: no color is produced.

    Returns:
        object: the point cloud in the requested format.
    """
    assert isinstance(camera,SimRobotSensor),"Must provide a SimRobotSensor instance"
    assert camera.type() == 'CameraSensor',"Must provide a camera sensor instance"
    assert int(camera.getSetting('depth'))==1,"Camera sensor must have a depth channel"
    has_numpy = _try_numpy_import()
    if points_format == 'numpy' and not has_numpy:
        points_format = 'native'

    images = camera_to_images(camera,'numpy',color_format)
    assert images != None

    rgb,depth = None,None
    if int(camera.getSetting('rgb'))==0:
        depth = images
        color_format = None
    else:
        rgb,depth = images

    w = int(camera.getSetting('xres'))
    h = int(camera.getSetting('yres'))
    xfov = float(camera.getSetting('xfov'))
    yfov = float(camera.getSetting('yfov'))
    zmin = float(camera.getSetting('zmin'))
    zmax = float(camera.getSetting('zmax'))
    xshift = -w*0.5
    yshift = -h*0.5
    xscale = math.tan(xfov*0.5)/(w*0.5)
    #yscale = -1.0/(math.tan(yfov*0.5)*h/2)
    yscale = xscale #square pixels are assumed
    xs = [(j+xshift)*xscale for j in range(w)]
    ys = [(i+yshift)*yscale for i in range(h)]
    if has_numpy:
        if all_points:
            depth[depth >= zmax] = 0
        if color_format == 'channels':
            #scale to range [0,1]
            rgb = rgb*(1.0/255.0)
        xgrid = np.repeat(np.array(xs).reshape((1,w)),h,0)
        ygrid = np.repeat(np.array(ys).reshape((h,1)),w,1)
        assert xgrid.shape == (h,w)
        assert ygrid.shape == (h,w)
        pts = np.dstack((np.multiply(xgrid,depth),np.multiply(ygrid,depth),depth))
        assert pts.shape == (h,w,3)
        if color_format is not None:
            if len(rgb.shape) == 2:
                rgb = rgb.reshape(rgb.shape[0],rgb.shape[1],1)
            pts = np.concatenate((pts,rgb),2)
        #now have a nice array containing all points, shaped h x w x (3+c)
        #extract out the valid points from this array
        if all_points:
            pts = pts.reshape(w*h,pts.shape[2])
        else:
            pts = pts[depth < zmax]

        if points_format == 'native':
            return pts.tolist()
        elif points_format == 'numpy':
            return pts
        elif points_format == 'PointCloud' or points_format == 'Geometry3D':
            res = PointCloud()
            if all_points:
                res.setSetting('width',str(w))
                res.setSetting('height',str(h))
            res.setPoints(pts.shape[0],pts[:,0:3].flatten().tolist())
            if color_format == 'rgb':
                res.addProperty('rgb')
                res.setProperties(pts[:,3].flatten().tolist())
            elif color_format == 'channels':
                res.addProperty('r')
                res.addProperty('g')
                res.addProperty('b')
                res.setProperties(pts[:,3:6].flatten().tolist())
            elif color_format == 'bgr':
                raise ValueError("bgr color format not supported with PointCloud output")
            if points_format == 'PointCloud':
                return res
            else:
                from klampt import Geometry3D
                g = Geometry3D()
                g.setPointCloud(res)
                return g
        else:
            raise ValueError("Invalid points_format "+points_format)
        return Nnoe
    else:
        raise NotImplementedError("Native format depth image processing not done yet")


def camera_to_points_world(camera,robot,points_format='numpy',color_format='channels'):
    """Same as :meth:`camera_to_points`, but converts to the world coordinate
    system given the robot to which the camera is attached.  

    Points that have no reading are stripped out.
    """
    assert isinstance(camera,SimRobotSensor),"Must provide a SimRobotSensor instance"
    assert camera.type() == 'CameraSensor',"Must provide a camera sensor instance"
    link = int(camera.getSetting('link'))
    Tsensor = camera.getSetting('Tsensor')
    #first 9: row major rotation matrix, last 3: translation
    entries = [float(v) for v in Tsensor.split()]
    Tworld = get_sensor_xform(camera,robot)
    #now get the points
    pts = camera_to_points(camera,points_format,all_points=False,color_format=color_format)
    if points_format == 'numpy':
        Rw = np.array(so3.matrix(Tworld[0]))
        tw = np.array(Tworld[1])
        pts[:,0:3] = np.dot(pts[:,0:3],Rw.T) + tw
        return pts
    elif points_format == 'native':
        for p in pts:
            p[0:3] = se3.apply(Tworld,p[0:3])
        return pts
    elif points_format == 'PointCloud' or points_format == 'Geometry3D':
        pts.transform(*Tworld)
    else:
        raise ValueError("Invalid format "+str(points_format))
    return pts


def camera_to_viewport(camera,robot):
    """Returns a GLViewport instance corresponding to the camera's view. 

    See :mod:`klampt.vis.glprogram` and :mod:`klampt.vis.visualization` for
    information about how to use the object with the visualization, e.g.
    ``vis.setViewport(vp)``.

    Args:
        camera (SimRobotSensor): the camera instance.
        robot (RobotModel): the robot on which the camera is located, which
            should be set to the robot's current configuration.  This could be
            set to None, in which case the camera's transform is in its link's
            local coordinates.

    Returns:
        :class:`GLViewport`: matches the camera's viewport.
    """
    assert isinstance(camera,SimRobotSensor),"Must provide a SimRobotSensor instance"
    assert camera.type() == 'CameraSensor',"Must provide a camera sensor instance"
    from ..vis.glviewport import GLViewport
    xform = get_sensor_xform(camera,robot)
    w = int(camera.getSetting('xres'))
    h = int(camera.getSetting('yres'))
    xfov = float(camera.getSetting('xfov'))
    yfov = float(camera.getSetting('yfov'))
    zmin = float(camera.getSetting('zmin'))
    zmax = float(camera.getSetting('zmax'))
    view = GLViewport()
    view.w, view.h = w,h
    view.fov = math.degrees(xfov)
    view.camera.dist = 1.0
    view.camera.tgt = se3.apply(xform,[0,0,view.camera.dist])
    #axes corresponding to right, down, fwd in camera view
    view.camera.set_orientation(xform[0],['x','y','z'])
    view.clippingplanes = (zmin,zmax)
    return view


def viewport_to_camera(viewport,camera,robot):
    """Fills in a simulated camera's settings to match a GLViewport specifying
    the camera's view. 

    Args:
        viewport (GLViewport): the viewport to match
        camera (SimRobotSensor): the viewport will be output to this sensor
        robot (RobotModel): the robot on which the camera is located, which
            should be set to the robot's current configuration.  This could be
            set to None, in which case the camera's transform is in its link's
            local coordinates.

    """
    from ..vis.glprogram import GLViewport
    assert isinstance(viewport,GLViewport)
    assert isinstance(camera,SimRobotSensor),"Must provide a SimRobotSensor instance"
    assert camera.type() == 'CameraSensor',"Must provide a camera sensor instance"
    xform = viewport.getTransform()
    link = int(camera.getSetting('link'))
    if link < 0 or robot is None:
        rlink = None
    else:
        rlink = robot.link(link)
    set_sensor_xform(camera,xform,rlink)
    (zmin,zmax) = viewport.clippingplanes
    xfov = math.radians(viewport.fov)
    yfov = xfov*viewport.h/viewport.w
    camera.setSetting('xres',str(viewport.w))
    camera.setSetting('yres',str(viewport.h))
    camera.setSetting('xfov',str(xfov))
    camera.setSetting('yfov',str(yfov))
    camera.setSetting('zmin',str(zmin))
    camera.setSetting('zmax',str(zmax))
    return camera


def camera_ray(camera,robot,x,y):
    """Returns the (source,direction) of a ray emanating from the
    SimRobotSensor at pixel coordinates (x,y).

    If you are doing this multiple times, it's faster to convert the camera
    to GLViewport and use GLViewport.click_ray.

    Arguments:
        camera (SimRobotSensor): the camera
        robot (RobotModel): the robot on which the camera is mounted.
        x (int/float): x pixel coordinates
        y (int/float): y pixel coordinates

    Returns:
        (source,direction): world-space ray source/direction.
    """
    return camera_to_viewport(camera,robot).click_ray(x,y)


def camera_project(camera,robot,pt,clip=True):
    """Given a point in world space, returns the (x,y,z) coordinates of the
    projected pixel.  z is given in absolute coordinates, while x,y are given
    in pixel values.

    If clip=True and the point is out of the viewing volume, then None is
    returned. Otherwise, if the point is exactly at the focal plane then the
    middle of the viewport is returned.

    If you are doing this multiple times, it's faster to convert the camera
    to GLViewport and use GLViewport.project.

    Arguments:
        camera (SimRobotSensor): the camera
        robot (RobotModel): the robot on which the camera is mounted.
        pt (3-vector): world coordinates of point
        clip (bool, optional): if true, None will be returned if the point is
            outside of the viewing volume.

    Returns:
        tuple: (x,y,z), where x,y are pixel value of image, z is depth.
    """
    return camera_to_viewport(camera,robot).project(pt,clip)


def visible(camera,object,full=True,robot=None):
    """Tests whether the given object is visible in a SimRobotSensor or a
    GLViewport. 

    If you are doing this multiple times, first convert to GLViewport.

    Args:
        camera (SimRobotSensor or GLViewport): the camera.
        object: a 3-vector, a (center,radius) pair indicating a sphere, an
            axis-aligned bounding box (bmin,bmax), a Geometry3D, or an object
            that has a geometry() method, e.g., RigidObjectModel, RobotModelLink.
        full (bool, optional): if True, the entire object must be in the
            viewing frustum for it to be considered visible.  If False, any
            part of the object can be in the viewing frustum.
        robot (RobotModel): if camera is a SimRobotSensor, this will be used to
            derive the transform.
    """
    if isinstance(camera,SimRobotSensor):
        camera = camera_to_viewport(camera,robot)
    if hasattr(object,'geometry'):
        return visible(camera,object.geometry(),full,robot)
    if hasattr(object,'__iter__'):
        if not hasattr(object[0],'__iter__'):
            #vector
            if len(object) != 3:
                raise ValueError("Object must be a 3-vector")
            return camera.project(object) != None
        elif hasattr(object[1],'__iter__'):
            if len(object[0]) != 3 or len(object[1]) != 3:
                raise ValueError("Object must be a bounding box")
            bmin,bmax = object
            if not full:
                #test whether center is in bmin,bmax
                center = vectorops.interpolate(bmin,bmax,0.5)
                cproj = camera.project(center)
                if cproj is not None:
                    return True
                if all(a <= v <= b for (a,b,v) in zip(bmin,bmax,camera.getTransform()[1])):
                    return True

            points = [camera.project(bmin,full),camera.project(bmax,full)]
            pt = [bmin[0],bmin[1],bmax[2]]
            points.append(camera.project(pt,full))
            pt = [bmin[0],bmax[1],bmax[2]]
            points.append(camera.project(pt,full))
            pt = [bmin[0],bmax[1],bmin[2]]
            points.append(camera.project(pt,full))
            pt = [bmax[0],bmin[1],bmin[2]]
            points.append(camera.project(pt,full))
            pt = [bmax[0],bmin[1],bmax[2]]
            points.append(camera.project(pt,full))
            pt = [bmax[0],bmax[1],bmin[2]]
            points.append(camera.project(pt,full))
            if any(p is None for p in points):
                return False
            if full:
                return True
            if min(p[2] for p in points) > camera.clippingplanes[1]:
                return False
            if max(p[2] for p in points) < camera.clippingplanes[0]:
                return False
            points = [p for p in points if p[2] > 0]
            for p in points:
                if 0 <= p[0] <= camera.w and 0 <= p[1] <= camera.h:
                    return True
            #TODO: intersection of projected polygon
            return False
        else:
            #sphere
            if len(object[0]) != 3:
                raise ValueError("Object must be a sphere")
            c,r = object
            if full:
                cproj = camera.project(c,True)
                if cproj is None: return False
                rproj = camera.w/cproj[2]*r
                if cproj[2] - r < camera.clippingplanes[0] or cproj[2] + r > camera.clippingplanes[1]: return False
                return 0 <= cproj[0] - rproj and cproj[0] + rproj <= camera.w and 0 <= cproj[1] - rproj and cproj[1] + rproj <= camera.h
            else:
                cproj = camera.project(c,False)
                if cproj is None:
                    dist = r - vectorops.distance(camera.getTransform()[1],c) 
                    if dist >= camera.clippingplanes[0]:
                        return True
                    return False
                if 0 <= cproj[0] <= camera.w and 0 <= cproj[1] <= camera.h:
                    if cproj[2] + r > camera.clippingplanes[0] and cproj[2] - r < camera.clippingplanes[1]:
                        return True
                    return False
                rproj = camera.w/cproj[2]*r
                xclosest = max(min(cproj[0],camera.w),0)
                yclosest = max(min(cproj[1],camera.h),0)
                zclosest = max(min(cproj[2],camera.clippingplanes[1]),camera.clippingplanes[0])
                return vectorops.distance((xclosest,yclosest),cproj[0:2]) <= rproj
    from klampt import Geometry3D
    if not isinstance(object,Geometry3D):
        raise ValueError("Object must be a point, sphere, bounding box, or Geometry3D")
    return visible(camera,object.getBB(),full,robot)

