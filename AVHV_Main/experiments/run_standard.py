from AVHV_Main.experiments.experiments import run_standard_experiments, \
    run_ratio_experiments

# Runs only standard experiments.
# 50% capacity
run_standard_experiments(capacity=50)

# 100% capacity
run_standard_experiments()
