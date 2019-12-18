from django.contrib.auth import settings
from datetime import datetime
from django.utils.dateformat import DateFormat
from pytz import timezone

from .models import PayrollSettings, Reports

import numpy as np
import pandas as pd


def get_employee_names():
    df_names = pd.read_excel(Reports.objects.latest('tips_by_employee').tips_by_employee.path,
                             sheet_name=0,
                             header=None,
                             skiprows=7)
    df_names.rename(columns={0: 'Employee'}, inplace=True)
    df_names['Employee'] = df_names['Employee'].str.lower()
    employee_names = df_names.loc[:, 'Employee'].tolist()
    employee_names.append('no manager')
    return [(name, name) for name in employee_names]


def read_excel_files():
    df_stylist_analysis = pd.read_excel(
        Reports.objects.latest('stylist_analysis').stylist_analysis.path,
        sheet_name=0, header=None, skiprows=4)
    df_tips = pd.read_excel(
        Reports.objects.latest('tips_by_employee').tips_by_employee.path,
        sheet_name=0, header=None, skiprows=0)
    df_hours1 = pd.read_excel(
        Reports.objects.latest('hours_week_1').hours_week_1.path,
        header=None, skiprows=5)
    df_hours2 = pd.read_excel(
        Reports.objects.latest('hours_week_2').hours_week_2.path,
        header=None, skiprows=5)
    df_retention = pd.read_excel(
        Reports.objects.latest('client_retention').client_retention.path,
        sheet_name=0, header=None, skiprows=8)
    df_efficiency = pd.read_excel(
        Reports.objects.latest('employee_service_efficiency').employee_service_efficiency.path,
        sheet_name=0, header=None, skiprows=5)
    return df_stylist_analysis, df_tips, df_hours1, df_hours2, df_retention, df_efficiency


def prepare_stylist_analysis(df_stylist_analysis):
    df_stylist_analysis.rename(
        columns={0: 'Store', 1: 'First', 2: 'Last', 3: 'Service Clients',
                 4: 'Percent Request', 5: 'Neck Trims',
                 6: 'Take Home Only Clients', 7: 'Total Clients',
                 8: 'Service Sales', 9: 'Take Home Sales', 10: 'Net Sales',
                 11: 'Total Hours', 12: 'Store Hours', 13: 'Non-Store Hours',
                 14: 'Take Home Per Client', 15: 'Total Avg Ticket',
                 16: 'Service Sales Per Hour', 17: 'Clients Per Hour',
                 18: 'Number of MVPs', 19: 'Paid MVP Percent',
                 20: 'Number of Paid Triple Plays',
                 21: 'Paid Triple Play Percent',
                 22: 'Paid BB Percent', 23: '# New Client BB',
                 24: 'New Client BB', 25: 'Number of New Clients',
                 26: 'Percent New Clients', 27: 'Number of Kids',
                 28: 'Percent Kids'}, inplace=True)
    df_stylist_analysis['Employee'] = (
            df_stylist_analysis['First'].astype(str) + ' ' + (
        df_stylist_analysis['Last']))
    df_stylist_analysis['Employee'] = (
        df_stylist_analysis['Employee'].str.lower())
    df_stylist_analysis['Paid BB Percent'] = (
            df_stylist_analysis['Paid BB Percent'].astype('float') / 100)
    df_stylist_analysis_short = (
        df_stylist_analysis.loc[:, ['Store', 'Employee',
                                    'Total Clients', 'Clients Per Hour',
                                    'Service Sales', 'Take Home Sales',
                                    'Take Home Per Client', 'Service Sales Per Hour',
                                    'Paid BB Percent', 'New Client BB']])
    return df_stylist_analysis, df_stylist_analysis_short


def set_pay_period(df_tips, df_stylist_analysis_short):
    df_tips['Pay Period'] = df_tips.loc[1, 1]
    df_tips.rename(
        columns={0: 'Employee', 3: 'Credit Tips'}, inplace=True)
    df_tips = df_tips.drop(df_tips.index[:6])
    df_tips = df_tips.loc[:, ['Employee', 'Credit Tips', 'Pay Period']]
    df_tips['Employee'] = df_tips['Employee'].str.lower()
    df_pay_period = df_tips.iloc[0, 2]
    df_all_employees = pd.merge(
        df_stylist_analysis_short, df_tips, how='left', on='Employee').fillna(0)
    df_all_employees['Pay Period'] = df_pay_period
    return df_all_employees


