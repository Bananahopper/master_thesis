import os

# ============================ PATH CONSTANTS ============================
WORK_PATH = "/scratch/users/ggaspar/CaPTk"
ANALYSIS_FOLDER = os.path.join(WORK_PATH, "output_analysis")

if not os.path.exists(ANALYSIS_FOLDER):
    os.makedirs(ANALYSIS_FOLDER)
