from ..visualization import _globalLock,VisualizationScene
from .. import glcommon
import weakref
import time
from collections import defaultdict

from OpenGL.GL import *

class WindowInfo:
    """Mode can be hidden, shown, or dialog"""
    def __init__(self,name,frontend,glwindow=None):
        self.name = name
        self.frontend = frontend
        self.glwindow = glwindow
        self.mode = 'hidden'
        self.guidata = None
        self.custom_ui = None
        self.doRefresh = False
        self.doReload = False
        #needed for GLUT to work properly with multiple windows
        self.worlds = []
        self.active_worlds = []
        self.worldDisplayListItems = defaultdict(list)


class GLVisualizationFrontend(glcommon.GLPluginProgram):
    def __init__(self):
        glcommon.GLPluginProgram.__init__(self)
        self.scene = GLVisualizationPlugin()
        self.setPlugin(self.scene)
        self.scene.program = weakref.proxy(self)
        self.rendered = False

    def addAction(self,hook,short_text,key,description):
        self.add_action(hook,short_text,key,description)

    def displayfunc(self):
        glcommon.GLPluginProgram.displayfunc(self)
        self.rendered = True


class GLVisualizationPlugin(glcommon.GLWidgetPlugin,VisualizationScene):
    def __init__(self):
        glcommon.GLWidgetPlugin.__init__(self)
        VisualizationScene.__init__(self)
        #need to set this to a weakref of the GLProgram being used with this plugin. Automatically done in GLVisualizationFrontend()
        self.program = None
        self.backgroundImage = None
        self.backgroundImageTexture = None
        self.backgroundImageDisplayList = None

    def initialize(self):
        #keep or refresh display lists?
        #self._clearDisplayLists()
        return glcommon.GLWidgetPlugin.initialize(self)

    def getViewport(self):
        return self.view

    def setViewport(self,viewport):
        self.program.set_view(viewport)

    def setBackgroundColor(self,r,g,b,a=1): 
        if self.program is not None:
            self.program.clearColor = [r,g,b,a]
        else:
            print("setBackgroundColor(): doesn't work yet because scene is not bound to a window")

    def edit(self,name,doedit=True):
        global _globalLock
        _globalLock.acquire()
        obj = self.getItem(name)
        if obj is None:
            _globalLock.release()
            raise ValueError("Object "+name+" does not exist in visualization")
        if doedit:
            world = self.items.get('world',None)
            if world is not None:
                world=world.item
            obj.make_editor(world)
            if obj.editor:
                self.klamptwidgetmaster.add(obj.editor)
        else:
            if obj.editor:
                self.klamptwidgetmaster.remove(obj.editor)
                obj.remove_editor()
        self.doRefresh = True
        _globalLock.release()

    def displayfunc(self):
        if self.backgroundImage is not None:
            (img,rows,cols,pixformat)= self.backgroundImage
            if self.backgroundImageTexture is None:
                self.backgroundImageTexture = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.backgroundImageTexture)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
                glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            else:
                glBindTexture(GL_TEXTURE_2D, self.backgroundImageTexture)
            
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, cols, rows, 0, pixformat, GL_UNSIGNED_BYTE, img)
            glBindTexture(GL_TEXTURE_2D, 0)
            self.backgroundImage = None
        if self.backgroundImageTexture is not None:
            self.program.prepare_GL()
            glMatrixMode(GL_PROJECTION)
            glDisable(GL_CULL_FACE)
            glLoadIdentity()
            glOrtho(0,1,1,0,-1,1);
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glDisable(GL_DEPTH_TEST)
            glDepthMask(GL_FALSE)
            glEnable(GL_TEXTURE_2D)
            glDisable(GL_LIGHTING)
            glTexEnvi(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE);
            if self.backgroundImageDisplayList is not None:
                self.backgroundImageDisplayList.draw(self.drawBackgroundImage)
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_CULL_FACE)
            glEnable(GL_LIGHTING)
            glEnable(GL_DEPTH_TEST)
            glDepthMask(GL_TRUE)

            #do the rest of displayfunc -- but prepare_GL does a clear
            #self.program.prepare_GL()
            self.program.set_lights_GL()
            self.program.view.set_current_GL()
            self.display()
            self.program.prepare_screen_GL()
            self.display_screen()
            return True
        return False

    def display(self):
        global _globalLock
        with _globalLock:
            #for items currently being edited AND having the appearance changed, draw the reference object
            #according to the vis settings
            #glcommon.GLWidgetPlugin.display(self)
            #restore any reference objects
            self.updateCamera()
            self.renderGL(self.view)

    def setBackgroundImage(self,img,format='auto',rows='auto'):
        """Sets an image to go underneath the OpenGL rendering.

        img must be a list of bytes or numpy array.  If it has shape w x h x 3, it
        is assumed to have rgb information as channels.  If it has shape w x h, it
        is assumed to have rgb information as integers 0xrrggbb by default. 
        If format='bgr', then the rgb information is assumed to be integers 0xbbggrr.

        If img == None, then the background image is cleared
        """
        global _globalLock
        if img is None:
            with _globalLock:
                self.backgroundImage = None
                if self.backgroundImageDisplayList is not None:
                    self.backgroundImageDisplayList.destroy()
                self.backgroundImageDisplayList = None
                if self.backgroundImageTexture is not None:
                    glDeleteTextures([self.backgroundImageTexture])
                self.backgroundImageTexture = None
            return
            
        pixformat = GL_RGBA
        if hasattr(img,'shape'):
            import numpy as np
            if len(img.shape) == 3:
                rows = img.shape[0]
                cols = img.shape[1]
                assert img.shape[2] == 3
                if img.dtype == np.uint8:
                    img = img.tobytes()
                else:
                    img = (img*255.0).convert(dtype=np.uint8).tobytes()
                pixformat = GL_RGB
            else:
                assert len(img.shape)==2
                rows = img.shape[0]
                cols = img.shape[1]
                img = img.tobytes()
                if format == 'bgr':
                    pixformat = GL_BGRA
        else:
            pixels = img
            assert rows != 'auto'
            pixformat = GL_RGB
            pixsize = 3
            if format == 'bgr':
                pixformat = GL_BGR
            elif format == 'rgba':
                pixsize = 4
                pixformat = GL_RGBA
            elif format == 'bgra':
                pixsize = 4
                pixformat = GL_BGRA
            cols = len(img) // (rows*pixsize)

        with _globalLock:
            self.backgroundImage = (img,rows,cols,pixformat)
            if self.backgroundImageDisplayList is None:
                self.backgroundImageDisplayList = glcommon.CachedGLObject()
            else:
                self.backgroundImageDisplayList.markChanged()

    def drawBackgroundImage(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.backgroundImageTexture)
        glBegin(GL_TRIANGLE_FAN)
        glTexCoord2f(0,0)
        glVertex2f(0,0)
        glTexCoord2f(1,0)
        glVertex2f(1,0)
        glTexCoord2f(1,1)
        glVertex2f(1,1)
        glTexCoord2f(0,1)
        glVertex2f(0,1)
        glEnd()

    def widgetchangefunc(self,edit):
        """Called by GLWidgetPlugin on any widget change"""
        for name,item in self.items.items():
            item.update_editor()

    def display_screen(self):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.display_screen(self)
        self.renderScreenGL(self.view,self.window)
        _globalLock.release()

    def reshapefunc(self,w,h):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.reshapefunc(self,w,h)
        _globalLock.release()
    def keyboardfunc(self,c,x,y):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.keyboardfunc(self,c,x,y)
        _globalLock.release()
    def keyboardupfunc(self,c,x,y):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.keyboardupfunc(self,c,x,y)
        _globalLock.release()
    def mousefunc(self,button,state,x,y):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.mousefunc(self,button,state,x,y)
        _globalLock.release()
    def motionfunc(self,x,y,dx,dy):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.motionfunc(self,x,y,dx,dy)
        _globalLock.release()
    def eventfunc(self,type,args=""):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.eventfunc(self,type,args)
        _globalLock.release()
    def closefunc(self):
        global _globalLock
        _globalLock.acquire()
        glcommon.GLWidgetPlugin.closefunc(self)
        _globalLock.release()

    def idle(self):
        global _globalLock
        _globalLock.acquire()
        VisualizationScene.updateTime(self,time.time())
        _globalLock.release()
        return False


