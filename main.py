### NTR LIDAS MDD
# Author: Floris Huider
# 18-10-2021

try:
    import argparse
    import numpy as np
    import pandas as pd
    import copy
    import pyreadstat
    import os
except ImportError:
    print('Failed to import required libraries. Please run the following:')
    print(' pip install --user pandas numpy pyreadstat argparse')

def morehelp(mhdict, k):
    if 'all' in k:
        mh = list(mhdict.keys())
    else:
        mh = k
    for x in mh:
        print('More help on {}:'.format(x))
        print('\n'.join(['  ' + i for i in mhdict[x]]))
        print()

def prep(input, output, mdddef, descriptives, minage):
    try:
        # Check input type minage
        if minage is not False:
            val = int(minage)
            print("Input is an integer number. Number = ", val)
    except ValueError:
        print("Error: Input for \'minage\' argument should be an integer or float")
    try:
        # Check input type pathdata
        if type(input) == str:
            print('Attempted to load in dataset: ' + '\'' + input + '\'')
        mydata = pd.read_spss(input, convert_categoricals=False)
    except ImportError:
        print("Error: Cannot find the specified file at this location. Input argument should be a string")
    try:
        # Check input mdddef. Requires update; currently accepts every type of input
        print('Used definition of MDD: ' + '\'' + mdddef + '\'')
    except ValueError:
        print("Error: Unexpected input for \'mdddef\' argument")

    if minage is not False:
        mydata = mydata.loc[mydata.loc[:, 'age12'] >= int(minage), :]
    if descriptives == True:
        print(mydata['age12'].describe())

    # Compute MDD symptom status from LIDAS items
    mydata['mdd01'] = -1
    mydata.loc[(mydata['deprmood12'] == 1) & (mydata['deprmoodf12'] == 1), ['mdd01']] = 1
    mydata.loc[(mydata['deprmood12'] == 0) | ((mydata['deprmood12'] == 1) & (mydata['deprmoodf12'] == 2)), ['mdd01']] = 0
    if descriptives == True:
        print(mydata['mdd01'].value_counts(dropna=False))

    mydata['mdd02'] = -1
    mydata.loc[((mydata['lossinterest12'] == 1) & (mydata['lossinterestf12'] == 1)) | ((mydata['deprmood_lossinterest12'] == 1) & (mydata['deprmood_lossinterestf12'] == 1)), ['mdd02']] = 1
    mydata.loc[(mydata['lossinterest12'] == 0) | ((mydata['lossinterest12'] == 1) & (mydata['lossinterestf12'] == 2)) | (mydata['deprmood_lossinterest12'] == 0) | ((mydata['deprmood_lossinterest12'] == 1) & (mydata['deprmood_lossinterestf12'] == 2)), ['mdd02']] = 0
    if descriptives == True:
        print(mydata['mdd02'].value_counts(dropna=False))

    mydata['mdd03'] = -1
    mydata.loc[(mydata['lossenergy12'] == 1), ['mdd03']] = 1
    mydata.loc[(mydata['lossenergy12'] == 0), ['mdd03']] = 0
    if descriptives == True:
        print(mydata['mdd03'].value_counts(dropna=False))

    mydata['mdd04'] = -1
    mydata.loc[((mydata['lossappetite12'] == 1) | (mydata['losswght12'] == 1) | (mydata['incrappetite12'] == 1) | (mydata['gainwght12'] == 1)), ['mdd04']] = 1
    mydata.loc[((mydata['lossappetite12'] == 0) & (mydata['losswght12'] == 0) & ((mydata['incrappetite12'] == 0) | (mydata['incrappetite12'] == 2)) & (mydata['gainwght12'] == 0)), ['mdd04']] = 0
    if descriptives == True:
        print(mydata['mdd04'].value_counts(dropna=False))

    mydata['mdd05'] = -1
    mydata.loc[(mydata['sleepprob12'] == 1) | (mydata['sleepwake12'] == 1) | (mydata['sleepmore12'] == 1), ['mdd05']] = 1
    mydata.loc[((mydata['sleepprob12'] == 0) & (mydata['sleepmore12'] == 0)), ['mdd05']] = 0  # We don't take sleepwake12 into account here?
    if descriptives == True:
        print(mydata['mdd05'].value_counts(dropna=False))

    mydata['mdd06'] = -1
    mydata.loc[(mydata['talkslow12'] == 1) | (mydata['movemore12'] == 1), ['mdd06']] = 1
    mydata.loc[((mydata['talkslow12'] == 0) | (mydata['talkslow12'] == 2)) & ((mydata['movemore12'] == 0) | (mydata['movemore12'] == 2)), ['mdd06']] = 0
    if descriptives == True:
        print(mydata['mdd06'].value_counts(dropna=False))

    mydata['mdd07'] = -1
    mydata.loc[(mydata['guilty12'] == 1), ['mdd07']] = 1
    mydata.loc[(mydata['guilty12'] == 0), ['mdd07']] = 0
    if descriptives == True:
        print(mydata['mdd07'].value_counts(dropna=False))

    mydata['mdd08'] = -1
    mydata.loc[(mydata['concentrate12'] == 1) | (mydata['decide12'] == 0), ['mdd08']] = 1       # Note the confusingly coded 'decide12' here. 0 = present, 1 = not present.
    mydata.loc[((mydata['concentrate12'] == 0) & (mydata['decide12'] == 1)), ['mdd08']] = 0
    if descriptives == True:
        print(mydata['mdd08'].value_counts(dropna=False))

    mydata['mdd09'] = -1
    mydata.loc[(mydata['death12'] == 1), ['mdd09']] = 1
    mydata.loc[(mydata['death12'] == 0), ['mdd09']] = 0
    if descriptives == True:
        print(mydata['mdd09'].value_counts(dropna=False))

    # Compute the nr of symptoms for each individual, later used to determine MDD case/control status
    mydata['coresymp'] = np.nan
    mydata.loc[((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)), ['coresymp']] = 1
    mydata.loc[((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0)), ['coresymp']] = 0
    if descriptives == True:
        print(mydata['coresymp'].value_counts(dropna=False)) # Implement a descriptive=yes/no argument to determine whether we print all the descriptives of these sub-variables.

    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
        mydata['dummymdd' + i] = copy.deepcopy(mydata['mdd' + i])
        mydata.loc[(mydata['mdd' + i] == -1), ['dummymdd' + i]] = 0
        # if descriptives == True:
        #     print(mydata['dummymdd' + i].value_counts(dropna=False)) # Check if counts for the new variables are ok.

    mydata['mddsymptoms'] = mydata[['dummymdd01', 'dummymdd02', 'dummymdd03', 'dummymdd04', 'dummymdd05', 'dummymdd06', 'dummymdd07', 'dummymdd08', 'dummymdd09']].sum(axis=1)
    if descriptives == True:
        print(mydata['mddsymptoms'].value_counts(dropna=False))
    # Compute the nr of present and missing symptoms, which we use to set mddsymptoms to np.nan if MDD status becomes ambiguous as a result of missing symptom data.
    # In many instances, a respondent can miss data for one or two symptoms and we will still be able to determine their MDD case/control status.
    # However, in some instances, a respondent will have too many missings for us to reliably determine MDD case/control status.
    # For example, a respondent with a 'yes' status for 4 / 9 symptoms would be an MDD control.
    # However, if this person has missing data on as much as one or more symptoms, their MDD case/control status becomes ambiguous:
    # If the symptom is present, the respondent would be an MDD case. If the symptom is not present, the respondent would be an MDD control.
    # We do not know whether this symptom is present or not, and so as a precaution we set the mddsymptoms variable for this respondent to np.nan; their MDD case/control status will also be np.nan as a consequence.
    # A fast way to do this would be to set all respondents to np.nan with 5 or more missing symptoms. But this is dangerous!
    # Remember that we use the presence of two coresymptoms as a threshold. If both core symptoms are absent, we know the person is a control and they skip the symptom items, meaning that they will have as much as 7 missing symptoms!
    # We can be sure that these people are controls, so there is no need to set them to missing. This is something that is taken into account in the code below.
    # Only the truly ambiguous MDD case/controls have their mddsymptoms value set to np.nan.
    for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09']:
        mydata['pres' + i] = np.nan
        mydata.loc[(mydata['mdd' + i] != -1), ['pres' + i]] = 1
        mydata.loc[(mydata['mdd' + i] == -1), ['pres' + i]] = 0
        if descriptives == True:
            print(mydata['pres' + i].value_counts(dropna=False))

    mydata['prescount'] = mydata[['pres01', 'pres02', 'pres03', 'pres04', 'pres05', 'pres06', 'pres07', 'pres08', 'pres09']].sum(axis=1)
    if descriptives == True:
        print(mydata['prescount'].value_counts(dropna=False))
    mydata['misscount'] = 9 - mydata['prescount']
    if descriptives == True:
        print(mydata['misscount'].value_counts(dropna=False))

    # Set mddsymptoms to np.nan for respondents with ambiguous MDD case/control status:
    # 4 symptoms but 1 or more missing symptom data:
    mydata.loc[((mydata['mddsymptoms'] == 4) & (mydata['misscount'] >= 1)), ['mddsymptoms']] = np.nan
    # 3 symptoms but 2 or more missing symptom data:
    mydata.loc[((mydata['mddsymptoms'] == 3) & (mydata['misscount'] >= 2)), ['mddsymptoms']] = np.nan
    # 2 symptoms but 3 or more missing symptom data:
    mydata.loc[((mydata['mddsymptoms'] == 2) & (mydata['misscount'] >= 3)), ['mddsymptoms']] = np.nan
    # 1 symptoms but 4 or more missing symptom data:
    mydata.loc[((mydata['mddsymptoms'] == 1) & (mydata['misscount'] >= 4)), ['mddsymptoms']] = np.nan
    # We can determine that someone is a control from the coresymptom items, but for this, both the status on mdd01 and mdd02 need to be known.
    # So if symptom status for either mdd01 or mdd02 is missing, and mddsymptoms = 0 and misscount >= 5, set mddsymptoms to np.nan:
    mydata.loc[(((mydata['mdd01'] == -1) | (mydata['mdd02'] == -1)) & (mydata['mddsymptoms'] == 0) & (mydata['misscount'] >= 5)), ['mddsymptoms']] = np.nan
    # We can determine that someone is a control from the coresymptom items, but for this, both the status on mdd01 and mdd02 need to be 0.
    # So if symptom status for either mdd01 or mdd02 is not zero, and mddsymptoms = 0 and misscount >= 5, set mddsymptoms to np.nan:
    mydata.loc[(((mydata['mdd01'] != 0) | (mydata['mdd02'] != 0)) & (mydata['mddsymptoms'] == 0) & (mydata['misscount'] >= 5)), ['mddsymptoms']] = np.nan
    if descriptives == True:
        print(mydata['mddsymptoms'].value_counts(dropna=False))

    # Compute variables for self-reported depression diagnosis, treatment, and other psychiatric disorders than depression.
    # Diagnosis for a disorder other than depression?
    mydata['opsyd'] = -1
    mydata.loc[((mydata['diag_bpd12'] == 1) | (mydata['diag_sczd12'] == 1) | (mydata['diag_ed12'] == 1) | (mydata['diag_ad12'] == 1) | (mydata['diag_pd12'] == 1) | (mydata['diag_ocd12'] == 1) |
                (mydata['diag_ptsd12'] == 1) | (mydata['diag_phb12'] == 1) | (mydata['diag_adhd12'] == 1) | (mydata['diag_persd12'] == 1) | (mydata['diag_alc12'] == 1) | (mydata['diag_drug12'] == 1)), ['opsyd']] = 1
    mydata.loc[((mydata['diag_bpd12'] == 0) & (mydata['diag_sczd12'] == 0) & (mydata['diag_ed12'] == 0) & (mydata['diag_ad12'] == 0) & (mydata['diag_pd12'] == 0) & (mydata['diag_ocd12'] == 0) &
                (mydata['diag_ptsd12'] == 0) & (mydata['diag_phb12'] == 0) & (mydata['diag_adhd12'] == 0) & (mydata['diag_persd12'] == 0) & (mydata['diag_alc12'] == 0) & (mydata['diag_drug12'] == 0)), ['opsyd']] = 0
    if descriptives == True:
        print(mydata['opsyd'].value_counts(dropna=False))

    # Diagnosis for depression or another disorder?
    mydata['psyd'] = -1
    mydata.loc[((mydata['diag_depr12'] == 1) | (mydata['diag_bpd12'] == 1) | (mydata['diag_sczd12'] == 1) | (mydata['diag_ed12'] == 1) | (mydata['diag_ad12'] == 1) | (mydata['diag_pd12'] == 1) | (mydata['diag_ocd12'] == 1) |
                (mydata['diag_ptsd12'] == 1) | (mydata['diag_phb12'] == 1) | (mydata['diag_adhd12'] == 1) | (mydata['diag_persd12'] == 1) | (mydata['diag_alc12'] == 1) | (mydata['diag_drug12'] == 1)), ['psyd']] = 1
    mydata.loc[((mydata['diag_depr12'] == 0) & (mydata['diag_bpd12'] == 0) & (mydata['diag_sczd12'] == 0) & (mydata['diag_ed12'] == 0) & (mydata['diag_ad12'] == 0) & (mydata['diag_pd12'] == 0) & (mydata['diag_ocd12'] == 0) &
                (mydata['diag_ptsd12'] == 0) & (mydata['diag_phb12'] == 0) & (mydata['diag_adhd12'] == 0) & (mydata['diag_persd12'] == 0) & (mydata['diag_alc12'] == 0) & (mydata['diag_drug12'] == 0)), ['psyd']] = 0
    if descriptives == True:
        print(mydata['psyd'].value_counts(dropna=False))

    # Treatment for a disorder other than depression?
    mydata['opsyt'] = -1
    mydata.loc[((mydata['contr_bpd12'] == 1) | (mydata['contr_sczd12'] == 1) | (mydata['contr_ed12'] == 1) | (mydata['contr_ad12'] == 1) | (mydata['contr_pd12'] == 1) | (mydata['contr_ocd12'] == 1) |
                (mydata['contr_ptsd12'] == 1) | (mydata['contr_phb12'] == 1) | (mydata['contr_adhd12'] == 1) | (mydata['contr_persd12'] == 1) | (mydata['contr_alc12'] == 1) | (mydata['contr_drug12'] == 1)), ['opsyt']] = 1
    mydata.loc[((mydata['contr_bpd12'] == 0) & (mydata['contr_sczd12'] == 0) & (mydata['contr_ed12'] == 0) & (mydata['contr_ad12'] == 0) & (mydata['contr_pd12'] == 0) & (mydata['contr_ocd12'] == 0) &
                (mydata['contr_ptsd12'] == 0) & (mydata['contr_phb12'] == 0) & (mydata['contr_adhd12'] == 0) & (mydata['contr_persd12'] == 0) & (mydata['contr_alc12'] == 0) & (mydata['contr_drug12'] == 0)), ['opsyt']] = 0
    if descriptives == True:
        print(mydata['opsyt'].value_counts(dropna=False))

    # Treatment for depression or another disorder?
    mydata['psyt'] = -1
    mydata.loc[((mydata['contr_depr12'] == 1) | (mydata['contr_bpd12'] == 1) | (mydata['contr_sczd12'] == 1) | (mydata['contr_ed12'] == 1) | (mydata['contr_ad12'] == 1) | (mydata['contr_pd12'] == 1) | (mydata['contr_ocd12'] == 1) |
                (mydata['contr_ptsd12'] == 1) | (mydata['contr_phb12'] == 1) | (mydata['contr_adhd12'] == 1) | (mydata['contr_persd12'] == 1) | (mydata['contr_alc12'] == 1) | (mydata['contr_drug12'] == 1)), ['psyt']] = 1
    mydata.loc[((mydata['contr_depr12'] == 0) & (mydata['contr_bpd12'] == 0) & (mydata['contr_sczd12'] == 0) & (mydata['contr_ed12'] == 0) & (mydata['contr_ad12'] == 0) & (mydata['contr_pd12'] == 0) & (mydata['contr_ocd12'] == 0) &
                (mydata['contr_ptsd12'] == 0) & (mydata['contr_phb12'] == 0) & (mydata['contr_adhd12'] == 0) & (mydata['contr_persd12'] == 0) & (mydata['contr_alc12'] == 0) & (mydata['contr_drug12'] == 0)), ['psyt']] = 0
    if descriptives == True:
        print(mydata['psyt'].value_counts(dropna=False))

    # Diagnosis or treatment for depression?
    mydata['depdt'] = -1
    mydata.loc[((mydata['diag_depr12'] == 1) | (mydata['contr_depr12'] == 1)), ['depdt']] = 1
    mydata.loc[((mydata['diag_depr12'] == 0) & ((mydata['contr_depr12'] == 0) | (mydata['contr_depr12'].isna()))), ['depdt']] = 0
    if descriptives == True:
        print(mydata['depdt'].value_counts(dropna=False))

    # Diagnosis or treatment for psychiatric disorder other than depression?
    mydata['opsydt'] = -1
    mydata.loc[((mydata['opsyd'] == 1) | (mydata['opsyt'] == 1)), ['opsydt']] = 1
    mydata.loc[((mydata['opsyd'] == 0) & ((mydata['opsyt'] == 0) | (mydata['opsyt'] == -1))), ['opsydt']] = 0
    if descriptives == True:
        print(mydata['opsydt'].value_counts(dropna=False))

    # Diagnosis or treatment for depression or other psychiatric disorders?
    mydata['psydt'] = -1
    mydata.loc[((mydata['psyd'] == 1) | (mydata['psyt'] == 1)), ['psydt']] = 1
    mydata.loc[((mydata['psyd'] == 0) & ((mydata['psyt'] == 0) | (mydata['psyt'] == -1))), ['psydt']] = 0
    if descriptives == True:
        print(mydata['psydt'].value_counts(dropna=False))

    # MDD algorithms
    if mdddef == "mdd":         # Or change to "mdd" isin mdddef or mdddef is "all":, so that people can use lists as input here.
        mydata['mdd'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['mdd']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['mdd']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['mdd']] = 0
        if descriptives == True:
            print(mydata['mdd'].value_counts(dropna=False))
    elif mdddef == "md":
        mydata['md'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['md']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['md']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['md']] = 0
        mydata.loc[(mydata['depdt'] == 1), ['md']] = 1
        if descriptives == True:
            print(mydata['md'].value_counts(dropna=False))
    elif mdddef == "mddsc":
        mydata['mddsc'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['mddsc']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['mddsc']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['mddsc']] = 0
        mydata.loc[((mydata['mddsc'] == 0) & (mydata['psydt'] == 1)), ['mddsc']] = -1
        mydata.loc[((mydata['mddsc'] == 0) & (mydata['treat_antidepr12'] == 1)), ['mddsc']] = -1
        if descriptives == True:
            print(mydata['mddsc'].value_counts(dropna=False))
    elif mdddef == "mdsc":
        mydata['mdsc'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['mdsc']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['mdsc']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['mdsc']] = 0
        mydata.loc[(mydata['depdt'] == 1), ['mdsc']] = 1
        mydata.loc[((mydata['mdsc'] == 0) & (mydata['psydt'] == 1)), ['mdsc']] = -1
        mydata.loc[((mydata['mdsc'] == 0) & (mydata['treat_antidepr12'] == 1)), ['mdsc']] = -1
        if descriptives == True:
            print(mydata['mdsc'].value_counts(dropna=False))
    elif mdddef == "mddc":
        mydata['mddc'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['mddc']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['mddc']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['mddc']] = 0
        mydata.loc[((mydata['mddc'] == 1) & ((mydata['deprlife_lastyear12'] == 0) | (mydata['deprlife_lastyear12'].isna()))), ['mddc']] = -1
        if descriptives == True:
            print(mydata['mddc'].value_counts(dropna=False))
    elif mdddef == "mddcsc":
        mydata['mddcsc'] = np.nan
        mydata.loc[((mydata['mddsymptoms'] >= 5) & ((mydata['mdd01'] == 1) | (mydata['mdd02'] == 1)) & (mydata['takecare12'] == 1)), ['mddcsc']] = 1
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mddsymptoms'] >= 0) & (mydata['mddsymptoms'] < 5))), ['mddcsc']] = 0
        mydata.loc[((mydata['takecare12'] == 0) | ((mydata['mdd01'] == 0) & (mydata['mdd02'] == 0))), ['mddcsc']] = 0
        mydata.loc[((mydata['mddcsc'] == 0) & (mydata['psydt'] == 1)), ['mddcsc']] = -1
        mydata.loc[((mydata['mddcsc'] == 0) & (mydata['treat_antidepr12'] == 1)), ['mddcsc']] = -1
        mydata.loc[((mydata['mddcsc'] == 1) & ((mydata['deprlife_lastyear12'] == 0) | (mydata['deprlife_lastyear12'].isna()))), ['mddcsc']] = -1
        if descriptives == True:
            print(mydata['mddcsc'].value_counts(dropna=False))
    try:
        # Check output argument
        if type(output) == str:
            print('Attempted to write results to: ' + '\'' + output + '\'')
        mydata.to_csv(path_or_buf=output, sep=';', index=False, na_rep='NA', float_format='%g')
    except ImportError:
        print("Error: Cannot write file to the specified location. Output argument should be a string")