def process_hours(df_hrs_wk1, df_hrs_wk2, df_all_employees):
    # hours settings
    work_day = 8
    work_week = 40
    resolution = 0.25

    # process hours week one
    df_hrs_wk1[0] = df_hrs_wk1[0].str.lower()
    df_hrs_wk1.rename(
        columns={0: 'Employee', 1: 'Date', 5: 'Hours1'}, inplace=True)
    df_hrs_wk1 = df_hrs_wk1.loc[:, ['Employee', 'Date', 'Hours1']]
    df_hrs_wk1['Hours1'] = (
        df_hrs_wk1['Hours1'].str.replace(r"[a-zA-Z]", '').astype('float'))
    df_hrs1_dropna = (
        df_hrs_wk1.dropna(subset=['Employee', 'Date', 'Hours1']))
    df_hrs_wk1_final = (
        df_hrs1_dropna.groupby(['Employee', 'Date']).sum().reset_index())
    df_hrs_wk1_final['Regular Hours'] = 0
    #  regular hours = 8 hours where hours are less than the work day
    df_hrs_wk1_final['Regular Hours'] = np.where(
        (df_hrs_wk1_final['Hours1']) < work_day,
        (df_hrs_wk1_final['Hours1']), work_day)
    #  create a column for week one OT hours with zeros in it,
    df_hrs_wk1_final['OT1'] = 0
    # Daily OT hours = (day hours - 8) where the hours for the day are greater than 8
    df_hrs_wk1_final['OT1'] = np.where(
        (df_hrs_wk1_final['Hours1']) > work_day,
        (df_hrs_wk1_final['Hours1']) - work_day,
        (df_hrs_wk1_final['OT1']))
    # cumulative sum the hours of each day to total the weekly hours
    df_hrs_wk1_final['Cum hours'] = (
        df_hrs_wk1_final.groupby('Employee')['Hours1'].transform('cumsum'))
    # weekly OT = cumulative hours for the (week - 40)
    df_hrs_wk1_final['Week OT1'] = np.where(
        df_hrs_wk1_final['Cum hours'] -
        df_hrs_wk1_final['Hours1'] > work_week,
        df_hrs_wk1_final['Hours1'],
        df_hrs_wk1_final['Cum hours'] - work_week)
    # Total OT = weekly OT
    df_hrs_wk1_final['OT1'] = np.where(
        df_hrs_wk1_final['Cum hours'] > work_week,
        df_hrs_wk1_final['Week OT1'],
        df_hrs_wk1_final['OT1'])

    df_hrs_wk1_final = (
        df_hrs_wk1_final.loc[:, ['Employee', 'Date', 'Hours1', 'OT1']])
    df_hrs_wk1_final = (
        df_hrs_wk1_final.groupby(['Employee']).sum().reset_index())

    df_hrs_wk1_final['OT1'] = (
        (df_hrs_wk1_final[['OT1']].div(resolution)).round().mul(resolution))

    df_hrs_wk1_final['Hours1'] = (
        (df_hrs_wk1_final[['Hours1']].div(resolution)).round().mul(resolution))

    df_hrs_wk1_final['Hours1'] = df_hrs_wk1_final['Hours1'] - df_hrs_wk1_final['OT1']

    # process hours week two
    df_hrs_wk2[0] = df_hrs_wk2[0].str.lower()
    df_hrs_wk2.rename(
        columns={0: 'Employee', 1: 'Date', 5: 'Hours2'}, inplace=True)
    df_hrs_wk2 = df_hrs_wk2.loc[:, ['Employee', 'Date', 'Hours2']]
    df_hrs_wk2['Hours2'] = df_hrs_wk2[
        'Hours2'].str.replace(r"[a-zA-Z]", '').astype('float')
    df_hrs_wk2_dropna = (
        df_hrs_wk2.dropna(subset=['Employee', 'Date', 'Hours2']))
    df_hrs_wk2_final = (
        df_hrs_wk2_dropna.groupby(['Employee', 'Date']).sum().reset_index())
    df_hrs_wk2_final['Regular Hours'] = 0
    df_hrs_wk2_final['Regular Hours'] = np.where(
        (df_hrs_wk2_final['Hours2']) < work_day,
        (df_hrs_wk2_final['Hours2']), work_day)
    df_hrs_wk2_final['OT2'] = 0
    df_hrs_wk2_final['OT2'] = np.where(
        (df_hrs_wk2_final['Hours2']) > work_day,
        (df_hrs_wk2_final['Hours2']) - work_day,
        (df_hrs_wk2_final['OT2']))
    df_hrs_wk2_final['Cum hours'] = df_hrs_wk2_final.groupby(
        'Employee')['Hours2'].transform('cumsum')
    df_hrs_wk2_final['Week OT2'] = np.where(
        df_hrs_wk2_final['Cum hours'] - df_hrs_wk2_final['Hours2'] > work_week,
        df_hrs_wk2_final['Hours2'],
        df_hrs_wk2_final['Cum hours'] - work_week)
    df_hrs_wk2_final['OT2'] = np.where(
        df_hrs_wk2_final['Cum hours'] > work_week,
        df_hrs_wk2_final['Week OT2'],
        df_hrs_wk2_final['OT2'])
    df_hrs_wk2_final = (
        df_hrs_wk2_final.loc[:, ['Employee', 'Date', 'Hours2', 'OT2']])
    df_hrs_wk2_final = (
        df_hrs_wk2_final.groupby(['Employee']).sum().reset_index())
    df_hrs_wk2_final['Hours2'] = (
        (df_hrs_wk2_final[['Hours2']].div(resolution)).round().mul(resolution))
    df_hrs_wk2_final['OT2'] = (
        (df_hrs_wk2_final[['OT2']].div(resolution)).round().mul(resolution))

    df_hrs_wk2_final['Hours2'] = df_hrs_wk2_final['Hours2'] - df_hrs_wk2_final['OT2']

    # merge data-frames
    df_all_employees = pd.merge(
        df_all_employees, df_hrs_wk1_final,
        how='outer', on='Employee').fillna(0)
    df_all_employees = pd.merge(
        df_all_employees, df_hrs_wk2_final,
        how='outer', on='Employee').fillna(0)
    df_all_employees['Total Hours'] = (
            df_all_employees['Hours1'] +
            df_all_employees['Hours2'])
    return df_all_employees


