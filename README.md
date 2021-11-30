# Derive lifetime MDD status from LIDAS items

BBMRI-NL BIONIC created the Lifetime Depression Assessment Self-report (LIDAS) questionnaire to efficiently identify lifetime major depressive disorder (MDD) cases in the general/Dutch population. Deriving MDD status from individual LIDAS items can be a complicated task, and so we wrote the script main.py to automate/aid in this process. 

**Context**
The LIDAS assesses lifetime MDD status in accordance with DSM 5 diagnostic criteria. MDD symptoms include two core symptoms, severely depressed mood and anhedonia, and seven accessory symptoms. These include decreased energy, altered weight/appetite, trouble sleeping, trouble concentrating/indecision, psychomotor retardation/agitation, feelings of worthlessness/guilt, and thoughts of death/suicidal ideation.
The DSM 5 diagnostic criteria define that lifetime MDD case status requires the presence of at least 5 symptoms, of which at least one is a core symptom, present for at least 2 weeks daily, most of the time, and causing significant disruption in daily life.
LIDAS measures not only the presence of depressive symptoms but also characteristics such as age of onset, episode duration, whether an episode led to significant dysfunction, whether it concerned a single or multiple episodes, whether an episode was experienced in the past 12 months, and whether professional help had been sought. 
LIDAS questions were gated in that core symptoms were assessed first, and follow-up symptoms were only assessed in respondents with at least one core symptom. In the absence of either core symptom, respondents were redirected to the end of the questionnaire.

**Arguments**
The script takes as input a .csv, .txt, or .sav file with data from the LIDAS questionnaire. To account for differences in naming conventions across cohorts, I’ve added a list of relevant LIDAS items below. Note that these should be renamed to the indicated format in order for the script to work!
{table 1}

The LIDAS also assesses psychiatric history by asking respondents about being diagnosed or treated for a range of psychiatric disorders. These variables are typically used to screen lifetime MDD controls for disease, e.g., to increase the disparity between cases and controls for power-hungry designs like GWAS. The variables below are required when options ‘mddsc’, ‘mdsc’, and ‘mddsc’ are supplied to the ‘--mdddef’ argument.
{table 2}

The variable below is required when options ‘mddc’ or ‘mddcsc’ are supplied to the ‘--mdddef’ argument.
{table 3}

