def usgs_datagrab():
    """
    usgs_datagrab accesses the USGS NWIS website and scraps the water surface level above NAVD 88 for available Lakes

    :return: pandas multindex dataframe of lake name, USGS site ID, date of data acquisition, and associated water level
    """
    from datetime import datetime
    import urllib3
    import certifi
    import re
    import pandas as pd

    begin_date = '1776-7-4'
    now = datetime.now()
    end_date = now.strftime('%Y-%m-%d')

    target_url = 'https://waterdata.usgs.gov/nwis/dv?referred_module=sw&site_tp_cd=LK&index_pmcode_62615=1&group_key=' \
                 'NONE&sitefile_output_format=rdb&column_name=site_no&column_name=station_nm&range_selection=' \
                 'date_range&begin_date={}&end_date={}&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value' \
                 '&list_of_search_criteria=site_tp_cd%2Crealtime_parameter_selection'.format(begin_date, end_date)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    req = http.request('GET', target_url)
    text = req.data.decode()

    retrieved_date = re.search(r"retrieved:.*$", text, re.M)
    print('This data was accessed on: {}'.format(retrieved_date.group()))

    site_ids = re.findall(r"USGS (\d*) (.*)$", text, re.M)
    temp_column_names = ['site_id', 'site_name']
    name_df = pd.DataFrame(site_ids, columns=temp_column_names)

    data = re.findall(r"(USGS)\t(\d*)\t([\d-]*)\t([\d.]*)", text)

    column_names =['Agency', 'site_id', 'date', 'water_level_ft']
    temp_usgs_dataframe = pd.DataFrame(data, columns=column_names)

    usgs_dataframe = temp_usgs_dataframe.merge(name_df)
    usgs_dataframe.set_index(['site_id', 'site_name', 'date'], inplace=True)
    print(usgs_dataframe)

    return usgs_dataframe

