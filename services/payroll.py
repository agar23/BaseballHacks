
import requests
import json
from matplotlib import pyplot
from numpy import mean
from numpy import std
from numpy import cov
from scipy.stats import pearsonr
from scipy.stats import spearmanr

url = 'http://lookup-service-prod.mlb.com/json/named.team_seas_results.bam'

def generate_red_sox_owner_data():
  owner_data = []
  for x in range(1901, 2020):
    if (x >= 1901 and x < 1903):
      owner_data.append({
        'name': 'Charles Somers',
        'season': str(x)
      })
    elif (x >= 1903 and x < 1904):
      owner_data.append({
        'name': 'Henry Killilea',
        'season': str(x)
      })
    elif (x >= 1904 and x < 1914):
      owner_data.append({
        'name': 'John I. Taylor',
        'season': str(x)
      })
    elif (x >= 1914 and x < 1916):
      owner_data.append({
        'name': 'Joseph Lannin',
        'season': str(x)
      })
    elif (x >= 1916 and x < 1923):
      owner_data.append({
        'name': 'Harry Frazee',
        'season': str(x)
      })
    elif (x >= 1923 and x < 1933):
      owner_data.append({
        'name': 'Bob Quinn',
        'season': str(x)
      })
    elif (x >= 1933 and x < 1976):
      owner_data.append({
        'name': 'Tom Yawkey',
        'season': str(x)
      })
    elif (x >= 1976 and x < 1992):
      owner_data.append({
        'name': 'Jean R. Yawkey',
        'season': str(x)
      })
    elif (x >= 1992 and x < 2001):
      owner_data.append({
        'name': 'John Harrington',
        'season': str(x)
      })
    else:
      owner_data.append({
        'name': 'John W. Henry',
        'season': str(x)
      })
  with open('resources/red_sox_owners.json', 'w') as fp:
    json.dump(owner_data, fp, indent=4)

def get_red_sox_data():
	params = {'team_id': '111'}
	try:
		r = requests.get(url = url, params = params)
		r.raise_for_status()
	except:
		return {'error': 'Error in request'}

	if (r.status_code == 204):
		return {'error': 'None Found'}

	data = r.json()

	try: 
		if (len(data)):
			return data["team_seas_results"]["queryResults"]["row"]
	except:
		return {'error': 'None Found'}

def find_correlation():
  red_sox_data = get_red_sox_data()
  payroll_data = []
  with open('resources/red_sox_total_payroll.json') as f:
    payroll_data = json.load(f)
  
  yearly_payroll = []
  yearly_wins = []
  data_for_chart = []
  payroll_for_max_win = []

  for d in red_sox_data:
    for pd in payroll_data:
      if (d["season"] == pd["season"]):
        if (int(d["w"]) >= 95):
          payroll_for_max_win.append(pd["payroll"])
        yearly_wins.append(int(d["w"]))
        yearly_payroll.append(pd["payroll"])
        data_for_chart.append({'x': pd["payroll"], 'y': int(d["w"]), 'z': d["season"]})

  optimal_range_min = min(payroll_for_max_win)
  optimal_range_max = max(payroll_for_max_win)
  covariance = cov(yearly_payroll, yearly_wins)
  pearson_corr, _ = pearsonr(yearly_payroll, yearly_wins)
  spearman_corr, _ = spearmanr(yearly_payroll, yearly_wins)

  print(payroll_for_max_win)
  print('yearly_payroll: mean=%.3f stdv=%.3f' % (mean(yearly_payroll), std(yearly_payroll)))
  print('yearly_wins: mean=%.3f stdv=%.3f' % (mean(yearly_wins), std(yearly_wins)))
  print('covariance:')
  print(covariance)
  print('Pearsons correlation: %.3f' % pearson_corr)
  print('Spearmans correlation: %.3f' % spearman_corr)

  final_result = {
    'pearsonCorr': pearson_corr,
    'optimalRangeMin': optimal_range_min,
    'optimalRangeMax': optimal_range_max,
    'chartData': data_for_chart
  }

  with open('results/payroll.json', 'w') as fp:
    json.dump(final_result, fp, indent=4)

  # pyplot.scatter(yearly_payroll, yearly_wins)
  # pyplot.show()

find_correlation()