def calculate_stylist_bonuses(df_all_employees, df_stylist_analysis):
    # stylist bonus settings
    bonus_settings = PayrollSettings.objects.get(id=1)

    service_bonus_sales_min = float(bonus_settings.service_bonus_sales_min)
    service_bonus_cap = float(bonus_settings.service_bonus_cap)
    service_bonus_take_home_sales_min = float(bonus_settings.service_bonus_take_home_sales_min)
    service_bonus_paid_bb_min = float(bonus_settings.service_bonus_paid_bb_min)
    star_multiplier = float(bonus_settings.star_multiplier)
    star_thpc_min = float(bonus_settings.star_thpc_min)
    star_paid_bb_min = float(bonus_settings.star_paid_bb_min)
    star_clients_per_hour_min = float(bonus_settings.star_clients_per_hour_min)
    all_star_multiplier = float(bonus_settings.all_star_multiplier)
    all_star_thpc_min = float(bonus_settings.all_star_thpc_min)
    all_star_paid_bb_min = float(bonus_settings.all_star_paid_bb_min)
    all_star_clients_per_hour_min = float(bonus_settings.all_star_clients_per_hour_min)
    mvp_multiplier = float(bonus_settings.mvp_multiplier)
    mvp_thpc_min = float(bonus_settings.mvp_thpc_min)
    mvp_paid_bb_min = float(bonus_settings.mvp_paid_bb_min)
    mvp_clients_per_hour_min = float(bonus_settings.mvp_clients_per_hour_min)
    platinum_multiplier = float(bonus_settings.platinum_multiplier)
    platinum_thpc_min = float(bonus_settings.platinum_thpc_min)
    platinum_paid_bb_min = float(bonus_settings.platinum_paid_bb_min)
    platinum_clients_per_hour_min = float(bonus_settings.platinum_clients_per_hour_min)
    take_hm_bonus_lvl_1_sales_min = float(bonus_settings.take_hm_bonus_lvl_1_sales_min)
    take_hm_bonus_lvl_1_multiplier = float(bonus_settings.take_hm_bonus_lvl_1_multiplier)
    take_hm_bonus_lvl_2_sales_min = float(bonus_settings.take_hm_bonus_lvl_2_sales_min)
    take_hm_bonus_lvl_2_multiplier = float(bonus_settings.take_hm_bonus_lvl_2_multiplier)

    # stylist service bonus
    df_all_employees['Service Bonus'] = (
            (df_all_employees['Service Sales Per Hour'] -
             service_bonus_sales_min) *
            (df_all_employees['Paid BB Percent'] *
             df_stylist_analysis['Store Hours'])).round(2)
    df_all_employees['Service Bonus'] = np.where(
        (df_all_employees['Service Bonus'])
        > service_bonus_cap, service_bonus_cap,
        (df_all_employees['Service Bonus'])).round(2)
    df_all_employees['Service Bonus'] = np.where(
        (df_all_employees['Service Bonus']) < 0.01, 0,
        (df_all_employees['Service Bonus'])).round(2)
    df_all_employees['Service Bonus'] = np.where(
        (df_all_employees['Take Home Sales']) <
        service_bonus_take_home_sales_min, 0, np.where(
        df_all_employees['Paid BB Percent'] <
        service_bonus_paid_bb_min, 0,
        df_all_employees['Service Bonus']).round(2))

    # stylist star bonus
    df_all_employees['Star Bonus Multiplier'] = 0.00
    df_all_employees['Star Bonus Multiplier'][
        (df_all_employees['Take Home Per Client']
         >= star_thpc_min)
        & (df_all_employees['Paid BB Percent']
           >= star_paid_bb_min)
        & (df_all_employees['Clients Per Hour']
           >= star_clients_per_hour_min)] = star_multiplier
    df_all_employees['Star Bonus Multiplier'][
        (df_all_employees['Take Home Per Client']
         >= all_star_thpc_min) &
        (df_all_employees['Paid BB Percent']
         >= all_star_paid_bb_min) &
        (df_all_employees['Clients Per Hour'] > (
            all_star_clients_per_hour_min))] = all_star_multiplier
    df_all_employees['Star Bonus Multiplier'][
        (df_all_employees['Take Home Per Client'] >= (
            mvp_thpc_min)) &
        (df_all_employees['Paid BB Percent'] >= (
            mvp_paid_bb_min)) &
        (df_all_employees['Clients Per Hour'] >= (
            mvp_clients_per_hour_min))] = mvp_multiplier
    df_all_employees['Star Bonus Multiplier'][
        (df_all_employees['Take Home Per Client'] >= (
            platinum_thpc_min)) &
        (df_all_employees['Paid BB Percent'] >= (
            platinum_paid_bb_min)) &
        (df_all_employees['Clients Per Hour'] >= (
            platinum_clients_per_hour_min))] = platinum_multiplier
    df_all_employees['Star Bonus'] = (
            df_all_employees['Star Bonus Multiplier'] *
            df_all_employees['Total Hours']).round(2)

    # stylist take home sales bonus
    df_all_employees['Take Home Tier'] = np.where(
        df_all_employees['Take Home Sales'] <
        take_hm_bonus_lvl_1_sales_min, 0, np.where(
            df_all_employees['Take Home Sales'] >
            take_hm_bonus_lvl_2_sales_min,
            take_hm_bonus_lvl_2_multiplier,
            take_hm_bonus_lvl_1_multiplier))
    df_all_employees['Take Home Bonus'] = (
            df_all_employees['Take Home Tier'] * (
        df_all_employees['Take Home Sales']).round(2))
    df_all_employees['Take Home Bonus'] = df_all_employees['Take Home Bonus'].round(2)

    df_all_employees = df_all_employees[
        ['Store', 'Employee', 'Pay Period', 'Hours1', 'Hours2',
         'OT1', 'OT2', 'Total Hours', 'Credit Tips', 'Total Clients',
         'Clients Per Hour', 'New Client BB', 'Take Home Sales',
         'Take Home Tier', 'Take Home Per Client', 'Service Sales',
         'Service Sales Per Hour', 'Paid BB Percent',
         'Star Bonus Multiplier', 'Star Bonus',
         'Service Bonus', 'Take Home Bonus']].fillna(0)
    df_all_employees['OT'] = (
            df_all_employees['OT1'] + df_all_employees['OT2'])
    df_all_employees['Holiday'] = ''
    df_all_employees['PTO Hours'] = ''
    df_all_employees['Other Hours/Training'] = ''
    df_all_employees['Other Pay'] = ''
    df_all_employees['Season Ticket Bonus'] = ''

    # star levels
    df_all_employees['Star Level'] = 'N/A'
    df_all_employees['Star Level'][
        (df_all_employees['Take Home Per Client'] > 0.99) &
        (df_all_employees['Paid BB Percent'] > 0.29)] = 'Rising Star!'
    df_all_employees['Star Level'][
        (df_all_employees['Take Home Per Client'] > 1.49) &
        (df_all_employees['Paid BB Percent'] > 0.34) &
        (df_all_employees['Clients Per Hour'] > 1.79)] = 'Star!'
    df_all_employees['Star Level'][
        (df_all_employees['Take Home Per Client'] > 1.74) &
        (df_all_employees['Paid BB Percent'] > 0.39) &
        (df_all_employees['Clients Per Hour'] > 1.99)] = 'All-Star!'
    df_all_employees['Star Level'][
        (df_all_employees['Take Home Per Client'] > 1.99) &
        (df_all_employees['Paid BB Percent'] > 0.44) &
        (df_all_employees['Clients Per Hour'] > 2.19)] = 'MVP!'
    df_all_employees['Star Level'][
        (df_all_employees['Take Home Per Client'] > 2.99) &
        (df_all_employees['Paid BB Percent'] > 0.64) &
        (df_all_employees['Clients Per Hour'] > 2.19)] = 'Platinum!'
    df_all_employees = df_all_employees[[
        'Store', 'Employee', 'Pay Period', 'Hours1', 'Hours2',
        'OT', 'Holiday', 'PTO Hours', 'Other Hours/Training',
        'Other Pay', 'Total Hours', 'Credit Tips',
        'Total Clients', 'Clients Per Hour', 'Take Home Sales',
        'Take Home Tier', 'Take Home Per Client', 'Service Sales',
        'Service Sales Per Hour', 'Paid BB Percent',
        'Star Bonus Multiplier', 'Star Bonus', 'Service Bonus',
        'Take Home Bonus', 'Season Ticket Bonus', 'Star Level',
        'New Client BB']].fillna(0)
    df_store = (
        df_all_employees[['Store', 'Employee', 'Pay Period', 'Hours1',
                          'Hours2', 'Total Hours', 'OT', 'Holiday',
                          'PTO Hours', 'Other Hours/Training',
                          'Credit Tips', 'Other Pay', 'Service Bonus',
                          'Take Home Bonus', 'Star Bonus',
                          'Season Ticket Bonus', 'Star Level']])
    df_all_employees['Client Excitement'] = ''
    df_all_employees['Client Retention'] = ''
    df_all_employees['Return Retention'] = ''
    df_all_employees['Varsity Times'] = ''
    df_all_employees['MVP Times'] = ''

    return df_all_employees, df_store


