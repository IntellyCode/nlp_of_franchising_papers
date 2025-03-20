read -p "Enter remote machine: " REMOTE
unison setup -auto -batch -ui text -addpref root "ssh://go76fil@$REMOTE//scratch/go76fil/Programs/Python/Paper_Topic_Modelling/"
