FROM ubuntu:20.04
RUN apt-get update && apt-get install -y libbz2-dev liblzma-dev software-properties-common 
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y python3.6 python3-pip
RUN pip3 install svim
COPY runSvim.sh ./runSvim.sh
RUN chmod +x runSvim.sh
