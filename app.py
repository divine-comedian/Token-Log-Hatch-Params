from tech.tech import read_impact_hour_data, read_cstk_data, TECH
from tech.tech import ImpactHoursData, ImpactHoursFormula, Hatch, DandelionVoting
from dotenv import load_dotenv
import pandas as pd
import panel as pn
import holoviews as hv
import numpy as np
import urllib
import urllib.parse as p
from tabulate import tabulate
import requests
import codecs
import os

load_dotenv()

# API settings
HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
HCTI_API_USER_ID = os.environ.get('HCTI_API_USER_ID')
HCTI_API_KEY = os.environ.get('HCTI_API_KEY')

tec_logo = "data:image/png;base64,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"
react = pn.template.ReactTemplate(title='TEC Hatch Dashboard',
                                  row_height=150, header_background= '#7622a8',
                                  logo=tec_logo)
pn.config.sizing_mode = 'stretch_both'

impact_hour_data_1, impact_hour_data_2 = read_impact_hour_data()
impact_hours_data = ImpactHoursData()

# ImpactHoursData
i = ImpactHoursData()

# TECH
t = TECH(total_impact_hours=i.total_impact_hours, impact_hour_data=impact_hour_data_1, total_cstk_tokens=8500)


# ImpactHoursFormula
#impact_hours_rewards = ImpactHoursFormula(i.total_impact_hours, impact_hour_data_1)
#impact_rewards_view = pn.Column(impact_hours_rewards.impact_hours_rewards,
# impact_hours_rewards.redeemable,
# impact_hours_rewards.cultural_build_tribute)

# Hatch
cstk_data = read_cstk_data()
#hatch = Hatch(cstk_data, impact_hours_rewards.target_raise,
# i.total_impact_hours,
# impact_hours_rewards.target_impact_hour_rate)

# DandelionVoting
dandelion = DandelionVoting(17e6)

# Import Params Button
import_params_button = pn.widgets.Button(name='Import params', button_type = 'primary')
import_description = pn.pane.Markdown('<h4>To import the parameters, click on the button below:</h4>')

# Share Button
comments = pn.widgets.TextAreaInput(name='Comments', max_length=1024, placeholder='Explain your thoughts on why you choose the params...')
share_button = pn.widgets.Button(name='Share your results on GitHub!', button_type = 'primary')
url = pn.widgets.TextInput(name='URL', value = '')
share_button.js_on_click(args={'target': url}, code='window.open(target.value)')
results_button = pn.widgets.Button(name='See your results', button_type = 'success')

@pn.depends(import_params_button)
def update_params_by_url_query(import_params_button):
    queries = pn.state.location.query_params
    if 'ihminr'in queries:
        t.min_max_raise[0] = int(queries['ihminr'])
    if 'hs' in queries:
        t.impact_hour_slope = float(queries['hs'])
    if 'maxihr' in queries:
        t.maximum_impact_hour_rate = float(queries['maxihr'])
    if 'ihtr' in queries:
        t.target_raise = int(queries['ihtr'])
    if 'ihmaxr' in queries:
        t.min_max_raise[0] = int(queries['ihmaxr'])
    if 'hor' in queries:
        t.hatch_oracle_ratio = float(queries['hor'])
    if 'hpd' in queries:
        t.hatch_period_days = int(queries['hpd'])
    if 'her' in queries:
        t.hatch_exchange_rate = float(queries['her'])
    if 'ht' in queries:
        t.hatch_tribute = int(queries['ht'])
    if 'sr' in queries:
        dandelion.support_required_percentage = int(queries['sr'])
    if 'maq' in queries:
        dandelion.minimum_accepted_quorum_percentage = int(queries['maq'])
    if 'vdd' in queries:
        dandelion.vote_duration_days = float(queries['vdd'])
    if 'vbh' in queries:
        dandelion.vote_buffer_hours = float(queries['vbh'])
    if 'rqh' in queries:
        dandelion.rage_quit_hours = float(queries['rqh'])
    if 'tfx' in queries:
        dandelion.tollgate_fee_xdai = float(queries['tfx'])

