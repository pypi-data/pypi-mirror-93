# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import pyCGM2
from viconnexusapi import ViconNexus
import numpy as np
import logging

try:
    from pyCGM2 import btk
except:
    logging.info("[pyCGM2] pyCGM2-embedded btk not imported")
    import btk


from pyCGM2.Tools import btkTools

# vicon nexus
try:
    import ViconNexus
except:
    from viconnexusapi import ViconNexus

from pyCGM2.Nexus import nexusTools,Devices
from pyCGM2.Utils import utils

NEXUS = ViconNexus.ViconNexus()

class NexusModelFilter(object):
    def __init__(self,NEXUS,iModel, iAcq, vskName,pointSuffix, staticProcessing = False ):
        """
            Constructor

            :Parameters:
                - `NEXUS` () - Nexus environment
                - `iModel` (pyCGM2.Model.CGM2.Model) - model instance
                - `vskName` (str) . subject name create in Nexus
                - `staticProcessingFlag` (bool`) : flag indicating only static model ouput will be export

        """
        self.m_model = iModel
        self.m_acq = iAcq
        self.m_vskName = vskName
        self.NEXUS = NEXUS
        self.staticProcessing = staticProcessing
        self.m_pointSuffix = pointSuffix if pointSuffix is None else "_"+pointSuffix

    def run(self):
        """
            method calling embedded-model method : viconExport
        """
        self.m_model.viconExport(self.NEXUS,self.m_acq, self.m_vskName,self.m_pointSuffix,self.staticProcessing)