if __name__ == '__main__':
    print('+----------------------------------------------+\n|         NTR LIDAS / List 12 MDD status       |')
    print('+----------------------------------------------+\n|                by Floris Huider              |')
    print('+----------------------------------------------+\n')
    parser = argparse.ArgumentParser(description='Python scripts to generate descriptives and MDD status variables of list 12.'
                                                 'This script is made for Python3 and requires the following libraries:'
                                                 'pandas, numpy, copy, pyreader, os')
    parser.add_argument('--input', help='Path to the datafile. This datafile should at least contain: ...', default=None)
    parser.add_argument('--output', help='Path and name of outputfile.', default=None)
    parser.add_argument('--mdddef', help='Choose definition of MDD. Should be one of: ... . Default=mdd', default='mdd')
    parser.add_argument('--descriptives', help='Define whether to output frequency tables of relevant variables. Default is False', action='store_true', default=False)
    parser.add_argument('--minage', help='Minimum age to include, e.g. only include 18+. Default is no restriction.', default=False)
    parser.add_argument('--morehelp', nargs="+", help='Print more help about this script (\'all\') or specific arguments')
    args = parser.parse_args()
    morehelpdict = {
        'this script': ['This script is used to prepare MDD case/control statuses variables in the NTR list12 LIDAS data.',
                        'This script is made for Python3 and requires pandas, numpy, matplotlib, json'],
        'minage': ['Define a minimumage, e.g. restrict minage to 18 years.'],
        'input': ['Define path + inputfile'],
        'output': ['Define path + outputfile + suffix'],
        'descriptives': ['Print descriptives'],
    }
    if args.morehelp is not None:
        morehelp(morehelpdict, args.morehelp)
    else:
        if (args.input is None):
            morehelp(morehelpdict, ['this script', 'input'])
            print('No input was requested. Please use at least (input) argument, see help above.')
            quit()
        if (args.input is not None) and (args.output is None):
            morehelp(morehelpdict, ['output'])
            print('Please specify an output filename. See help above')
            quit()
        prep(input=args.input, output=args.output, mdddef=args.mdddef, descriptives=args.descriptives, minage=args.minage)
        print(args.mdddef)
