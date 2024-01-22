#!/bin/bash
source /root/.bashrc
source activate /opt/conda/envs/hd-seq-id-env
cd /home/HD-SEQ-ID/
python3 hd_seq_id -i /mnt/input/ -o /mnt/output/ -m models/ -write False
