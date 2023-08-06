# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2017
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

from pixiedust.display.chart.renderers import PixiedustRenderer
from pixiedust.display.chart.colorManager import Colors
from .matplotlibBaseDisplay import MatplotlibBaseDisplay
from pixiedust.utils import Logger
import numpy as np

@PixiedustRenderer(id="barChart")
@Logger()
class BarChartRenderer(MatplotlibBaseDisplay):

    def getNumFigures(self):
        return len(self.getValueFields()) if self.isSubplot() else 1

    def isSubplot(self):
        return self.options.get("charttype", "grouped") == "subplots"

    def getExtraFields(self):
        if not self.isSubplot() and len(self.getValueFields())>1:
            #no clusterby if we are grouped and multiValueFields
            return []
    
        clusterby = self.options.get("clusterby")
        return [clusterby] if clusterby is not None else []

    def getSubplotHSpace(self):
        return 0.5

    #Main rendering method
    def matplotlibRender(self, fig, ax):
        keyFields = self.getKeyFields()
        valueFields = self.getValueFields()
        stacked = self.options.get("charttype", "grouped") == "stacked"
        subplots = self.isSubplot()
        kind = "barh" if self.options.get("orientation", "vertical") == "horizontal" else "bar"
        clusterby = self.options.get("clusterby")

        if clusterby is not None and (subplots or len(valueFields)<=1):
            subplots = subplots if len(valueFields)==1 else False
            for j, valueField in enumerate(valueFields):
                pivot = self.getWorkingPandasDataFrame().pivot(
                    index=keyFields[0], columns=clusterby, values=valueField
                )
                pivot.index.name=keyFields[0]

                # sort order is lost after pivot
                sortby = self.options.get("sortby", None)
                if sortby:
                    if sortby == 'Keys ASC':
                        pivot = pivot.sort_values(keyFields, ascending=True)
                    elif sortby == 'Keys DESC':
                        pivot = pivot.sort_values(keyFields, ascending=False)
                    else:
                        pivot[valueFields[0]] = pivot.sum(axis=1)
                        if sortby == 'Values ASC':
                            pivot = pivot.sort_values(valueFields[0], ascending=True)
                        elif sortby == 'Values DESC':
                            pivot = pivot.sort_values(valueFields[0], ascending=False)
                        pivot.drop(valueFields[0], axis=1, inplace=True)

                thisAx = pivot.plot(kind=kind, stacked=stacked, ax=self.getAxItem(ax, j), sharex=True, legend=self.showLegend(), 
                    label=None if subplots else valueField, subplots=subplots,colormap = Colors.colormap)

                if isinstance(thisAx, (list, np.ndarray)):
                    if kind == 'barh':
                        for plotaxis in thisAx:
                            plotaxis.invert_yaxis()
                    if len(valueFields)==1 and subplots:
                        #resize the figure
                        figw = fig.get_size_inches()[0]
                        fig.set_size_inches( figw, (figw * 0.5)*min( len(thisAx), 10 ))
                elif kind == 'barh':
                    thisAx.invert_yaxis()

                return thisAx
        else:
            thisAx = self.getWorkingPandasDataFrame().plot(kind=kind, stacked=stacked, ax=ax, x=keyFields[0], legend=self.showLegend(), subplots=subplots,colormap = Colors.colormap)
            if kind == 'barh':
                if isinstance(thisAx, (list, np.ndarray)):
                    for plotaxis in thisAx:
                        plotaxis.invert_yaxis()
                else:
                    thisAx.invert_yaxis()

            if clusterby is not None:
                self.addMessage("Warning: 'Cluster By' ignored when you have multiple Value Fields but subplots option is not selected")