from AVHV_Main.experiments.experiments import run_standard_experiments, \
    run_ratio_experiments

# Runs both standard and ratio experiments.
# 50% capacity
run_ratio_experiments(capacity=50)

# 100% capacity
run_ratio_experiments()