def calculate_manager_bonuses(df_all_employees, man_name, df_store):
    # manager bonus settings
    bonus_settings = PayrollSettings.objects.get(id=1)

    manager_service_breakpoint = float(bonus_settings.manager_service_breakpoint)
    manager_service_bonus_cap = float(bonus_settings.manager_service_bonus_cap)
    manager_service_bonus_paid_bb_min = float(bonus_settings.manager_service_bonus_paid_bb_min)
    manager_service_bonus_thpc_min = float(bonus_settings.manager_service_bonus_thpc_min)

    df_manager = df_all_employees[df_all_employees['Employee'].str.contains(man_name)]
    df_manager['Service Breakpoint'] = manager_service_breakpoint
    df_manager['Manager Service Diff'] = (
            df_manager['Service Sales'] -
            df_manager['Service Breakpoint'])
    df_manager['Store BB Percent'] = df_all_employees.iloc[-1, 19]
    df_manager['Service Bonus'] = (
            df_manager['Store BB Percent'] *
            df_manager['Manager Service Diff']).round(2)
    df_manager['Star Bonus'] = 0
    df_manager = df_manager[[
        'Store', 'Pay Period', 'Employee', 'Hours1', 'Hours2',
        'Total Hours', 'OT', 'Holiday', 'PTO Hours',
        'Other Hours/Training', 'Credit Tips', 'Other Pay',
        'Service Bonus', 'Take Home Bonus', 'Take Home Per Client',
        'Paid BB Percent', 'Star Bonus', 'Season Ticket Bonus',
        'Star Level']]

    # manager service bonus
    df_manager['Service Bonus'] = np.where(
        df_manager['Service Bonus'] >
        manager_service_bonus_cap, manager_service_bonus_cap,
        df_manager['Service Bonus'])
    df_manager['Service Bonus'] = np.where(
        df_manager['Service Bonus'] < 0, 0,
        df_manager['Service Bonus'])
    df_manager['Service Bonus'] = np.where(
        (df_manager['Paid BB Percent']) <
        manager_service_bonus_paid_bb_min, 0,
        (df_manager['Service Bonus'])).round(2)
    df_manager['Service Bonus'] = np.where(
        (df_manager['Take Home Per Client']) <
        manager_service_bonus_thpc_min, 0,
        (df_manager['Service Bonus'])).round(2)

    # store totals
    df_store.loc[df_store['Employee'] == man_name] = df_manager
    df_store = df_store[:-1]
    df_store.loc[-1] = [
        df_store.loc[1, 'Store'], 'total salon',
        df_store.loc[1, 'Pay Period'],
        df_store['Hours1'].sum(), df_store['Hours2'].sum(),
        df_store['Total Hours'].sum(), df_store['OT'].sum(), '', '', '',
        df_store['Credit Tips'].sum(), '',
        df_store['Service Bonus'].sum(), df_store['Take Home Bonus'].sum(),
        df_store['Star Bonus'].sum(), '', '']
    return df_store


