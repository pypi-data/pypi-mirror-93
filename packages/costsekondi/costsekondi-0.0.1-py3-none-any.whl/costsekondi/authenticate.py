import requests
import click
import json


def makerequest(url):
    request = requests.get(url)
    if request.status_code == 200:
        return request.content
    else:
        raise Exception("Bad request")


def displayPojectResults(data):
    
    if len(json.loads(data)) > 0:
        count = 0
        dataList = json.loads(data)
        # print(data)
        for index in range(len(dataList)):
            count += 1
            projectname = dataList[index]["name"]
            click.echo(f' {click.style(f"======> Poject {str(count)} ({projectname}): <======", fg="yellow")} \n')
            click.echo(f' {click.style("ID:", fg="green")} {dataList[index]["projectid"]} \n')
            click.echo(f' {click.style("Owner:", fg="green")} {dataList[index]["owner"]} \n')
            click.echo(f' {click.style("Title:", fg="green")} {dataList[index]["name"]} \n')
            click.echo(f' {click.style("Type of Project:", fg="green")} {dataList[index]["project_type"]} \n')
            click.echo(f' {click.style("Location:", fg="green")} {dataList[index]["location"]} \n')
            click.echo(f' {click.style("Description:", fg="green")} {dataList[index]["description"]} \n')
            click.echo(f' {click.style("Expected Life of Asset:", fg="green")} {dataList[index]["life_of_asset"]} \n')
            click.echo(f' {click.style("Scope:", fg="green")} {dataList[index]["project_scope"]} \n')
            click.echo(f' {click.style("Environmental Impact:", fg="green")} {dataList[index]["env_impact"]} \n')
            click.echo(f' {click.style("Land and Settlement Impact:", fg="green")} {dataList[index]["land_impact"]} \n')
            click.echo(f' {click.style("Design Standard:", fg="green")} {dataList[index]["design_standard"]} \n')
            click.echo(f' {click.style("Estimated Cost in USD:", fg="green")} {dataList[index]["pd_grant_original_currency"]} \n')
            click.echo(f' {click.style("Estimated Cost in GHS:", fg="green")} {dataList[index]["pd_grant_local_currency"]} \n')
            click.echo(f' {click.style("Date of Approval:", fg="green")} {dataList[index]["pd_grant_approve_date"]} \n')
            click.echo(f' {click.style("Estimated Start Date:", fg="green")} {dataList[index]["pd_grant_period_from"]} \n')
            click.echo(f' {click.style("Estimated Completion Date:", fg="green")} {dataList[index]["pd_grant_period_to"]} \n')
            click.echo(f' {click.style("Risk Assessment:", fg="green")} {dataList[index]["risk_assessment"]} \n')
            click.echo(f' {click.style("Purpose of Project:", fg="green")} {dataList[index]["purpose"]} \n')
            click.echo(f' {click.style("Completion Cost in USD:", fg="green")} {dataList[index]["completion_cost"]} \n')
            click.echo(f' {click.style("Completion Date:", fg="green")} {dataList[index]["completion_date"]} \n')
            click.echo(f' {click.style("Scope of Completion:", fg="green")} {dataList[index]["scope_completion"]} \n')
            click.echo(f' {click.style("Geographical Latitude Coodinates:", fg="green")} {dataList[index]["latitude"]} \n')
            click.echo(f' {click.style("Geographical Longitude Coodinate:", fg="green")} {dataList[index]["longitude"]} \n')
            # click.echo('------------------------------------------------------------------------------\n\n')



def displayContractResults(data):
    
    if len(json.loads(data)) > 0:
        count = 0
        dataList = json.loads(data)
        # print(data)
        for index in range(len(dataList)):
            count += 1
            contractname = dataList[index]["contract_title"]
            click.echo(f' {click.style(f"======> Contract {str(count)} ({contractname}): <======", fg="yellow")} \n')
            click.echo(f' {click.style("ID:", fg="green")} {dataList[index]["contractid"]} \n')
            click.echo(f' {click.style("Title:", fg="green")} {dataList[index]["contract_title"]} \n')
            click.echo(f' {click.style("Number of Firms Tendering:", fg="green")} {dataList[index]["firms_trending"]} \n')
            click.echo(f' {click.style("Admin Entity:", fg="green")} {dataList[index]["contract_admin_entity"]} \n')
            click.echo(f' {click.style("Estimated Cost:", fg="green")} {dataList[index]["cost_currency"]} {dataList[index]["cost_estimate"]} \n')
            click.echo(f' {click.style("Actual Contract Cost:", fg="green")} {dataList[index]["price_currency"]} {dataList[index]["contract_price"]} \n')
            click.echo(f' {click.style("Scope:", fg="green")} {dataList[index]["work_scope"]} \n')
            click.echo(f' {click.style("Prospective Commencement Date:", fg="green")} {dataList[index]["prospective_start_date"]} \n')
            click.echo(f' {click.style("Prospective Completion Date:", fg="green")} {dataList[index]["prospective_end_date"]} \n')
            click.echo(f' {click.style("Actual Commencement Date:", fg="green")} {dataList[index]["act_start_date"]} \n')
            click.echo(f' {click.style("Actual Completion Date:", fg="green")} {dataList[index]["act_end_date"]} \n')
            click.echo(f' {click.style("Contract Duration:", fg="green")} {dataList[index]["duration"]} \n')
