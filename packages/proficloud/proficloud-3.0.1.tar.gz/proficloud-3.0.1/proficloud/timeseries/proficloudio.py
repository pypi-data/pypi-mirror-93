from kaa_sdk.config import set_credentials_file, set_config_file
from kaa_sdk.epts.v1.api import get_last_time_series
from datetime import datetime, timedelta

import time
from pandas import DataFrame, merge, Series

from streamz.core import Stream
import time
import tornado.ioloop
from tornado import gen
from pandas import DataFrame
import pandas as pd
import numpy

from py_linq import Enumerable

##############################
#Pigyback updated URI:

from kaa_sdk.epts.v1 import api
import requests
from kaa_sdk.config import get_config
from kaa_sdk.token import get_access_token

def get_time_series(app_name, time_series_names, from_date, to_date, endpoint_id, sort='ASC'):
    r"""
    Returns time series data points within the specified time range ordered by timestamp and grouped by endpoints.

    :param app_name: Application name
    :param time_series_names: One or more time series names.
    :param from_date: Start date to retrieve data points.
    :param to_date: End date to retrieve data points.
    :param endpoint_id: One or more endpoint IDs. If not specified, data is returned for all available endpoints.
    :param sort: Sorting order by timestamp. (one of 'ASC', 'DESC' - default: 'ASC')
    :return: json with time-series data
    """
    host = get_config()['host']
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "timeSeriesName": time_series_names,
        "uuid": endpoint_id, #use uuid instead of endpointId
        "fromDate": f"{from_date.isoformat()}Z",
        "toDate": f"{to_date.isoformat()}Z",
        "sort": sort
    }

    resp = requests.get(f'https://{host}/epts/data', params=params, headers=headers)
    resp.raise_for_status()

    return resp.json()

api.get_time_series = get_time_series

##############################

