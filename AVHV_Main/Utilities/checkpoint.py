import os
import pickle


def read_checkpoint_file(obj, checkpoint_file):
    # Read the content of the checkpoint file.
    with open(checkpoint_file, "r") as f:
        content = f.read()

        if content == '':
            curr_time = 0.0
        else:
            try:
                curr_time = float(content)
            except ValueError as e:
                curr_time = 0.0

    return curr_time


def load_checkpoint(obj, checkpoint_file):
    # Check to see if there is a checkpoint file.
    if os.path.exists(checkpoint_file):
        read_checkpoint_file(obj, checkpoint_file)
    else:
        # Create a checkpoint file.
        with open(checkpoint_file, "w") as f:
            f.write(str(0.0))

    return read_checkpoint_file(obj, checkpoint_file)


def save_checkpoint(obj, curr_time, end_time, checkpoint_file, state_file):
    # Rewrite checkpoint file with new timestamp.
    with open(checkpoint_file, "w") as f:

        # If simulation is over, remove state file and write timestamp as
        # `0.0` in check point file.
        if curr_time >= end_time:
            f.write(str(0.0))
            os.remove(state_file)
            if os.path.exists(state_file + '.bak'):
                os.remove(state_file + '.bak')
        else:
            f.write(str(curr_time))

            # Create backup of state file.
            if os.path.exists(state_file):
                backup_file = state_file + '.bak'
                if os.path.exists(backup_file):
                    try:
                        os.remove(backup_file)
                    except PermissionError:
                        pass

                try:
                    os.rename(state_file, backup_file)
                except PermissionError:
                    pass
                except FileExistsError:
                    pass

            # if os.path.exists(state_file):
            #     os.remove(state_file)

            # Save
            with open(state_file, 'wb') as g:
                pickle.dump(obj.__dict__, g)