def process_one_on_one(df_all_employees, df_retention, df_efficiency):
    df_1on1 = df_all_employees[[
        'Store', 'Employee', 'Pay Period', 'Service Sales Per Hour',
        'Paid BB Percent', 'New Client BB', 'Clients Per Hour',
        'Take Home Per Client', 'Client Excitement',
        'Varsity Times', 'MVP Times']].fillna(0)
    df_1on1 = df_1on1[:-1]
    df_retention1 = df_retention[[0, 7, 9]]
    df_retention2 = df_retention1[:-1]
    df_retention2.rename(columns={
        0: 'Employee', 7: 'Client Retention',
        9: 'Return Retention'}, inplace=True)
    df_retention2['Employee'] = (
        df_retention2['Employee'].str.lower())
    df_1on1_3 = df_1on1.merge(
        df_retention2, how='outer', left_on='Employee',
        right_on='Employee').fillna(0)
    df_1on1_4 = df_1on1_3[[
        'Store', 'Employee', 'Pay Period', 'Service Sales Per Hour',
        'Paid BB Percent', 'New Client BB', 'Clients Per Hour',
        'Take Home Per Client', 'Client Retention',
        'Return Retention', 'Client Excitement']]
    df_efficiency = df_efficiency[:-1]
    df_efficiency = df_efficiency[[0, 1, 4]]
    df_efficiency.rename(
        columns={
            0: 'Employee', 1: 'MVP Times', 4: 'Varsity Times'},
        inplace=True)
    df_efficiency['Employee'] = (
        df_efficiency['Employee'].str.lower())
    df_1on1_5 = df_1on1_4.merge(
        df_efficiency, how='outer', left_on='Employee',
        right_on='Employee').fillna(0)
    df_1on1_5['New Client BB'] = (
            df_1on1_5['New Client BB'] / 100)
    df_1on1_5['Client Retention'] = (
            df_1on1_5['Client Retention'] / 100)
    df_1on1_5['Return Retention'] = (
            df_1on1_5['Return Retention'] / 100)
    df_1on1_5['Paid BB Percent'] = (
        df_1on1_5['Paid BB Percent'].round(2))
    df_1on1_5['Clients Per Hour'] = (
        df_1on1_5['Clients Per Hour'].round(2))
    df_1on1_5['Take Home Per Client'] = (
        df_1on1_5['Take Home Per Client'].round(2))
    df_1on1_5['Client Retention'] = (
        df_1on1_5['Client Retention'].round(2))
    df_1on1_5['Return Retention'] = (
        df_1on1_5['Return Retention'].round(2))
    df_1on1_5['MVP Times'] = (
        df_1on1_5['MVP Times'].astype('int'))
    df_1on1_5['Varsity Times'] = (
        df_1on1_5['Varsity Times'].astype('int'))
    df_1on1_5 = df_1on1_5[['Store', 'Employee', 'Pay Period',
                           'Service Sales Per Hour', 'Paid BB Percent',
                           'New Client BB', 'Take Home Per Client',
                           'Clients Per Hour', 'Client Excitement',
                           'Client Retention', 'Return Retention',
                           'Varsity Times', 'MVP Times'
                           ]]
    return df_1on1_5, df_1on1