class ProficloudIOMetrics():

    DEBUGTIME = False
    """Debug request response times (print)"""
    DEBUGRESPONSE = False
    """
    Debug http-responses. When set to true, the attribute DEBUGRESPONSECONTENT then contains the last raw response. 
    Does not work when calling API in parallel using the same instance!
    """
    DEBUGRESPONSECONTENT = None
    """
    Contains the last response if DEBUGRESPONSE is set to True.
    """

    def __init__(self, staging=False):
        self._host = 'tsd.proficloud.io'
        self._auth_host = 'auth.proficloud.io'
        if staging:
            self._host = 'tsd.proficloud-staging.io'
            self._auth_host = 'auth.proficloud-staging.io'
        self._client_id = 'grafana-frontend'
        self._client_secret = None #None for no secret
        self._realm = 'kaa'
        self._application_name = "proficloud"

    def authenticate(self, username, password):
        set_credentials_file(uname=username,
                            password=password,
                            client_id=self._client_id,
                            client_secret=self._client_secret)

        set_config_file(host=self._host,
                        auth_host=self._auth_host,
                        realm=self._realm)

    def queryMetrics(self, uuid, metrics, start_time=None, end_time=None, createDf=True, fillNaMethod = None, dropTrailingNa=True, orderDesc=False, mergeTime=False):
        """
        Query metrics and return the data as pandas DataFrame.
        
        :type metrics: list(str), str
        :param metrics: A list of metric names (or a single metric name) to query. 
        :type start_time: int, datetime, str or None
        :param start_time: Timestamp (ms based), or datetime object (or datetime as string) not used when None. (Default: None)
        :type end_time: int, datetime, str or None
        :param end_time: Timestamp (ms based), or datetime object (or datetime as string). This must be later in time than the start time. If not specified, the end time is assumed to be the current date and time. (Default: None)
        :type orderDesc: boolean
        :param orderDesc: Orders returned data points based on timestamp. Descending order when True, or ascending when False (default) Only in effect when returning DataFrame.
        :type createDF: boolean
        :param createDF: Convert response into a convenient Pandas Dataframe. (Default=True)
        :type fillNaMethod: str
        :param fillNaMethod: {‘backfill’, ‘bfill’, ‘pad’, ‘ffill’, None}, default None. Method to use for filling holes in reindexed Series pad / ffill: propagate last valid observation forward to next valid backfill / bfill: use NEXT valid observation to fill gap
        :type dropTrailingNa: boolean
        :param dropTrailingNa: Drop trailing NaN values when set to true. Especially useful when end neither end param is specified (filters time delay when querying multiple metrics). Default: True
        :rtype: pandas.DataFrame or dict
        :return: Returns pandas.DataFrame 
        """
        
        if ProficloudIOMetrics.DEBUGTIME:
            start_t = datetime.now()

        sort = "ASC"
        if orderDesc:
            sort = "DESC"

        metrics_string = ",".join(metrics)
        response = api.get_time_series(self._application_name, metrics_string, start_time, end_time, uuid, sort=sort)
        #print(response)
        if ProficloudIOMetrics.DEBUGTIME:
            end_t = datetime.now()
            print("Database query took "+str(end_t - start_t))

        if ProficloudIOMetrics.DEBUGRESPONSE:
            ProficloudIOMetrics.DEBUGRESPONSECONTENT = response

        if not createDf:
            return response
        else:
            if ProficloudIOMetrics.DEBUGTIME:
                start_t = datetime.now()
            dfres = ProficloudIOMetrics.convert_response(response, uuid, fillNaMethod=fillNaMethod, dropTrailingNa=dropTrailingNa, convertTimestamp=True, mergeTime=mergeTime)
            if ProficloudIOMetrics.DEBUGTIME:
                end_t = datetime.now()
                print("Dataframe conversion took "+str(end_t - start_t))
            return dfres


    @staticmethod
    def dateparse(datestring):
        dateformat = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
        res = datestring
        try:
            res = datetime.strptime(datestring, dateformat[0])
        except:
            res = datetime.strptime(datestring, dateformat[1])
        return res

    @staticmethod
    def convert_response(response, uuid, fillNaMethod=None, dropTrailingNa=True, convertTimestamp=False, mergeTime=True):#, orderDesc=False
        """
        Used existing function from package as base. Description follows.
        """
        result = None

        if response is None:
            raise KeyError("Provided response is invalid. (None)")

        data = Enumerable(response)
        filter_endpoint = data.where(lambda w: uuid in w)
        check_uuid = len(list(filter_endpoint))
        
        if check_uuid <= 0:
            return None
                
        unique_metrics = list(filter_endpoint.select(lambda x: list(x[uuid].keys())[0]).distinct())
        metricCount = len(unique_metrics)

        if metricCount <= 0:
            return None

        for m in range(0, metricCount):
                
            #Get Metric Name
            mname = unique_metrics[m]
            
            try:
                #get metric data:
                all_from_one = data.select(lambda s: s[uuid]).where(lambda w: mname in w)
                items_from_one = all_from_one.select_many(lambda s: s[mname])
            
                valuematrix =list(map(lambda d: [d['timestamp'],d['values']['value']], items_from_one))
                mdf = DataFrame(valuematrix, columns=["timestamp", mname])
            except:
                raise KeyError("Provided query is invalid (invalid 'values' provided)")

            if convertTimestamp and ("timestamp" in mdf):
                mdf["timestamp"] = mdf["timestamp"].map(ProficloudIOMetrics.dateparse)

            if result is None:
                result = mdf
                result.sort_values("timestamp", inplace=True)
            else:
                result.sort_values("timestamp", inplace=True)
                mdf.sort_values("timestamp", inplace=True)
                if mergeTime:
                    mdf_re = mdf.set_index("timestamp").reindex(result.set_index("timestamp").index, method='nearest').reset_index()
                    result = merge(result, mdf_re, on="timestamp", sort=True)
                else:
                    result = merge(result, mdf, on="timestamp", how="outer", sort=True)
                

        if result.empty:
            return result

        if dropTrailingNa:
            last = min(result.apply(Series.last_valid_index, axis=0))
            result = result.loc[0:last]

        if fillNaMethod is not None:
            result = DataFrame.fillna(result, method=fillNaMethod, axis=0)
            result.dropna(how='all',inplace=True)
            result.dropna(how='all',axis=1,inplace=True)

        if result.empty:
            return result

        return result


