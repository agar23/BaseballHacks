
import requests
import json
import csv
from matplotlib import pyplot
from numpy import mean
from numpy import std
from numpy import cov
from scipy.stats import pearsonr
from scipy.stats import spearmanr

url = 'http://lookup-service-prod.mlb.com/json/named.team_seas_results.bam'

def read_pop_crime_data():
  reader = csv.DictReader(open("resources/mass_pop_crime.csv"))
  dict_list = []
  for line in reader:
      dict_list.append(line)
  return dict_list

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
  pop_crime_data = read_pop_crime_data()
  
  yearly_pop = []
  yearly_crime_index = []
  yearly_wins = []
  data_for_chart1 = []
  data_for_chart2 = []
  crime_for_max_win = []
  pop_for_max_win = []

  for d in red_sox_data:
    for pd in pop_crime_data:
      if (d["season"] == pd["year"]):
        curr_crime = pd["crime"].replace(",", "")
        curr_pop = pd["population"].replace(",", "")
        if (int(d["w"]) >= 95):
          crime_for_max_win.append(int(curr_crime))
          pop_for_max_win.append(int(curr_pop))
        yearly_wins.append(int(d["w"]))
        yearly_crime_index.append(int(curr_crime))
        yearly_pop.append(int(curr_pop))
        data_for_chart1.append({'x': int(curr_crime), 'y': int(d["w"]), 'z': d["season"]})
        data_for_chart2.append({'x': int(curr_pop), 'y': int(d["w"]), 'z': d["season"]})

  optimal_range_min_crime = min(crime_for_max_win)
  optimal_range_max_crime = max(crime_for_max_win)
  covariance_crime = cov(yearly_crime_index, yearly_wins)
  pearson_corr_crime, _ = pearsonr(yearly_crime_index, yearly_wins)
  spearman_corr_crime, _ = spearmanr(yearly_crime_index, yearly_wins)

  optimal_range_min_pop = min(pop_for_max_win)
  optimal_range_max_pop = max(pop_for_max_win)
  covariance_pop = cov(yearly_pop, yearly_wins)
  pearson_corr_pop, _ = pearsonr(yearly_pop, yearly_wins)
  spearman_corr_pop, _ = spearmanr(yearly_pop, yearly_wins)

  print(crime_for_max_win)
  print(pop_for_max_win)
  print('yearly_crime_index: mean=%.3f stdv=%.3f' % (mean(yearly_crime_index), std(yearly_crime_index)))
  print('yearly_pop: mean=%.3f stdv=%.3f' % (mean(yearly_pop), std(yearly_pop)))
  print('yearly_wins: mean=%.3f stdv=%.3f' % (mean(yearly_wins), std(yearly_wins)))
  print('covariance crime:')
  print(covariance_crime)
  print('covariance population:')
  print(covariance_pop)
  print('Pearsons correlation crime: %.3f' % pearson_corr_crime)
  print('Spearmans correlation crime: %.3f' % spearman_corr_crime)
  print('Pearsons correlation population: %.3f' % pearson_corr_pop)
  print('Spearmans correlation population: %.3f' % spearman_corr_pop)

  final_result_crime = {
    'pearsonCorr': pearson_corr_crime,
    'optimalRangeMin': optimal_range_min_crime,
    'optimalRangeMax': optimal_range_max_crime,
    'chartData': data_for_chart1
  }

  final_result_population = {
    'pearsonCorr': pearson_corr_pop,
    'optimalRangeMin': optimal_range_min_pop,
    'optimalRangeMax': optimal_range_max_pop,
    'chartData': data_for_chart2
  }

  with open('results/crime.json', 'w') as fp:
    json.dump(final_result_crime, fp, indent=4)
  
  with open('results/population.json', 'w') as fp:
    json.dump(final_result_population, fp, indent=4)

  # pyplot.scatter(yearly_pop, yearly_wins)
  # pyplot.show()

find_correlation()