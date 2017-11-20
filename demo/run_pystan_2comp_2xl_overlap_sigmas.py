import csv
import generate
import getData
import pystan
import sys
import stan_utility_copy as stan_utility

#arg = sys.argv[1]
filename = "planets_WASP.csv"
modelfile = "powerlaw_2comp_2xl_overlap_sigmas_alltransit.stan"
nChains = 2
nIterations = 10000
nThin = 1
nJobs = -1

data = getData.NEA_to_dict(filename)
Stan_data = getData.create_Stan_input_mixture_sigmas_alltransit(data)

Stan_ICs = generate.ICs_2comp_2xl_overlap_sigmas_alltransit([[0.35,0.65], [0.5,-1.5], [1.05, 2.3], 12.], Stan_data, nChains)

fit = pystan.stan(file=modelfile, data=Stan_data, iter=nIterations, chains=nChains, thin=nThin, init=Stan_ICs, n_jobs=nJobs)

postSamp = getData.stan_output_to_posterior_samples_2comp_2xl_overlap(fit.extract())

with open("postSamp_WASP_2comp_2xl_overlap_sigmas.txt", "w") as f:
#with open("postSamp_WASP_2comp_2xl_overlap_sigmas." + arg + ".txt", "w") as f:
    writer = csv.writer(f, delimiter=' ')
    for item in postSamp:
        writer.writerow(list(item))


stan_utility.check_treedepth(fit)
stan_utility.check_energy(fit)
stan_utility.check_div(fit)
