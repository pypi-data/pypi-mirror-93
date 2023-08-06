# -*- coding: utf-8 -*-
#import ipdb
import matplotlib.pyplot as plt
import numpy as np
from pyCGM2.Report import plot, plotFilters, plotViewers, normativeDatasets, emgPlotViewers, ComparisonPlotViewers
from pyCGM2.Processing import scores
from pyCGM2.Tools import btkTools
from pyCGM2 import enums

def plotTemporalKinematic(DATA_PATH, modelledFilenames,bodyPart, pointLabelSuffix=None, exportPdf=False,outputName=None,show=True,title=None,
                          btkAcq=None,exportPng=False):
    """
    plotTemporalKinematic : display temporal trace of the Kinematics

    :param DATA_PATH [str]: path to your data
    :param modelledFilenames [string list]: c3d files
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]: name of the output filed
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    :param btkAcq [Btk::Acquisition]: force use of an openma trial instance


    Examples:

    """

    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")

    if exportPdf or exportPng:
        if outputName is None:
            filenameOut =  modelledFilenames+"-Temporal Kinematics ["+ bodyPart.name+"]"
        else:
            filenameOut =  outputName+"-Temporal Kinematics ["+ bodyPart.name+"]"

    if btkAcq is not None:
        acq = btkAcq
        btkTools.sortedEvents(acq)
    else:
        acq =btkTools.smartReader(DATA_PATH + modelledFilenames)

    kv = plotViewers.TemporalKinematicsPlotViewer(acq,pointLabelSuffix=pointLabelSuffix,bodyPart = bodyPart)
    # # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if title is not None: pf.setTitle(title+"-Temporal Kinematics ["+ bodyPart.name+"]")
    if exportPdf :pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()

    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plotTemporalKinetic(DATA_PATH, modelledFilenames,bodyPart,pointLabelSuffix=None,exportPdf=False,outputName=None,show=True,title=None,
                        btkAcq=None,exportPng=False):

    """
    plotTemporalKinetic : display temporal trace of the Kinetics


    :param DATA_PATH [str]: path to your data
    :param modelledFilenames [string list]: c3d files
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]: name of the output filed
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    :param btkAcq [Btk::Acquisition]: force use of an openma trial instance

    Examples:

    """

    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")

    if exportPdf or exportPng:
        if outputName is None:
            filenameOut =  modelledFilenames+"-Temporal Kinetics["+ bodyPart.name+"]"
        else:
            filenameOut =  outputName+"-Temporal Kinetics ["+ bodyPart.name+"]"

    if btkAcq is not None:
        acq = btkAcq
        btkTools.sortedEvents(acq)

    else:
        acq =btkTools.smartReader(DATA_PATH+modelledFilenames)

    kv = plotViewers.TemporalKineticsPlotViewer(acq,pointLabelSuffix=pointLabelSuffix,bodyPart = bodyPart)
    # # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if title is not None: pf.setTitle(title+"-Temporal Kinetics ["+ bodyPart.name+"]")
    if exportPdf :pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()

    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plotTemporalEMG(DATA_PATH, processedEmgfile, emgChannels, muscles, contexts, normalActivityEmgs, rectify = True,
                    exportPdf=False,outputName=None,show=True,title=None,
                    btkAcq=None,ignoreNormalActivity= False,exportPng=False,OUT_PATH=None):
    """
    plotTemporalEMG : display temporal trace of EMG signals


    :param DATA_PATH [str]: path to your data
    :param processedEmgfile [string]: c3d file
    :param emgChannels [string list]: labels of your emg channels
    :param muscles [string list]: muscle labels associated with your emg channels
    :param contexts [string list]: contexts associated with your emg channel
    :param normalActivityEmgs [string list]: normal activities associated with your emg channels
    :param btkAcq [Btk::Acquisition]: force use of an openma trial instance


    **optional**

    :param rectify [bool]:  plot rectify signals (True[default])
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]: name of the output filed
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """

    if OUT_PATH is None:
        OUT_PATH = DATA_PATH

    if btkAcq is not None:
        acq = btkAcq
    else:
        acq =btkTools.smartReader(DATA_PATH+processedEmgfile)


    emgChannels_list=  [emgChannels[i:i+10] for i in range(0, len(emgChannels), 10)]
    contexts_list =  [contexts[i:i+10] for i in range(0, len(contexts), 10)]
    muscles_list =  [muscles[i:i+10] for i in range(0, len(muscles), 10)]
    normalActivityEmgs_list =  [normalActivityEmgs[i:i+10] for i in range(0, len(normalActivityEmgs), 10)]

    pageNumber = len(emgChannels_list)

    figs=list()
    outfilenames=list()

    count = 0
    for i in range(0,pageNumber):

        if exportPdf and pageNumber>1:
            if outputName is None:
                filenameOut =  processedEmgfile+"-TemporalEmgPlot"+"[rectify]-"+count if rectify else processedEmgfile+"-TemporalEmgPlot"+"[raw]-"+count
            else:
                filenameOut =  outputName+"-TemporalEmgPlot"+"[rectify]-"+count if rectify else title+"-TemporalEmgPlot"+"[raw]-"+count
        else:
            if outputName is None:
                filenameOut =  processedEmgfile+"-TemporalEmgPlot"+"[rectify]" if rectify else processedEmgfile+"-TemporalEmgPlot"+"[raw]"
            else:
                filenameOut =  outputName+"-TemporalEmgPlot"+"[rectify]" if rectify else title+"-TemporalEmgPlot"+"[raw]"

        combinedEMGcontext=[]
        for j in range(0,len(emgChannels_list[i])):
            combinedEMGcontext.append([emgChannels_list[i][j],contexts_list[i][j], muscles_list[i][j]])

        # # viewer
        kv = emgPlotViewers.TemporalEmgPlotViewer(acq)
        kv.setEmgs(combinedEMGcontext)
        kv.setNormalActivationLabels(normalActivityEmgs_list[i])
        kv.ignoreNormalActivty(ignoreNormalActivity)
        kv. setEmgRectify(rectify)

        # # filter

        pf = plotFilters.PlottingFilter()
        pf.setViewer(kv)
        if title is not None:
            if pageNumber>1:
                pf.setTitle(title+"-TemporalEmgPlot"+"[rectify]-"+count if rectify else title+"-TemporalEmgPlot"+"[raw]-"+count)
            else:
                pf.setTitle(title+"-TemporalEmgPlot"+"[rectify]" if rectify else title+"-TemporalEmgPlot"+"[raw]")
        if exportPdf :pf.setExport(OUT_PATH,filenameOut,"pdf")
        fig = pf.plot()

        if exportPng:
            fig.savefig(OUT_PATH+filenameOut+".png")

        if exportPng:
            outfilenames.append(filenameOut+".png")

        figs.append(fig)

        count+=1
    if show: plt.show()

    if exportPng:
        return figs,outfilenames
    else:
        return figs

