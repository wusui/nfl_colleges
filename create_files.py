# Copyright (C) 2024 Warren Usui, MIT License
"""
Create nfl_players.json and nfl_players.html
"""
import json
from datetime import date
from itertools import chain
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from format_data import get_solution

def get_date_msg():
    """
    Get current date for use in html header
    """
    def gdm_inner(tdate):
        return f"NFL players on {tdate}"
    return gdm_inner(date.today().strftime("%B %d, %Y"))

def get_table_text(solution):
    """
    Build the html tables and the headers that get placed into the
    jinja2 template
    """
    def gtt_entry(school):
        def gtt_next(sname):
            def set_head(sdata):
                def sh_all(allv):
                    def sh_active(activ):
                        def gsort_key():
                            return str((999 - activ) * 1000 +
                                       (999 - allv)).zfill(6) + sname
                        return {'text':
                                f'{sname} (Active {activ}, Total {allv})',
                                'sort_key': gsort_key(),
                                'table': set_table(sdata)}
                    return sh_active(len(list(filter(lambda a:
                                    a['Status'] == 'Active', sdata))))
                return sh_all(len(sdata))
            def set_table(sdata):
                def set_cols():
                    def set_cols2(column_heads):
                        return list(map(lambda x: list(map(
                                lambda a: a[x], sdata)), column_heads))
                    def pull_coll():
                        return list(filter(lambda a: a != 'College',
                                    list(sdata[0].keys())))
                    def inner_set(col_names):
                        return dict(list(zip(col_names, set_cols2(col_names))))
                    return inner_set(pull_coll())
                return pd.DataFrame(data=set_cols()).to_html(index=False)
            return set_head(solution[school])
        def gtt_fix_dashes(sname):
            if sname == '--':
                return 'None'
            return sname
        return gtt_next(gtt_fix_dashes(school))
    def set_jinja_data(key_info):
        return list(map(lambda a: {'headerv': f"{a[0] + 1}. {a[1]['text']}",
                            'tablev': f"{a[1]['table']}"}, enumerate(key_info)))
    return set_jinja_data(sorted(list(map(gtt_entry, solution)),
                                 key=lambda a: a['sort_key']))

def render_html(solution):
    """
    Create the html file
    """
    def rh_env(env):
        def rh_tplt(template):
            def rh_set_data(data):
                return template.render(data)
            return rh_set_data({'hmsg': get_date_msg(),
                                'htmltables': get_table_text(solution)})
        return rh_tplt(env.get_template('template.html'))
    return rh_env(Environment(loader=FileSystemLoader('./')))

def mk_lines(solution):
    """
    Extract solution entries as single lines
    """
    def mk_recs(solution):
        return list(chain.from_iterable(list(map(
                    lambda a: solution[a], solution))))
    return '\n'.join(list(map(lambda a: '|'.join(a.values()),
                                           mk_recs(solution))))

def create_files():
    """
    Write out json and html files
    """
    def cf_inner(solution):
        with open('nfl_players.text', 'w', encoding='utf-8') as tfile:
            tfile.write(mk_lines(solution))
        with open('nfl_players.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(solution, jsonfile, ensure_ascii=False, indent=4)
        with open('nfl_players.html', "w", encoding="utf-8") as mfile:
            mfile.write(render_html(solution))
        return solution
    return cf_inner(get_solution())

if __name__ == "__main__":
    create_files()