@pn.depends(results_button)
def update_result_score(results_button):
    data_table = {'Parameters': ["Target raise (wxDai)", "Maximum raise (wxDai)", "Minimum raise (wxDai)",
    "Impact hour slope (wxDai/IH)", "Maximum impact hour rate (wxDai/IH)",
    "Hatch oracle ratio (wxDai/CSTK)", "Hatch period (days)",
    "Hatch exchange rate (TESTTECH/wxDai)", "Hatch tribute (%)", "Support required (%)",
    "Minimum accepted quorum (%)", "Vote duration (days)", "Vote buffer (hours)",
    "Rage quit (hours)", "Tollgate fee (wxDai)"],
    'Values': [t.target_raise, t.min_max_raise[1],
    t.min_max_raise[0], t.impact_hour_slope,
    t.maximum_impact_hour_rate, t.hatch_oracle_ratio,
    t.hatch_period_days, t.hatch_exchange_rate, t.hatch_tribute,
    dandelion.support_required_percentage, dandelion.minimum_accepted_quorum_percentage, dandelion.vote_duration_days,
    dandelion.vote_buffer_hours, dandelion.rage_quit_hours, dandelion.tollgate_fee_xdai]}
    df = pd.DataFrame(data=data_table)

    if results_button:
        # Define output pane
        output_pane = pn.Row(pn.Column(t.impact_hours_view,
                                       t.redeemable_plot,
                                       t.cultural_build_tribute_plot),
        pn.Column(dandelion.vote_pass_view, t.funding_pool_view))
        output_pane.save('output.html')
        pn.panel(t.output_scenarios_out_issue().hvplot.table()).save('out_scenarios.html')

        scenarios = codecs.open("out_scenarios.html", 'r')
        charts = codecs.open("output.html", 'r')

        data_charts = { 'html': charts.read(),
        'css': ".box { color: white; background-color: #0f79b9; padding: 10px; font-family: Roboto }",
        'google_fonts': "Roboto" }
        data_scenarios = { 'html': scenarios.read(),
        'css': ".box { color: white; background-color: #0f79b9; padding: 10px; font-family: Roboto }",
        'google_fonts': "Roboto" }

        charts = requests.post(url = HCTI_API_ENDPOINT, data = data_charts, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
        scenarios = requests.post(url = HCTI_API_ENDPOINT, data = data_scenarios, auth=(HCTI_API_USER_ID, HCTI_API_KEY))

        output_data = """

<h1>Output Charts</h1>

![image]({image_charts})

<h1>Output Scenarios</h1>

![image]({image_scenarios})
        """.format(image_charts=charts.json()['url'],
        image_scenarios=scenarios.json()['url'])

        parameters_data = """

<h1>Parameters</h1>

{params_table}
        """.format(params_table=df.to_markdown(index=False))

        string_data = """
<h1>Results</h1>

<p>{comments}</p>

- It costs {tollgate_fee_xdai} wxDAI to make a proposal

- Votes will be voted on for {vote_duration_days} days

- TECH token holders will have {rage_quit_hours} Hours to exit the DAO if they don't like the result of a vote (as long as they don't vote yes).

- There can be a maximum of {max_proposals_month} votes per year.

- A proposal that passes can be executed {proposal_execution_hours} hours after it was proposed.

- A CSTK Token holder that has 2000 CSTK can send a max of {max_wxdai_ratio} wxDai to the Hatch

Play with my parameters [here](http://localhost:5006/app?ihminr={ihf_minimum_raise}&hs={hour_slope}&maxihr={maximum_impact_hour_rate}&ihtr={ihf_target_raise}&ihmaxr={ifh_maximum_raise}&hor={hatch_oracle_ratio}&hpd={hatch_period_days}&her={hatch_exchange_rate}&ht={hatch_tribute}&sr={support_required}&maq={minimum_accepted_quorum}&vdd={vote_duration_days}&vbh={vote_buffer_hours}&rqh={rage_quit_hours}&tfx={tollgate_fee_xdai}).

        """.format(comments=comments.value,
        tollgate_fee_xdai=dandelion.tollgate_fee_xdai,
        vote_duration_days=dandelion.vote_duration_days,
        rage_quit_hours=dandelion.rage_quit_hours,
        ihf_minimum_raise=t.min_max_raise[0],
        hour_slope=t.impact_hour_slope,
        maximum_impact_hour_rate=t.maximum_impact_hour_rate,
        ihf_target_raise=t.target_raise,
        ifh_maximum_raise=t.min_max_raise[1],
        hatch_oracle_ratio=t.hatch_oracle_ratio,
        hatch_period_days=t.hatch_period_days,
        hatch_exchange_rate=t.hatch_exchange_rate,
        hatch_tribute=t.hatch_tribute,
        support_required=dandelion.support_required_percentage,
        minimum_accepted_quorum=dandelion.minimum_accepted_quorum_percentage,
        vote_buffer_hours=dandelion.vote_buffer_hours,
        max_proposals_month=int(365*24/dandelion.vote_buffer_hours),
        proposal_execution_hours=dandelion.vote_buffer_hours+dandelion.rage_quit_hours,
        max_wxdai_ratio=int(2000*t.hatch_oracle_ratio))

        markdown_panel = pn.pane.Markdown(parameters_data + string_data + output_data)
        body = urllib.parse.quote(markdown_panel.object, safe='')
        url.value = "https://github.com/TECommons/Token-Log-Hatch-Params/issues/new?title=Vote%20for%20My%20Params&labels=TEST%20VOTE&body=" + body

    else:
        string_data=""
    markdown_panel = pn.pane.Markdown(string_data)
    return pn.Row(df.hvplot.table(),markdown_panel)

# Front-end
react.main[:1, :4] = pn.Column(import_description, import_params_button)
react.main[:2, 4:12] = i.impact_hours_accumulation
react.main[2:6, :4] = t
react.main[6:7, :4] = t.funding_pool_data_view
react.main[7:8, :4] = t.payout_view
react.main[2:8, 4:12] = pn.Column(t.impact_hours_view,
t.redeemable_plot,
t.cultural_build_tribute_plot)
react.main[8:11, :12] = t.funding_pool_view
react.main[11:11, :4] = dandelion
react.main[11:13, 4:12] = dandelion.vote_pass_view
react.main[13:14, :4] = comments
react.main[14:14, :4] = pn.Column(share_button, url)
react.main[13:13, 4:12] = results_button
react.main[15:17, :] = pn.panel(update_result_score)
react.main[17:17, :] = pn.panel('')

react.servable();

