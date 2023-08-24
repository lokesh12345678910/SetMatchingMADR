#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 input_csv output_dir p_min"
    exit 1
fi

inputSpreadSheet=$1
outputDirectory=$2
p_min=$3
failed_runs=0

while true; do
    #python setMatchingWhileLoop.py FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutputLoop/ 0.01
    #./setMatchingWhileLoop.sh FINAL_R01_LRT_PreTx_Probing_DataSheet.csv trialOutputLoop/ 0.01
    python setMatchingWhileLoop.py "$inputSpreadSheet" "$outputDirectory" "$p_min"
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Script executed successfully."
        break
    else
        ((failed_runs++))  # Increment the failed_runs count
        echo "Generated sets didn't fulfill p value requirements. Regenerating sets..."
    fi
done

# Print the number of failed runs at the end
echo "Number of combinations tried out before all p values were > p_min: $failed_runs"