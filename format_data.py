# Copyright (C) 2024 Warren Usui, MIT License
"""
Format scraped data from get_ptables into a useful dict.
"""
from itertools import chain
from get_teams import get_ptables

def hndl_team(team_info):
    """
    Assign team name to player records and assign human readable statuses
    """
    def ht_get_ptypes(pgroup):
        def ht_get_rows(plyr_row):
            def ht_status(pstatus):
                return ['Offense', 'Defense', 'Special Teams',
                        'Injured Reserve', 'Practice Squad'][pstatus]
            return list(plyr_row[1].items()) + [('team', team_info[0]),
                                            ('Status', ht_status(pgroup[0]))]
        return list(map(ht_get_rows, pgroup[1].iterrows()))
    return list(chain.from_iterable(
                list(map(ht_get_ptypes, enumerate(team_info[1])))))

def get_players():
    """
    Get ptable data and chain into one list reformatted into fields
    that we care about.
    """
    return list(chain.from_iterable(list(map(hndl_team, get_ptables()))))

def clean_list(player):
    """
    Only keep track of a subset of the player data
    """
    return list(filter(lambda a: a[0] in ['Name',
                    'POS', 'College', 'team', 'Status'], player))

def dictify():
    """
    Convert player info into a dict entry
    """
    return list(map(dict, list(map(clean_list, get_players()))))

def fix_status(pstatus):
    """
    Make sure all players not on IR list or Practice Squad are Active
    """
    if pstatus in ['Offense', 'Defense', 'Special Teams']:
        return 'Active'
    return pstatus

def fix_name(plyr_name):
    """
    Remove player numbers accidentally concatenated onto names
    """
    return ''.join(list(filter(lambda a: not a.isdigit(), plyr_name)))

def fix_end_dict(player):
    """
    Apply fix_name and fix_status to fields in player record
    """
    return {'College': player['College'], 'Team': player['team'],
            'Name': fix_name(player['Name']), 'POS': player['POS'],
            'Status': fix_status(player['Status'])}

def name_sort(player):
    """
    Translate name into a reasonable last name, first name format.  Account
    for punctuation, jr and the third suffixes, and consider St. X and VaN Y
    to be last names
    """
    def fix_sp_ln(pname):
        def fsl_spl(nparts):
            if len(nparts) > 2:
                if nparts[-2] in ['st', 'van']:
                    ' '.join(nparts[-2:] + nparts[0: -2])
            return ' '.join([nparts[-1]] + nparts[0:-1])
        return fsl_spl(pname.split(' '))
    def pull_suff(mod_name):
        if mod_name.split(' ')[-1] in ["ii", "iii", "iv", "jr", "sr"]:
            return ' '.join(mod_name.split(' ')[0:-1])
        return mod_name
    def ns_apos(string1):
        def ns_noper(string2):
            return fix_sp_ln(pull_suff(''.join(string2.split('-'))))
        return ns_noper(''.join(string1.split('.')))
    return ns_apos(''.join(player['Name'].lower().split("'")))

def sort_namekey(in_data):
    """
    Sort based on last name
    """
    return sorted(in_data, key=name_sort)

def format_data():
    """
    Call fix_end_dict to all the player data
    """
    return sort_namekey(list(map(fix_end_dict, dictify())))

def get_solution():
    """
    Return a dict indexed by school where each value is a list of player
    records
    """
    def get_cols(records):
        return sorted(list(set(list(map(lambda a: a['College'], records)))),
                      key=str.lower)
    def gs_inner(records):
        def gs_inn2(cdata):
            def mk_ans_entry(school):
                return [school, list(filter(lambda a: a['College'] == school,
                                            records))]
            return dict(list(map(mk_ans_entry, cdata)))
        return gs_inn2(get_cols(records))
    return gs_inner(format_data())