class NexusConstructAcquisitionFilter(object):
    def __init__(self,dataPath,filenameNoExt,subject):

        """
        """
        self.m_dataPath = dataPath
        self.m_filenameNoExt = filenameNoExt
        self.m_subject = subject

        self.m_framerate = NEXUS.GetFrameRate()
        #self.m_frames = NEXUS.GetTrialRange()[1]
        self.m_rangeROI = NEXUS.GetTrialRegionOfInterest()
        self.m_trialRange = NEXUS.GetTrialRange()
        self.m_trialFirstFrame = self.m_trialRange[0] # might be different from 1 if corpped and no x2d

        self.m_firstFrame = self.m_rangeROI[0]
        self.m_lastFrame = self.m_rangeROI[1]
        self.m_frames = self.m_lastFrame-(self.m_firstFrame-1)



        deviceIDs = NEXUS.GetDeviceIDs()
        self.m_analogFrameRate = NEXUS.GetDeviceDetails(deviceIDs[0])[2] if ( len(deviceIDs) > 0 ) else self.m_framerate


        self.m_numberAnalogSamplePerFrame = int(self.m_analogFrameRate/self.m_framerate)
        self.m_analogFrameNumber = self.m_frames * self.m_numberAnalogSamplePerFrame


        self.m_nexusForcePlates = list()
        self.m_nexusAnalogDevices = list()


        if( len(deviceIDs) > 0 ):
            for deviceID in deviceIDs:
                if NEXUS.GetDeviceDetails( deviceID )[1] == "ForcePlate":
                    self.m_nexusForcePlates.append( Devices.ForcePlate(deviceID))
                else:
                    self.m_nexusAnalogDevices.append(Devices.AnalogDevice(deviceID))


        self.m_acq = btk.btkAcquisition()
        self.m_acq.Init(0, int(self.m_frames),0, self.m_numberAnalogSamplePerFrame)
        self.m_acq.SetPointFrequency(self.m_framerate)
        self.m_acq.SetFirstFrame(self.m_firstFrame)


    def appendEvents(self):


        eventType = "Foot Strike"
        eventContext = "Left"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Automatic)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)


        eventType = "Foot Off"
        eventContext = "Left"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Automatic)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)

        eventType = "Foot Strike"
        eventContext = "Right"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Automatic)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)

        eventType = "Foot Off"
        eventContext = "Right"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Automatic)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)

        eventType = "Event"
        eventContext = "General"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Manual)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)

        eventType = "Left-FP"
        eventContext = "General"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Manual)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)


        eventType = "Right-FP"
        eventContext = "General"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Manual)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)


        eventType = "Start"
        eventContext = "Left"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Manual)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)


        eventType = "End"
        eventContext = "Left"
        if NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0] != []:
            for frame in NEXUS.GetEvents(self.m_subject,eventContext,eventType)[0]:
                if frame>=self.m_firstFrame and frame<=self.m_lastFrame:
                    time = (frame-1)/self.m_framerate
                    ev = btk.btkEvent(eventType,time, int(frame), eventContext, btk.btkEvent.Manual)
                    ev.SetSubject(self.m_subject)
                    self.m_acq.AppendEvent(ev)



    def appendMarkers(self):

        markersLoaded = NEXUS.GetMarkerNames(self.m_subject)
        markers =[]
        for i in range(0,len(markersLoaded)):
            data = NEXUS.GetTrajectory(self.m_subject,markersLoaded[i])
            if data != ([],[],[],[]):
                markers.append(markersLoaded[i])


        for marker in markers:
            rawDataX, rawDataY, rawDataZ, E = NEXUS.GetTrajectory(self.m_subject,marker)

            E = np.asarray(E).astype("float")-1
            values =np.array([np.asarray(rawDataX),np.asarray(rawDataY),np.asarray(rawDataZ)]).T

            start = self.m_firstFrame - self.m_trialFirstFrame
            end = self.m_lastFrame - self.m_trialFirstFrame

            values_cut = values[start:end+1,:]
            E_cut = E[start:end+1]


            btkTools.smartAppendPoint(self.m_acq,marker,values_cut, PointType=btk.btkPoint.Marker,desc="",
                                      residuals=E_cut)

    def appendAnalogs(self):

        ftr = NEXUS.GetTrialRange()[0]

        for nexusAnalogDevice in self.m_nexusAnalogDevices:

            start = self.m_firstFrame - 1#self.m_trialFirstFrame
            end = self.m_lastFrame - 1#self.m_trialFirstFrame

            channels = nexusAnalogDevice.getChannels()
            for channel in channels:
                analog = btk.btkAnalog()
                analog.SetLabel(channel.getLabel())
                analog.SetUnit(channel.getUnit())
                analog.SetFrameNumber(self.m_analogFrameNumber)
                analog.SetValues(channel.getValues()[start*self.m_numberAnalogSamplePerFrame:(end+1)*self.m_numberAnalogSamplePerFrame])
                analog.SetDescription(channel.getDescription())

                self.m_acq.AppendAnalog(analog)

    def appendForcePlates(self):

        forcePlateNumber = len(self.m_nexusForcePlates)

        fp_count=0
        for nexusForcePlate in self.m_nexusForcePlates:
            forceLocal = nexusForcePlate.getLocalReactionForce() #  row number =  NEXUS.getTrialRange[1] not FrameCount
            momentLocal = nexusForcePlate.getLocalReactionMoment()


            start = self.m_firstFrame - 1 #-1 because Nexus frame start at 1
            end = self.m_lastFrame -1#- self.m_trialFirstFrame

            forceLabels =["Force.Fx"+str(fp_count+1), "Force.Fy"+str(fp_count+1),"Force.Fz"+str(fp_count+1)]
            for j in range(0,3):
                analog = btk.btkAnalog()
                analog.SetLabel(forceLabels[j])
                analog.SetUnit("N")#nexusForcePlate.getForceUnit())
                analog.SetFrameNumber(self.m_analogFrameNumber)
                analog.SetValues(forceLocal[(start)*self.m_numberAnalogSamplePerFrame:(end+1)*self.m_numberAnalogSamplePerFrame,j])
                analog.SetDescription(nexusForcePlate.getDescription())
                #analog.SetGain(btk.btkAnalog.PlusMinus10)

                self.m_acq.AppendAnalog(analog)

            momentLabels =["Moment.Mx"+str(fp_count+1), "Moment.My"+str(fp_count+1),"Moment.Mz"+str(fp_count+1)]
            for j in range(0,3):
                analog = btk.btkAnalog()
                analog.SetLabel(momentLabels[j])
                analog.SetUnit("Nmm")#nexusForcePlate.getMomentUnit())
                analog.SetFrameNumber(self.m_analogFrameNumber)
                analog.SetValues(momentLocal[(start)*self.m_numberAnalogSamplePerFrame:(end+1)*self.m_numberAnalogSamplePerFrame,j])
                analog.SetDescription(nexusForcePlate.getDescription())
                #analog.GetGain(btk.btkAnalog.PlusMinus10)
                self.m_acq.AppendAnalog(analog)

            fp_count+=1

        # metadata for platform type2
        md_force_platform = btk.btkMetaData('FORCE_PLATFORM')
        btk.btkMetaDataCreateChild(md_force_platform, "USED", int(forcePlateNumber))# a
        btk.btkMetaDataCreateChild(md_force_platform, "ZERO", [1,0]) #
        btk.btkMetaDataCreateChild(md_force_platform, "TYPE", btk.btkDoubleArray(forcePlateNumber, 2)) #btk.btkDoubleArray(forcePlateNumber, 2))# add a child

        self.m_acq.GetMetaData().AppendChild(md_force_platform)


        origins = []
        for nexusForcePlate in self.m_nexusForcePlates:
            origins.append(-1.0*nexusForcePlate.getLocalOrigin())

        md_origin = btk.btkMetaData('ORIGIN')
        md_origin.SetInfo(btk.btkMetaDataInfo([3,int(forcePlateNumber)], np.concatenate(origins)))
        md_force_platform.AppendChild(md_origin)


        corners = []
        for nexusForcePlate in self.m_nexusForcePlates:
            corners.append(nexusForcePlate.getCorners().T.flatten())

        md_corners = btk.btkMetaData('CORNERS')
        md_corners.SetInfo(btk.btkMetaDataInfo([3,4,int(forcePlateNumber)], np.concatenate(corners)))
        md_force_platform.AppendChild(md_corners)

        md_channel = btk.btkMetaData('CHANNEL')
        md_channel.SetInfo(btk.btkMetaDataInfo([6,int(forcePlateNumber)], np.arange(1,int(forcePlateNumber)*6+1).tolist()))
        md_force_platform.AppendChild(md_channel)


    def appendModelOutputs(self):

        modelOutputNames = NEXUS.GetModelOutputNames(self.m_subject)

        if modelOutputNames!=[]:
            for modelOutputName in modelOutputNames:
                data, E = NEXUS.GetModelOutput(self.m_subject,modelOutputName)
                type = NEXUS.GetModelOutputDetails(self.m_subject,modelOutputName)[0]

                if type in ["Angles","Forces","Moments","Powers", "Modeled Markers"]:

                    E = np.asarray(E).astype("float")-1
                    values =np.array([np.asarray(data[0]),np.asarray(data[1]),np.asarray(data[2])]).T


                    start = self.m_firstFrame - self.m_trialFirstFrame
                    end = self.m_lastFrame - self.m_trialFirstFrame

                    values_cut = values[start:end+1,:]
                    E_cut = E[start:end+1]


                    if type == "Angles":
                        btkTools.smartAppendPoint(self.m_acq,modelOutputName,values_cut, PointType=btk.btkPoint.Angle,desc="",
                                                  residuals=E_cut)
                    elif type == "Forces":
                        btkTools.smartAppendPoint(self.m_acq,modelOutputName,values_cut, PointType=btk.btkPoint.Force,desc="",
                                                  residuals=E_cut)
                    elif type == "Moments":
                        btkTools.smartAppendPoint(self.m_acq,modelOutputName,values_cut, PointType=btk.btkPoint.Moment,desc="",
                                                  residuals=E_cut)
                    elif type == "Powers":
                        btkTools.smartAppendPoint(self.m_acq,modelOutputName,values_cut, PointType=btk.btkPoint.Power,desc="",
                                                  residuals=E_cut)
                    elif type == "Modeled Markers":
                        btkTools.smartAppendPoint(self.m_acq,modelOutputName,values_cut, PointType=btk.btkPoint.Marker,desc="",
                                                  residuals=E_cut)
                    else:
                        logging.warning("[pyCGM2] : type unknown")

                else:
                    logging.warning("[pyCGM2] : Model Output (%s) from Nexus not added to the btk acquisition"%(modelOutputName))



    def build(self):
        self.appendEvents()
        self.appendMarkers()
        if self.m_nexusForcePlates !=[]: self.appendForcePlates()
        if self.m_nexusAnalogDevices !=[]:self.appendAnalogs()
        self.appendModelOutputs()


        return self.m_acq

    def exportC3d(self,filenameNoExt=None):

        if filenameNoExt is None:
            btkTools.smartWriter(self.m_acq,self.m_dataPath+self.m_filenameNoExt+".c3d")
        else:
            btkTools.smartWriter(self.m_acq,self.m_dataPath+filenameNoExt+".c3d")
