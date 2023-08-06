import sys
import click

from costsekondi.authenticate import makerequest, displayPojectResults, displayContractResults

URL = "https://adminportal.costsekondi-takoradigh.org/cli?"
ENTITY = "entity="
FLAG = "&flag="


@click.group()
@click.version_option("0.0.1")
def main():
    """
        A CLI tool for CoST Sekondi-Takoradi in Ghana 
        West Africa to make the general public access their 
        Infrastructure Transparency Initiative \n\n
    """
    pass


@main.command('project', short_help='Access project data => costsekondi project --help')
@click.option('--list', 'projectlist', flag_value='list', default=True, help='List all projects')
@click.option('--lookout', 'projectid', default=True, help='Get a specific project(s) details')
def project(projectlist, projectid):
    """
        \b
        A command to access all project data, \n
        attaching some flags can fetch contract details along \n\n

        ===> 'costsekondi project --help' \n
        to display the flags of this command \n\n
    """

    flag_condition = ""
    if str(projectlist) == "":
        flag_condition = projectid
    else:
        flag_condition = projectlist
    
    url = f"{URL}{ENTITY}project{FLAG}{flag_condition}"
    result = makerequest(url)
    click.echo(f"\n {click.style('<================== PROJECT DETAILS ==================>', fg='magenta')} \n")
    displayPojectResults(result)


@main.command('contract', short_help='Access contract data => costsekondi contract --help')
@click.option('--list', 'contractlist', flag_value='list', default=True, help='List all contracts')
@click.option('--lookout', 'contractid', default=True, help='Get a specific contract(s) details')
def contract(contractlist, contractid):
    """
        \b
        A command to access all contract data, \n
        attaching some flags can fetch project details along \n\n

        ===> 'costsekondi contract --help' \n
        to display the flags of this command \n\n
    """

    flag_condition = ""
    if str(contractid) == "":
        flag_condition = contractlist
    else:
        flag_condition = contractid
    
    url = f"{URL}{ENTITY}contract{FLAG}{flag_condition}"
    result = makerequest(url)
    click.echo(f"\n{click.style('<================== CONTRACT DETAILS ==================>', fg='magenta')} \n")
    displayContractResults(result)


@main.command('about', short_help='About CoST Sekondi Takoradi => costsekondi about')
def about():
    click.echo(f"\n\n {click.style('ABOUT CoST SEKONDI TAKORADI', fg='yellow')} {click.style('(https://costsekondi-takoradigh.org/cost_takoradi)', fg='blue')} \n")
    click.echo("CoST Sekondi-Takoradi is a Subnational Chapter of CoST International, a UK registered charity (number: 1152236) working worldwide to implement transparency and accountability reform within the infrastructure sector. \n");
    click.echo("CoST works internationally with key anti-corruption organisations to facilitate the global exchange of experience and knowledge on transparency and accountability in public infrastructure. \n")
    click.echo("CoST’s international partners include, Article 19, Open Contracting Partnership, Transparency International and Hivos. CoST currently works in 14 countries spanning four continents, including five Fragile and Conflict-Affected States. \n")
    click.echo("CoST Sekondi-Takoradi is Championed by the Sekondi-Takoradi Metropolitan Assembly and guided by a Multi-Stakeholder Group (MSG) of nine persons who lead, plan, engage together to build trust, transparency and accountability amongst the three sectors. In Sekondi-Takoradi, the Initiative is hosted by the Development Planning Unit of the Sekondi-Takoradi Metropolitan Assembly. \n")
    click.echo("Publicly-funded infrastructure in Ghana is subject to the Public Procurement Act 2003 (as amended in 2016, Act 914) which gives clear procurement guidelines on the award of public contract/works. Over the years, most subnational governments including STMA, have performed well with regards to enacting this Act without any serious irregularities. However, information on public infrastructure such as project details, contract award processes and implementation monitoring has been limited to the general public. \n")
    click.echo("There are inadequate opportunities for citizens to oversee infrastructure projects which sometimes result in the delay and cancellation of projects. This has had a knock-on effect on public trust and confidence in officials. According to the Open Government Partnership (OGP), around 70% of citizens in STMA do not understand the procurement processes. \n")
    click.echo("Sekondi Takoradi Metropolitan Assembly joined CoST International in March 2019. STMA becomes the fifth CoST member in Africa and the first sub national member in CoST International family. This membership comes at a time when STMA wishes to operationalize their Open Government Action Plan commitment on enhancing Infrastructure Transparency. \n")
    click.echo("They either lack access to infrastructure project documents or are unable to interpret the information in them, which significantly impacts their ability to hold officials to account. In light of this, the CoST approach focuses on increasing data disclosure on infrastructure projects and turning it into compelling information so that key issues are put into the public domain. \n")
    click.echo("This a true example of how CoST helps countries implement their specific commitments in relation to its core features. The chapter has established an MSG, a team of Assurance professionals' and commenced their first assurance process on 3 projects; the chapter has developed its governance policies and embraced capacity building for media, Civil Society and Procurement Entities on CoST. \n")
    click.echo("This helps to inform and empower citizens to demand for accountability from duty-bearers and derive the optimum benefit from infrastructure investments. \n")
    click.echo("STMA is also planning to design an Information Portal for Infrastructure Projects. \n")
    click.echo(f"Visit website for more: {click.style('https://costsekondi-takoradigh.org', fg='blue')} \n")




if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("\n\n\n CoSTSekondi \n\n")
    main()