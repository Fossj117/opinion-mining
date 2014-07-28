# Update featurization? 
# Run this shell script to retrain the models

rm ./results/*
rm ./results/final_models

python 1_featurize_training_dat.py
domino run 2_grid_search_CV.py
