import bs4
import requests
from tqdm import tqdm


def schmidt_tools(verbose=True):
    """ Scrape the Schmidt Futures forum learning web page for Education project ideas

    >>> projects = schmidt_tools(verbose=False)
    >>> len(projects)
    40
    """
    base_url = 'https://futuresforumonlearning.org/competition-finalists/'
    page = requests.get(base_url)
    soup = bs4.BeautifulSoup(page.text)
    finalists = soup.find_all('div', {'class': 'accrod-finalists'})

    if verbose:
        print('# Schmidt Futures Tools Competition Finalists')
        print()
        print('1. [Small](#catalyst-prize-finalists)')
        print('2. [Medium](mid-range-prize-finalists)')
        print('3. [Large](large-prize-finalists)')

    projects = []
    for category in finalists:
        group = category.find('div', {'class': 'wpsm_panel-group'})
        tier = category.find('h3')
        if verbose:
            print()
            print()
            print('## ' + tier.text.strip())
            print()
        panels = group.find_all('div', {'class': 'wpsm_panel'})
        for panel in tqdm(panels):
            heading = panel.find('div', {'class': 'wpsm_panel-heading'})
            title = heading.find('h4', {'class': 'wpsm_panel-title'})
            collapsed = panel.find('div', {'class': 'wpsm_panel-collapse'})
            body = collapsed.find('div', {'class': "wpsm_panel-body"})
            team = body.h4.text.strip()
            paragraphs = [p.text.strip() for p in body.find_all('p')]
            if verbose:
                print('### ' + title.text.strip())
                print()
                print('#### ' + team)
                print()
                for p in paragraphs:
                    print('  ' + p)
                    print()
            projects.append({
                'team': team[5:].strip() if team.lower().startswith('team:') else team,
                'summary': paragraphs,
                'title': title.text.strip(),
                'category': tier.text})

    return projects
