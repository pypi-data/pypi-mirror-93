# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from collections import OrderedDict
from pyCGM2.Tools import exportTools



# --- FILTER ----


class DiscreteEMGFilter(object):
    """
    """

    def __init__(self, discreteEMGProcedure, analysis,emgLabels, emgMuscles, emgContexts,subjInfo=None,condExpInfo=None):

        self.m_procedure = discreteEMGProcedure
        self.m_analysis=analysis
        self.dataframe =  None

        self.m_subjInfo = subjInfo
        self.m_condExpInfo = condExpInfo

        self.m_emgMuscles=emgMuscles
        self.m_emgLabels=emgLabels
        self.m_emgContexts=emgContexts

    def setSubjInfo(self, subjInfo):
        self.m_subjInfo = subjInfo

    def setCondExpInf(self, condExpInfo):
        self.m_condExpInfo = condExpInfo


    def getOutput(self):
        self.dataframe = self.m_procedure.detect(self.m_analysis,self.m_emgLabels,self.m_emgMuscles,self.m_emgContexts)

        # add infos

        if self.m_subjInfo is not None:
            for key,value in self.m_subjInfo.items():
                exportTools.isColumnNameExist( self.dataframe, key)
                self.dataframe[key] = value

        if self.m_condExpInfo is not None:
            for key,value in self.m_condExpInfo.items():
                exportTools.isColumnNameExist( self.dataframe, key)
                self.dataframe[key] = value

        return self.dataframe





# --- PROCEDURE ----



class AmplitudesProcedure(object):

    NAME = "EMG Amplitude from Integration for each gait phase"


    def __init__(self):
        pass

    def detect (self,analysisInstance,emgLabels,emgMuscles,emgContexts):

        dataframes = list()

        index = 0
        for emgLabel in emgLabels:
            context = emgContexts[index]
            muscle = emgMuscles[index]
            dataframes.append(self.__getAmplitudebyPhase(analysisInstance,emgLabel+"_Rectify_Env_Norm",muscle,context))
            index+=1

        return pd.concat(dataframes)



    def __construcPandasSerie(self,emgLabel,muscle,context, cycleIndex,phase,
                              value,procedure):
        iDict = OrderedDict([('ChannelLabel', emgLabel),
                     ('Label', muscle),
                     ('EventContext', context),
                     ('Cycle', cycleIndex),
                     ('Phase', phase),
                     ('Procedure', procedure),
                     ('Value', value)])
        return pd.Series(iDict)

    def __getAmplitudebyPhase(self,analysisInstance,emglabel,muscle,context):

        procedure = "Amplitude"
        muscle = context[0]+muscle


        stanceValues =   analysisInstance.emgStats.pst['stancePhase', context]['values']
        doubleStance1Values =   analysisInstance.emgStats.pst['doubleStance1', context]['values']
        doubleStance2Values =   stanceValues - analysisInstance.emgStats.pst['doubleStance2', context]['values']

        normalizedCycleValues = analysisInstance.emgStats.data [emglabel,context]

        series = list()

        for i in range(0,len(normalizedCycleValues["values"])):

            # cycle
            lim0 = 0; lim1 = 100
            res_cycle=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "cycle",
                                               res_cycle,
                                               procedure)
            series.append(serie)

            # stance
            lim0 = 0; lim1 = int(stanceValues[i])
            res_stance=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "stance",
                                               res_stance,
                                               procedure)
            series.append(serie)


            # swing
            lim0 = int(stanceValues[i]); lim1 = 100
            res_swing=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "swing",
                                               res_swing,
                                               procedure)
            series.append(serie)


            # doubleStance1
            lim0 = 0; lim1 = int(doubleStance1Values[i])
            res_d1=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "doubleStance1",
                                               res_d1,
                                               procedure)
            series.append(serie)

            # double stance2
            lim0 = int(doubleStance2Values[i]); lim1 = int(stanceValues[i])
            res_d2=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "doubleStance2",
                                               res_d2,
                                               procedure)
            series.append(serie)

            lim0 = int(doubleStance1Values[i]); lim1 = int(doubleStance2Values[i])
            res_single=np.trapz(normalizedCycleValues["values"][i][lim0:lim1+1],
                         x=np.arange(lim0,lim1+1),axis=0)[0]

            serie = self.__construcPandasSerie(emglabel,muscle,context,
                                               int(i),
                                               "singleStance",
                                               res_single,
                                               procedure)
            series.append(serie)


        return pd.DataFrame(series)
