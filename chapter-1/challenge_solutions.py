
# Libraries ----
from python import eia_api as api
import os
import datetime
import plotly.express as px


# ## Question 1
#
# Extract from the EIA dashboard the metadata of the San Diego Gas and Electric balancing authority subregion (SUBBA) under California Independent System Operator parent (PARENT). This series is under the `Hourly Demand By Subregion` sub-category.
#
# ## Solution
#
# On the API Dashboard select the following route:
# - Electricity
# - Electric Power Operation (Daily and Hourly)
# - Hourly Demand by Subregion
#
# Once the filters loaded, go to facets and you can either use directly the `SUBBA` filter and find the San Diego Gas and Electric balancing authority subregion (out of the 83 series), or select first  California Independent System Operator on the `PARENT` filter and then it narrow down the options the four sub-regions under this parent.
#
#
# If you go with the last option, you should expect to have the following API URL:
#
# ```
# https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/?frequency=hourly&data[0]=value&facets[subba][]=SDGE&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000
# ```
#
# Which enables you to extract the API route path (as we saw before) - `electricity/rto/region-sub-ba-data/data`
#
# In addition, you can extract from the header the facets argument for the GET request:
#
#
# ```json
# {
#     "frequency": "hourly",
#     "data": [
#         "value"
#     ],
#     "facets": {
#         "parent": [
#             "CISO"
#         ],
#         "subba": [
#             "SDGE"
#         ]
#     },
#     "start": null,
#     "end": null,
#     "sort": [
#         {
#             "column": "period",
#             "direction": "desc"
#         }
#     ],
#     "offset": 0,
#     "length": 5000
# }
# ```
#
#
# The link to the filtered dashboard is available [here](https://www.eia.gov/opendata/browser/electricity/rto/region-sub-ba-data?frequency=hourly&data=value;&facets=subba;&subba=SDGE;&sortColumn=period;&sortDirection=desc;).


# ## Question 2
#
# Set a GET request to pull observations between Jan 1st and Jan 31st 2024 with R/Python
#
# ## Solution
#
# Using the information we pulled from the API dashboard we can set the GET request parameters:


api_key = os.getenv('EIA_API_KEY')

api_path = "electricity/rto/region-sub-ba-data/data/"

frequency = "hourly"

facets = {
    "parent": "CISO",
    "subba": "SDGE"
}

start = datetime.datetime(2024, 1, 1, 1)
end = datetime.datetime(2024, 1, 31, 23)


df1 = api.eia_get(
    api_key = api_key,
    api_path = api_path,
    frequency = frequency,
    facets = facets,
    start = start,
    end = end
)


df1.data


px.line(df1.data, x="period", y="value")


# ## Question 3
#
# Let's use the backfill function to pull data between Jan 1st 2020 and Feb 1st 2024:


start = datetime.datetime(2020, 1, 1, 1)
end = datetime.datetime(2024, 2, 1, 23)
offset = 2000

df2 = api.eia_backfill(
  start = start,
  end = end,
  offset = offset,
  api_path= api_path,
  api_key = api_key,
  facets = facets)


df2.data


px.line(df2.data, x="period", y="value")