def plotDescriptiveEnvelopEMGpanel(DATA_PATH,analysis, emgChannels, muscles,contexts, normalActivityEmgs, normalized=False,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):

    """
    plotDescriptiveEnvelopEMGpanel : display average and standard deviation of time-normalized traces of EMG envelops


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param emgChannels [string list]: labels of your emg channels
    :param muscles [string list]: muscle labels associated with your emg channels
    :param contexts [string list]: contexts associated with your emg channels
    :param normalActivityEmgs [string list]: normal emg activities associated with your emg channels


    **optional**

    :param normalized [bool]: plot normalized amplitude envelops (False[default])
    :param type [string]:  display gait events (other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """

    if outputName is None:
        outputName = "PyCGM2-Analysis"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-DescriptiveEmgEnv"+"[No Normalized]-" if not normalized else outputName+"-DescriptiveEmgEnv"+"[Normalized]"

    # viewer
    combinedEMGcontext=[]
    for i in range(0,len(emgChannels)):
        combinedEMGcontext.append([emgChannels[i],contexts[i], muscles[i]])


    kv = emgPlotViewers.EnvEmgGaitPlotPanelViewer(analysis)
    kv.setEmgs(combinedEMGcontext)
    kv.setNormalActivationLabels(normalActivityEmgs)
    kv.setNormalizedEmgFlag(normalized)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot)
    else:
        kv.setConcretePlotFunction(plot.descriptivePlot)

    # # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)

    if exportPdf :pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()

    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plotConsistencyEnvelopEMGpanel(DATA_PATH,analysis, emgChannels,muscles, contexts, normalActivityEmgs, normalized=False,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):

    """
    plotConsistencyEnvelopEMGpanel : display all cycle of time-normalized traces of EMG envelops


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param emgChannels [string list]: labels of your emg channels
    :param muscles [string list]: muscle labels associated with your emg channels
    :param contexts [string list]: contexts associated with your emg channels
    :param normalActivityEmgs [string list]: normal activities associated with your emg channels


    **optional**

    :param normalized [bool]: (**default**: False) plot normalized amplitude envelops
    :param type [string]:  display gait events ( other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """

    if outputName is None:
        outputName = "PyCGM2-Analysis"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-ConsistencyEmgEnv"+"[No Normalized]-" if not normalized else outputName+"-DescriptiveEmgEnv"+"[Normalized]"

    # viewer
    combinedEMGcontext=[]
    for i in range(0,len(emgChannels)):
        combinedEMGcontext.append([emgChannels[i],contexts[i], muscles[i]])


    kv = emgPlotViewers.EnvEmgGaitPlotPanelViewer(analysis)
    kv.setEmgs(combinedEMGcontext)
    kv.setNormalActivationLabels(normalActivityEmgs)
    kv.setNormalizedEmgFlag(normalized)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitConsistencyPlot)
    else:
        kv.setConcretePlotFunction(plot.consistencyPlot)

    # # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if title is not None: pf.setTitle( title+"-ConsistencyEmgEnv"+"[No Normalized]-" if not normalized else title+"-DescriptiveEmgEnv"+"[Normalized]")
    if exportPdf :pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()

    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig


def plot_spatioTemporal(DATA_PATH,analysis,exportPdf=False,outputName=None,show=True,title=None,exportPng=False):
    """
    plot_spatioTemporal : display spatio-temporal parameters as horizontal histogram


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance

    **optional**

    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel

    """

    if outputName is None:  outputName = "pyCGM2-analysis"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-SpatioTemporal parameters"

    stpv = plotViewers.SpatioTemporalPlotViewer(analysis)
    stpv.setNormativeDataset(normativeDatasets.NormalSTP())

    # filter
    stppf = plotFilters.PlottingFilter()
    stppf.setViewer(stpv)
    if title is not None: stppf.setTitle(title+"-SpatioTemporal parameters")
    if exportPdf: stppf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = stppf.plot()

    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plot_DescriptiveKinematic(DATA_PATH,analysis,bodyPart,normativeDataset,pointLabelSuffix=None,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):
    """
    plot_DescriptiveKinematic : display average and standard deviation of time-normalized kinematic outputs


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param type [string]:  display gait events ( other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel

    """


    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")


    if outputName is None:
        outputName = "pyCGM2-analysis ["+ bodyPart.name+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-descriptive Kinematics ["+ bodyPart.name+"]"


    # filter 1 - descriptive kinematic panel
    #-------------------------------------------
    # viewer

    kv = plotViewers.NormalizedKinematicsPlotViewer(analysis,pointLabelSuffix=pointLabelSuffix,bodyPart=bodyPart)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot)
    else:
        kv.setConcretePlotFunction(plot.descriptivePlot)


    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if title is not None: pf.setTitle(title+"-descriptive Kinematics ["+ bodyPart.name+"]")
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig


def plot_ConsistencyKinematic(DATA_PATH,analysis,bodyPart,normativeDataset,pointLabelSuffix=None,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):

    """
    plot_ConsistencyKinematic : display all gait cycle of time-normalized kinematic outputs


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param type [string]:  display gait events ( other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """
    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")


    if outputName is None:
        outputName = "PyCGM2-Analysis ["+ bodyPart.name+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-consistency Kinematics ["+ bodyPart.name+"]"


    kv = plotViewers.NormalizedKinematicsPlotViewer(analysis,pointLabelSuffix=pointLabelSuffix,bodyPart=bodyPart)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitConsistencyPlot)
    else:
        kv.setConcretePlotFunction(plot.consistencyPlot)


    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-consistency  Kinematics ["+ bodyPart.name+"]")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plot_DescriptiveKinetic(DATA_PATH,analysis,bodyPart,normativeDataset,pointLabelSuffix=None,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):
    """
    plot_DescriptiveKinetic : display average and standard deviation of time-normalized kinetic outputs


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param type [string]:  display gait events ( other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """

    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")


    if outputName is None:
        outputName = "PyCGM2-Analysis ["+ bodyPart.name+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-descriptive Kinetics ["+ bodyPart.name+"]"

    kv = plotViewers.NormalizedKineticsPlotViewer(analysis,pointLabelSuffix=pointLabelSuffix,bodyPart=bodyPart)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot)
    else:
        kv.setConcretePlotFunction(plot.descriptivePlot)



    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-descriptive  Kinetics ["+ bodyPart.name+"]")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plot_ConsistencyKinetic(DATA_PATH,analysis,bodyPart, normativeDataset,pointLabelSuffix=None,type="Gait",exportPdf=False,outputName=None,show=True,title=None,exportPng=False):
    """
    plot_ConsistencyKinetic : display all gait cycle of time-normalized kinetic outputs


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param pointLabelSuffix [string]: suffix previously added to your model outputs
    :param type [string]:  display gait events ( other choice than gait [default], display foot strikes only)
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """
    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")

    if outputName is None:
        outputName = "PyCGM2-Analysis ["+ bodyPart.name+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-consistency Kinetics ["+ bodyPart.name+"]"

    kv = plotViewers.NormalizedKineticsPlotViewer(analysis,pointLabelSuffix=pointLabelSuffix,bodyPart=bodyPart)

    if type == "Gait":
        kv.setConcretePlotFunction(plot.gaitConsistencyPlot)
    else:
        kv.setConcretePlotFunction(plot.consistencyPlot)

    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-consistency  Kinetics ["+ bodyPart.name+"]")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def plot_MAP(DATA_PATH,analysis,normativeDataset,exportPdf=False,outputName=None,pointLabelSuffix=None,show=True,title=None,exportPng=False):
    """
    plot_MAP : display the Movement Analysis Profile


    :param DATA_PATH [str]: path to your data
    :param analysis [pyCGM2.Processing.analysis.Analysis]: pyCGM2 analysis instance
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance


    **optional**

    :param pointLabelSuffix [string]: (None) suffix added to outputs
    :param exportPdf [bool]: save as pdf (False[default])
    :param outputName [string]:  name of your pdf file (None[default] export your pdf with name : Global Analysis)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    """
    if outputName is None:
        outputName = "PyCGM2-Analysis"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-Map"

    #compute
    gps =scores.CGM1_GPS(pointSuffix=pointLabelSuffix)
    scf = scores.ScoreFilter(gps,analysis, normativeDataset)
    scf.compute()

    #plot
    kv = plotViewers.GpsMapPlotViewer(analysis,pointLabelSuffix=pointLabelSuffix)

    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-Map")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def compareKinematic(DATA_PATH,analyses,legends,context,bodyPart,normativeDataset,plotType="Descriptive",type="Gait",pointSuffixes=None,show=True,title=None,outputName=None,exportPng=False,exportPdf=False):
    """
    compareKinematic : compare kinematics of two pyCGM2 analysis instances


    :param analysis [pyCGM2.Processing.analysis.Analysis list]: list of pyCGM2 analysis instances
    :param legends [string list]: legend of each analysis instance
    :param context [string]: gait context ( choice: Left, Right)
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param plotType [string]: trace type ( Descriptive [default] or Consistency)
    :param type [string]:  display events  (Gait [defaut] or None)

    :example:

    >>> normativeData = normativeDatasets.Schwartz2008("Free")
    >>> plot.compareKinematic([analysisPre,analysisPost],["pre","post"],"Left","LowerLimb",normativeData)
    """
    if outputName is None:
        outputName = "pyCGM2-Comparison"+"-"+context+" ["+ bodyPart+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-"+context+" ["+ bodyPart+"]"+"- Kinematics Comparison"

    i=1
    for analysis in analyses:
        if analysis.kinematicStats.data == {}:
            raise Exception("[pyCGM2]: Kinetic comparison aborted. Analysis [%i] has no kinematic data"%(i))
        i+=1


    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")

    kv = ComparisonPlotViewers.KinematicsPlotComparisonViewer(analyses,context,legends,bodyPart=bodyPart,pointLabelSuffix_lst=pointSuffixes)

    if plotType == "Descriptive":
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot ) if type =="Gait" else kv.setConcretePlotFunction(plot.descriptivePlot )
    elif plotType == "Consistency":
        kv.setConcretePlotFunction(plot.gaitConsistencyPlot ) if type =="Gait" else kv.setConcretePlotFunction(plot.consistencyPlot )


    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if title is not None: pf.setTitle(title+"-Kinematic comparison")
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def compareKinetic(DATA_PATH,analyses,legends,context,bodyPart,normativeDataset,plotType="Descriptive",type="Gait",pointSuffixes=None,show=True,title=None,outputName=None,exportPng=False,exportPdf=False):

    """
    compareKinetic : compare kinetics of two pyCGM2 analysis instances


    :param analysis [pyCGM2.Processing.analysis.Analysis list]: list of pyCGM2 analysis instances
    :param legends [string list]: legend of each analysis instance
    :param context [string]: gait context (choice: Left, Right)
    :param bodyPart [str]: body part (choice : LowerLimb, Trunk, UpperLimb)
    :param normativeDataset [pyCGM2.Report.normativeDatasets]: pyCGM2 normative dataset instance

    **optional**

    :param plotType [string]: trace type ( Descriptive [default] or Consistency)
    :param type [string]:  display events (Gait [defaut] or None)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel

    :example:

    >>> normativeData = normativeDatasets.Schwartz2008("Free")
    >>> plot.compareKinetic([analysisPre,analysisPost],["pre","post"],"Left","LowerLimb",normativeData)
    """
    if outputName is None:
        outputName = "pyCGM2-Comparison"+"-"+context+" ["+ bodyPart+"]"

    if exportPdf or exportPng:
        filenameOut =  outputName+"-"+context+" ["+ bodyPart+"]"+"- Kinetics Comparison "


    i=1
    for analysis in analyses:
        if analysis.kineticStats.data == {}:
            raise Exception("[pyCGM2]: Kinetic comparison aborted. Analysis [%i] has no kinetic data"%(i))
        i+=1


    if bodyPart == "LowerLimb":
        bodyPart = enums.BodyPartPlot.LowerLimb
    elif bodyPart == "Trunk":
        bodyPart = enums.BodyPartPlot.Trunk
    elif bodyPart == "UpperLimb":
        bodyPart = enums.BodyPartPlot.UpperLimb
    else:
        raise Exception("[pyCGM2] - bodyPart argument not recognized ( must be LowerLimb, Trunk or UpperLimb) ")


    kv = ComparisonPlotViewers.KineticsPlotComparisonViewer(analyses,context,legends,bodyPart=bodyPart,pointLabelSuffix_lst=pointSuffixes)

    if plotType == "Descriptive":
        kv.setConcretePlotFunction(plot.gaitDescriptivePlot ) if type =="Gait" else kv.setConcretePlotFunction(plot.descriptivePlot )
    elif plotType == "Consistency":
        kv.setConcretePlotFunction(plot.gaitConsistencyPlot ) if type =="Gait" else kv.setConcretePlotFunction(plot.consistencyPlot )


    if normativeDataset is not None:
        kv.setNormativeDataset(normativeDataset)

    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-Kinetic comparison")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def compareEmgEnvelops(DATA_PATH,analyses,legends, emgChannels, muscles, contexts, normalActivityEmgs, normalized=False,plotType="Descriptive",show=True,title=None,type="Gait",outputName=None,exportPng=False,exportPdf=False):
    """
    compareEmgEvelops : compare emg envelops from  two pyCGM2 analysis instances


    :param analysis [pyCGM2.Processing.analysis.Analysis list]: list of pyCGM2 analysis instances
    :param legends [string list]: legend of each analysis instance
    :param emgChannels [string list]: label of your emg channels
    :param muscles [string list]: muscle label associated with your emg channels
    :param contexts [string list]: context associated with your emg channels
    :param normalActivityEmgs [string list]: normal activity associated with your emg channels



    **optional**
    :param normalized [bool]:  plot normalized-amplitude envelops
    :param plotType [string]: trace type ( Descriptive [default] or Consistency)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel

    :example:

    >> plot.compareEmgEvelops([emgAnalysisPre,emgAnalysisPost],
    >>>                       ["Pre","Post"],
    >>>                       ["EMG1","EMG2"]
    >>>                       ["Left","Right"]
    >>>                       ["RECFEM","VASLAT"])

    """
    if outputName is None:
        outputName = "pyCGM2-Comparison"

    if exportPdf or exportPng:
        filenameOut =  outputName+"- EMG Comparison"



    i=1
    for analysis in analyses:
        if analysis.emgStats.data == {}:
            raise Exception("[pyCGM2]: EMG comparison aborted. Analysis [%i] has no emg data"%(i))
        i+=1


    combinedEMGcontext=[]
    for i in range(0,len(emgChannels)):
        combinedEMGcontext.append([emgChannels[i],contexts[i],muscles[i]])


    kv = emgPlotViewers.MultipleAnalysis_EnvEmgPlotPanelViewer(analyses,legends)

    kv.setEmgs(combinedEMGcontext)
    kv.setNormalActivationLabels(normalActivityEmgs)
    if normalized:
        kv.setNormalizedEmgFlag(True)

    if type=="Gait":
        if plotType == "Descriptive":
            kv.setConcretePlotFunction(plot.gaitDescriptivePlot )
        elif plotType == "Consistency":
            kv.setConcretePlotFunction(plot.gaitConsistencyPlot )
    else:
        if plotType == "Descriptive":
            kv.setConcretePlotFunction(plot.descriptivePlot )
        elif plotType == "Consistency":
            kv.setConcretePlotFunction(plot.consistencyPlot )


    # filter
    pf = plotFilters.PlottingFilter()
    pf.setViewer(kv)
    if exportPdf: pf.setExport(DATA_PATH,filenameOut,"pdf")
    if title is not None: pf.setTitle(title+"-EMG envelop comparison")
    fig = pf.plot()
    if show: plt.show()

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig

def compareSelectedEmgEvelops(DATA_PATH,analyses,legends, emgChannels,contexts, normalized=False,plotType="Descriptive",type="Gait",show=True,title=None,outputName=None,exportPng=False,exportPdf=False):
    """
    compareSelectedEmgEvelops : compare selected emg envelops from  pyCGM2 analysis instances

    :param analysis [pyCGM2.Processing.analysis.Analysis list]: list of pyCGM2 analysis instances
    :param legends [string list]: legend of each analysis instance
    :param emgChannels [string list]: label of your emg channels
    :param contexts [string list]: context associated with your emg channels


    **optional**
    :param normalized [bool]:  display normalized amplitude envelop (false [defaut])
    :param plotType [string]: trace type ( Descriptive [default] or Consistency)
    :param type [string]:  display events (Gait [defaut] or None)
    :param show [bool]: enable matplotlib show function
    :param title [string]: change default title of the plot panel
    :example:

    >>> plot.compareSelectedEmgEvelops([emgAnalysisPre,emgAnalysisPost],["Pre","Post"],["EMG1","EMG1"],["Left","Left"],normalized=False)
    """

    if outputName is None:
        outputName = "pyCGM2-Comparison"

    if exportPdf or exportPng:
        filenameOut =  outputName+"- specific EMG Comparison"

    fig = plt.figure()
    ax = plt.gca()

    colormap_i_left=[plt.cm.Reds(k) for k in np.linspace(0.2, 1, len(analyses))]
    colormap_i_right=[plt.cm.Blues(k) for k in np.linspace(0.2, 1, len(analyses))]

    i=0
    for analysis in analyses:
        label = emgChannels[i] + "_Rectify_Env" if not normalized else emgChannels[i] + "_Rectify_Env_Norm"
        title = "EMG Envelop Comparison" if not normalized else "Normalized EMG Envelop Comparison"

        if contexts[i] == "Left":
            color=colormap_i_left[i]
        elif contexts[i] == "Right":
            color=colormap_i_right[i]

        if plotType == "Descriptive":
            if type =="Gait":
                plot.gaitDescriptivePlot(ax,analysis.emgStats,
                                        label,contexts[i],0,
                                        color=color,
                                        title=title, xlabel="Gait Cycle", ylabel="emg",ylim=None,
                                        customLimits=None,legendLabel=legends[i])
            else:
                plot.descriptivePlot(ax,analysis.emgStats,
                                        label,contexts[i],0,
                                        color=None,
                                        title=title, xlabel="Gait Cycle", ylabel="emg",ylim=None,
                                        customLimits=None,legendLabel=legends[i])
        elif plotType == "Consistency":
            if type =="Gait":
                plot.gaitConsistencyPlot(ax,analysis.emgStats,
                                        label,contexts[i],0,
                                        color=color,
                                        title=title, xlabel="Gait Cycle", ylabel="emg",ylim=None,
                                        customLimits=None,legendLabel=legends[i])
            else:
                plot.consistencyPlot(ax,analysis.emgStats,
                                        label,contexts[i],0,
                                        color=None,
                                        title=title, xlabel="Gait Cycle", ylabel="emg",ylim=None,
                                        customLimits=None,legendLabel=legends[i])
        else:
            raise Exception ("[pyCGM2]: plot type does not recongnized")

        i+=1

        ax.legend(fontsize=6)
    if show: plt.show()

    if exportPdf:
        fig.savefig(DATA_PATH+filenameOut+".pdf")

    if exportPng:
        fig.savefig(DATA_PATH+filenameOut+".png")
        return fig,filenameOut+".png"
    else:
        return fig
