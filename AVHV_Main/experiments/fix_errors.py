import os

# Running this file will fix many errors that occur when the experiments are
# running by removing all the state and checkpoint files (.pickle and .txt)
# of the project so that the experiment can run fresh from the beginning.

TL_checkpoint_file = "../AVHV_TL/checkpoint.txt"
CAwSD4WI_checkpoint_file = "../AVHV_CAwSD4WI/checkpoint.txt"
RN_checkpoint_file = "../checkpoint.txt"

TL_experiment_pickle = "../AVHV_Tl/state.pickle"
TL_experiment_pickle_backup = "../AVHV_Tl/state.pickle.bak"

CAwSD4WI_experiment_pickle = "../AVHV_AVHV_CAwSD4WI/state.pickle"
CAwSD4WI_experiment_pickle_backup = \
    "../AVHV_AVHV_CAwSD4WI/state.pickle.bak"

RN_experiment_pickle = "../state.pickle"
RN_experiment_pickle_backup = "../state.pickle.bak"

TL_results_pickle = "./tl_result_values.pickle"
RN_results_pickle = "./cawsd4wi_result_values.pickle"

all_state_files = [TL_checkpoint_file, CAwSD4WI_checkpoint_file,
                   RN_checkpoint_file, TL_experiment_pickle,
                   TL_experiment_pickle_backup, CAwSD4WI_experiment_pickle,
                   CAwSD4WI_experiment_pickle_backup, RN_experiment_pickle,
                   RN_experiment_pickle_backup, TL_results_pickle, RN_results_pickle]

for f in all_state_files:
    if os.path.exists(f):
        os.remove(f)

print("Errors fixed.")