class MetricsStreamIO(Stream):
    """
    This class creates a "streamz"-stream from a ProvicloudV3Connector (or one of its child classes such as ProficloudMetrics).

    :type connector: ProficloudIOMetrics (or subclass)
    :param connector: An initialized connector.
    :type metrics: list(str), str
    :param metrics: A list of metric names (or a single metric name) to query. 
    :type intervalMs: int
    :param intervalMs: Polling interval in milliseconds
    :type bufferTime: dict
    :param bufferTime: The buffer time is the current date and time minus the specified value and unit. Possible unit values are “milliseconds”, “seconds”, “minutes”, “hours”, “days”, “weeks”, “months”, and “years”. For example, if the start time is 5 minutes, the query will return all matching data points for the last 5 minutes. Example value: { "value": "10", "unit": "minutes" } 
    :type convertTimestamp: boolean
    :param convertTimestamp: Convert the timestamp to datetime (Default: False)
    """

    def __init__(self, connector, endpoint_id, metrics, intervalMs, bufferTime, **kwargs):
        self.__connector = connector
        self.__metrics = metrics
        self.__intervalMs = intervalMs
        self.__bufferTime = bufferTime
        self.__endpoint_id = endpoint_id
        self.header = DataFrame(columns=["timestamp"] + metrics)
        """The header for DataFrame creation with the streamz package"""
        super().__init__(ensure_io_loop=True, **kwargs)
        self.stopped = True

    @gen.coroutine
    def poll_metrics(self):
        """
        Polling co-routine. This retrieves metrics from the connector.
        """
        previousTs = None
        newSamples = None
        lastEmit = None

        while True:

            #Check interval after successful emit:
            if lastEmit is None:
                lastEmit = datetime.utcnow()
            else:
                diffMs = (datetime.utcnow() - lastEmit).total_seconds()*1000
                if diffMs < self.__intervalMs and diffMs > 0:
                    yield(gen.sleep((self.__intervalMs - diffMs)/1000.0))


            try:
                end_t = datetime.utcnow()
                start_t = end_t - self.__bufferTime
                try:
                    currentFrame = self.__connector.queryMetrics(self.__endpoint_id, self.__metrics, start_time=start_t, end_time=end_t, dropTrailingNa=True, createDf=True)
                except KeyError as err:
                    #Here, this exception might mean that no data was sent in the requested timedelta. Ignoring
                    currentFrame = None
                    #print(err)
            except:
                raise
                
            if currentFrame is not None:
                if ~currentFrame.empty:
                    if previousTs is not None:
                        newSamples = currentFrame[~currentFrame.timestamp.isin(previousTs)]
                    else:
                        newSamples = currentFrame   
                    previousTs = currentFrame["timestamp"]

                    if (~newSamples.empty) and numpy.array_equal(newSamples.columns, self.header.columns):
                        lastEmit = datetime.utcnow()
                        yield self._emit(newSamples)
                    else:
                        yield gen.sleep(self.__intervalMs/1000.0)
                else:
                    yield gen.sleep(self.__intervalMs/1000.0)
            else:
                yield gen.sleep(self.__intervalMs/1000.0)
            if self.stopped:
                break

    def start(self):
        """
        Start the stream.
        """
        if self.stopped:
            self.stopped = False
            self.loop.add_callback(self.poll_metrics)

    def stop(self):
        """
        Stop the stream.
        """
        if not self.stopped:
            self.stopped = True

    def changeInterval(self, intervalMs):
        self.__intervalMs = intervalMs
