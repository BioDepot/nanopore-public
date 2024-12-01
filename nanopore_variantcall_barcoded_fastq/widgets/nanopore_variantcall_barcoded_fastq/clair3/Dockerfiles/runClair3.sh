#!/bin/bash
shopt -s extglob
inputArgs=("$@")

# Optional parameters are stored as environment variables,
# need to format them such that `--PARAM=VALUE`.
# Function to filter and format environment variables
generate_arguments() {
    for var in $(printenv | grep -E '^(CONDA_|PWD|HOME|LANG|TERM|SHLVL|PATH|RERIO|_|HOSTNAME|LC_ALL)='); do
        # Ignore these variables
        continue
    done

    for var in $(printenv | grep -Ev '^(CONDA_|PWD|HOME|LANG|TERM|SHLVL|PATH|RERIO|_|HOSTNAME|LC_ALL)'); do
        # Split the variable into name and value
        IFS='=' read -r name value <<< "$var"
        # Print the argument in the required format
        echo "--$name=$value"
    done
}

# Generate arguments from environment variables
optionalArgs=$(generate_arguments)

# Using Rerio model for Clair3, need to download from GitHub
if [ -n "$RERIO" ]; then 
	git clone https://github.com/nanoporetech/rerio && python3 rerio/download_model.py --clair3 "rerio/clair3_models/${MODEL}_model" 
	MODEL_ARG="/opt/bin/rerio/clair3_models/${MODEL}"
else # Using pre-existing model
	MODEL_ARG="/opt/models/${MODEL}"
fi

# Run Clair3
echo /opt/bin/run_clair3.sh -m "${MODEL_ARG}" "${inputArgs[@]}" "${optionalArgs}"
eval /opt/bin/run_clair3.sh -m "${MODEL_ARG}" "${inputArgs[@]}" "${optionalArgs}"