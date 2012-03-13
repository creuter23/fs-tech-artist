# zoomerate.py

import pymel.core as pm

def gui():
    '''
    Triggers the interface for zoomerate.
    '''
    
    # Warning this is causeing issues with 2012
    panel = pm.getPanel(wf=True)
    try:
        whichCam = pm.modelPanel(panel, q=1, camera=True)
    except RuntimeError:
        whichCam = pm.modelPanel('modelPanel4', q=1, camera=True)
        print 'Using: %s' % whichCam
        
    whichCamShape = pm.ls(whichCam, dag=True, shapes=True, ap=True)
    
    # Figure out what cameras to use when building the menu
    cameras = pm.ls(ca=True)
    diffCams = []
    diffCams.extend(whichCamShape)
    diffCams.extend(cameras)
    print diffCams, len(diffCams)
    
    win_name = 'zoomer_win2'
    if pm.window(win_name, ex=True):
        pm.deleteUI(win_name)
        
    win = pm.window(win_name, s=0, ip=True, iconName='zoomer', w=400, h=180,
                    t='Camera zoomeratro v1.0')
    main = pm.columnLayout()
    pm.frameLayout(borderVisible=True, labelVisible=True, labelAlign='cener', label='Zoom Options', marginWidth=5, marginHeight=5)
    pm.columnLayout()
    global which_cam_menu
    which_cam_menu = pm.optionMenuGrp(label='Camera to Zoom', cc=connect)
    pm.menuItem(label=whichCamShape[0])
    for i in xrange(len(diffCams)-1):
        pm.menuItem(label=cameras[i])
    
    horizontal_attr = '%s.horizontalFilmOffset' % whichCamShape[0]
    vertical_attr = '%s.verticalFilmOffset' % whichCamShape[0]
    overscan_attr = '%s.overscan' % whichCamShape[0]
    
    global horizontal_slider, vertical_slider, overscan_slider
    horizontal_slider = pm.floatSliderGrp(field=True, label='Horizontal', min=-3, max=3, pre=3, step=0.001)
    vertical_slider = pm.floatSliderGrp(field=True, label='Vertical', min=-3, max=3, pre=3, step=0.001)
    overscan_slider = pm.floatSliderGrp(field=True, label='Overscan', min=-3, max=3, pre=3, step=0.001)
    
    pm.connectControl(horizontal_slider, horizontal_attr)
    pm.connectControl(vertical_slider, vertical_attr)
    pm.connectControl(overscan_slider, overscan_slider)
    
    pm.button(label='Reset', c=reset)
    win.show()
 
def update(*args):
    reset_cam = which_cam_menu.getValue()
    print reset_cam
    horizontal_attr = '%s.horizontalFilmOffset' % reset_cam
    vertical_attr = '%s.verticalFilmOffset' % reset_cam
    overscan_attr = '%s.overscan' % reset_cam
    
    return horizontal_attr, vertical_attr, overscan_attr
     
def connect(*args):
    horizontal_attr, vertical_attr, overscan_attr = update()
    pm.connectControl(horizontal_slider, horizontal_attr)
    pm.connectControl(vertical_slider, vertical_attr)
    pm.connectControl(overscan_slider, overscan_attr)    

def reset(*args):
    horizontal_attr, vertical_attr, overscan_attr = update()
    pm.setAttr(horizontal_attr, 0)
    pm.setAttr(vertical_attr, 0)
    pm.setAttr(overscan_attr, 1)
    