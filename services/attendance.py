
import requests
import json
from matplotlib import pyplot
from numpy import mean
from numpy import std
from numpy import cov
from scipy.stats import pearsonr
from scipy.stats import spearmanr

url = 'http://lookup-service-prod.mlb.com/json/named.team_seas_results.bam'

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
  yearly_attendance = []
  yearly_wins = []
  yearly_losses = []
  attendance_for_max_win = []
  attendance_for_min_win = []
  max_win = 95 # max_win = max(yearly_wins)
  min_win_not_zero = 46
  data_for_chart = []

  for d in red_sox_data:
    # if (int(d["w"]) < min_win_not_zero and int(d["attendance"]) != 0):
    #   min_win_not_zero = int(d["w"])
    if (int(d["w"]) >= max_win and int(d["attendance"]) != 0):
      attendance_for_max_win.append(int(d["attendance"]))
    if (int(d["w"]) == min_win_not_zero):
      attendance_for_min_win.append(d)
    yearly_attendance.append(int(d["attendance"]))
    yearly_wins.append(int(d["w"]))
    yearly_losses.append(int(d["l"]))
    data_for_chart.append({'x': int(d["attendance"]), 'y': int(d["w"]), 'z': d["season"]})

  optimal_range_min = min(attendance_for_max_win)
  optimal_range_max = max(attendance_for_max_win)
  covariance = cov(yearly_attendance, yearly_wins)
  pearson_corr, _ = pearsonr(yearly_attendance, yearly_wins)
  spearman_corr, _ = spearmanr(yearly_attendance, yearly_wins)

  print('yearly_attendance: mean=%.3f stdv=%.3f' % (mean(yearly_attendance), std(yearly_attendance)))
  print('yearly_wins: mean=%.3f stdv=%.3f' % (mean(yearly_wins), std(yearly_wins)))
  print('covariance:')
  print(covariance)
  print('Pearsons correlation: %.3f' % pearson_corr)
  print('Spearmans correlation: %.3f' % spearman_corr)
  print('Data for most amount of wins in a season:')
  print(str(attendance_for_max_win))

  final_result = {
    'pearsonCorr': pearson_corr,
    'optimalRangeMin': optimal_range_min,
    'optimalRangeMax': optimal_range_max,
    'chartData': data_for_chart
  }

  with open('results/attendance.json', 'w') as fp:
    json.dump(final_result, fp, indent=4)

  # print('Data for least amount of wins in a season:')
  # print(str(attendance_for_min_win))

  # pyplot.scatter(yearly_attendance, yearly_wins)
  # pyplot.show()

find_correlation()