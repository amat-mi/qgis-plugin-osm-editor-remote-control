#!python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from urllib import *
# initialize Qt resources from file resouces.py
import resources
class OSMEditorRemoteControlPlugin:
  def __init__(self, iface):
    self.iface = iface
  def initGui(self):
    self.action = QAction(QIcon(":/plugins/OSMEditorRemoteControl/icon.png"), "OSM Editor Remote Control", self.iface.mainWindow())
    self.action.setEnabled(False);
    self.action.setWhatsThis("Send remote control command to OSM editor to load data at current map view")
    self.action.setStatusTip("Send remote control command to OSM editor to load data at current map view")
    self.action.triggered.connect(self.run)
    self.iface.mapCanvas().layersChanged.connect(self.changeStatus);
    self.iface.mapCanvas().extentsChanged.connect(self.changeStatus);
    self.iface.addToolBarIcon(self.action)
  def unload(self):
    self.iface.removeToolBarIcon(self.action)
  def getLonLatExtent(self):
    extent = self.iface.mapCanvas().mapRenderer().extent()
    layer = self.iface.mapCanvas().currentLayer()
    crs_map = layer.crs()
    crs_4326 = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
    return QgsCoordinateTransform(crs_map, crs_4326).transform(extent)
  def changeStatus(self):
    if self.iface.mapCanvas().currentLayer() == None:
      self.action.setEnabled(False);
    else:
      extent = self.getLonLatExtent()
      self.action.setEnabled(extent.width() * extent.height() < 0.1)
  def run(self):
    extent = self.getLonLatExtent()
    url = 'http://localhost:8111/load_and_zoom?left=%f&right=%f&top=%f&bottom=%f' % (extent.xMinimum(), extent.xMaximum(), extent.yMaximum(), extent.yMinimum())
    print "OSMEditorRemoteControl plugin calling " + url
    try:
      urlopen(url)
    except IOError:
      QMessageBox.warning(self.iface.mainWindow(), "OSM Editor Remote Control Plugin", "Could not connect to the OSM editor. Did you start it?")