def write_data_to_excel_file(df_1on1_5, df_store, df_1on1):
    row_len = len(df_1on1_5.index)
    number_rows = len(df_store.index) + 1

    # sheet names
    payroll = df_1on1.loc[0, 'Store']
    one_on_one = df_1on1_5.loc[0, 'Store'] + ' One-on-One'

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    dt = datetime.now(timezone('US/Pacific'))
    df = DateFormat(dt)
    time = df.format('Y-m-d-h-i-s')
    file_path = settings.MEDIA_ROOT + '/payroll-' + time + '.xlsx'
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # Convert the data-frame to an XlsxWriter Excel object.
    df_store.to_excel(writer, index=False, sheet_name=payroll)
    df_1on1_5.to_excel(writer, index=False, sheet_name=one_on_one)
    workbook = writer.book

    payroll_sheet = writer.sheets[payroll]
    one_on_one_sheet = writer.sheets[one_on_one]

    one_on_one_sheet.merge_range('A35:C36', 'Stylist Signature')
    one_on_one_sheet.merge_range('D35:E36', 'Date')
    one_on_one_sheet.merge_range('F35:I36', 'Managers Note')
    one_on_one_sheet.merge_range('A37:C38', 'Stylist Signature')
    one_on_one_sheet.merge_range('D37:E38', 'Date')
    one_on_one_sheet.merge_range('F37:I38', 'Managers Note')
    one_on_one_sheet.merge_range('A39:C40', 'Stylist Signature')
    one_on_one_sheet.merge_range('D39:E40', 'Date')
    one_on_one_sheet.merge_range('F39:I40', 'Managers Note')
    one_on_one_sheet.merge_range('A41:C42', 'Stylist Signature')
    one_on_one_sheet.merge_range('D41:E42', 'Date')
    one_on_one_sheet.merge_range('F41:I42', 'Managers Note')
    one_on_one_sheet.merge_range('A43:C44', 'Stylist Signature')
    one_on_one_sheet.merge_range('D43:E44', 'Date')
    one_on_one_sheet.merge_range('F43:I44', 'Managers Note')
    one_on_one_sheet.merge_range('A45:C46', 'Stylist Signature')
    one_on_one_sheet.merge_range('D45:E46', 'Date')
    one_on_one_sheet.merge_range('F45:I46', 'Managers Note')
    one_on_one_sheet.merge_range('A47:C48', 'Stylist Signature')
    one_on_one_sheet.merge_range('D47:E48', 'Date')
    one_on_one_sheet.merge_range('F47:I48', 'Managers Note')
    one_on_one_sheet.merge_range('A49:C50', 'Stylist Signature')
    one_on_one_sheet.merge_range('D49:E50', 'Date')
    one_on_one_sheet.merge_range('F49:I50', 'Managers Note')
    one_on_one_sheet.merge_range('A51:C52', 'Stylist Signature')
    one_on_one_sheet.merge_range('D51:E52', 'Date')
    one_on_one_sheet.merge_range('F51:I52', 'Managers Note')
    one_on_one_sheet.merge_range('A53:C54', 'Stylist Signature')
    one_on_one_sheet.merge_range('D53:E54', 'Date')
    one_on_one_sheet.merge_range('F53:I54', 'Managers Note')
    one_on_one_sheet.merge_range('A55:C56', 'Stylist Signature')
    one_on_one_sheet.merge_range('D55:E56', 'Date')
    one_on_one_sheet.merge_range('F55:I56', 'Managers Note')
    one_on_one_sheet.merge_range('A57:C58', 'Stylist Signature')
    one_on_one_sheet.merge_range('D57:E58', 'Date')
    one_on_one_sheet.merge_range('F57:I58', 'Managers Note')

    store_total_format = workbook.add_format(
        {'font_size': 40, 'bold': True})
    data_format1 = workbook.add_format(
        {'bg_color': '#ffffff'})
    data_format2 = workbook.add_format(
        {'bg_color': '#e5e5e5'})
    dollar_format = workbook.add_format(
        {'num_format': '$#,##0.00'})
    per_format = workbook.add_format(
        {'num_format': '0%'})

    payroll_sheet.conditional_format(
        "$A$1:$Q$%d" % number_rows,
        {"type": "formula",
         "criteria": '=INDIRECT("B"&ROW())="total salon"',
         "format": store_total_format})

    one_on_one_sheet.conditional_format(1, 3, row_len, 3, {
        'type': 'cell', 'criteria': 'less than',
        'value': 3400, 'format': dollar_format})
    one_on_one_sheet.conditional_format(1, 4, row_len, 4, {
        'type': 'cell', 'criteria': 'less than',
        'value': 5, 'format': per_format})
    one_on_one_sheet.conditional_format(1, 5, row_len, 5, {
        'type': 'cell', 'criteria': 'less than',
        'value': 80, 'format': per_format})
    one_on_one_sheet.conditional_format(1, 6, row_len, 6, {
        'type': 'cell', 'criteria': 'less than',
        'value': 100, 'format': dollar_format})
    one_on_one_sheet.conditional_format(1, 7, row_len, 7, {
        'type': 'cell', 'criteria': 'less than',
        'value': 100, 'format': dollar_format})
    one_on_one_sheet.conditional_format(1, 8, row_len, 8, {
        'type': 'cell', 'criteria': 'less than',
        'value': 20, 'format': per_format})
    one_on_one_sheet.conditional_format(1, 9, row_len, 9, {
        'type': 'cell', 'criteria': 'less than',
        'value': 100, 'format': per_format})
    one_on_one_sheet.conditional_format(1, 10, row_len, 10, {
        'type': 'cell', 'criteria': 'less than',
        'value': 100, 'format': per_format})

    for row in range(0, number_rows + 1, 2):
        payroll_sheet.set_row(row, cell_format=data_format1)
        payroll_sheet.set_row(row + 1, cell_format=data_format2)
        payroll_sheet.write(row, 0, None)
        payroll_sheet.write(row + 1, 0, None)

    for row in range(0, row_len + 1, 2):
        one_on_one_sheet.set_row(row, cell_format=data_format1)
        one_on_one_sheet.set_row(row + 1, cell_format=data_format2)
        one_on_one_sheet.write(row, 0, None)
        one_on_one_sheet.write(row + 1, 0, None)

    chart_thpc = workbook.add_chart(
        {'type': 'column'})
    chart_paid_bb = workbook.add_chart(
        {'type': 'column', 'num_format': '0%'})
    chart_clients_per_hr = workbook.add_chart(
        {'type': 'column'})

    # [sheet name, first_row, first_col, last_row, last_col]
    chart_thpc.add_series(
        {'name': 'Take Home Per Client',
         'categories': [one_on_one, 1, 1, row_len, 1],
         'values': [one_on_one, 1, 6, row_len, 6],
         'gradient': {'colors': ['red', 'black'], }})
    chart_paid_bb.add_series(
        {'name': 'Paid Back Bar %',
         'categories': [one_on_one, 1, 1, row_len, 1],
         'values': [one_on_one, 1, 4, row_len, 4],
         'gradient': {'colors': ['red', 'black']},
         'type': 'percentage'})
    chart_clients_per_hr.add_series(
        {'name': 'Clients Per Hour',
         'categories': [one_on_one, 1, 1, row_len, 1],
         'values': [one_on_one, 1, 7, row_len, 7],
         'gradient': {'colors': ['red', 'black']}})

    chart_thpc.set_x_axis({'num_font': {'rotation': 45}})
    chart_paid_bb.set_x_axis({'num_font': {'rotation': 45}})
    chart_clients_per_hr.set_x_axis({'num_font': {'rotation': 45}})
    chart_thpc.set_style(12)
    chart_paid_bb.set_style(12)
    chart_clients_per_hr.set_style(12)

    one_on_one_sheet.insert_chart(
        (row_len + 1), 0, chart_thpc, {
            'x_scale': .65, 'y_scale': 1.5})
    one_on_one_sheet.insert_chart(
        (row_len + 1), 4, chart_paid_bb, {
            'x_scale': .65, 'y_scale': 1.5})
    one_on_one_sheet.insert_chart(
        (row_len + 1), 8, chart_clients_per_hr, {
            'x_scale': .7, 'y_scale': 1.5})

    payroll_sheet.insert_image('O22', 'media/1.png')
    one_on_one_sheet.insert_image('J44', 'media/1.png')

    writer.save()
    workbook.close()
    return file_path


def run_payroll(man_name):
    df_stylist_analysis, df_tips, df_hours1, df_hours2, df_retention, df_efficiency = read_excel_files()
    df_processed_sar, df_processed_sar_short = prepare_stylist_analysis(df_stylist_analysis)
    df_processed_all_employees = set_pay_period(df_tips, df_processed_sar_short)
    df_employees_and_hours = process_hours(df_hours1, df_hours2, df_processed_all_employees)
    df_employees_and_bonuses, df_store = calculate_stylist_bonuses(df_employees_and_hours, df_processed_sar)
    df_processed_store = calculate_manager_bonuses(df_employees_and_bonuses, man_name, df_store)
    df_processed_1on1, df_second_1on1 = process_one_on_one(df_employees_and_bonuses, df_retention, df_efficiency)
    file_path = write_data_to_excel_file(df_processed_1on1, df_processed_store, df_second_1on1)
    return file_path
