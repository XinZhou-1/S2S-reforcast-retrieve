#!/bin/sh
#################################
# bash Job to merge the perturbed run and controled run on local machines
#################################
# where the model output directory is
MODEL=/nfs/b0128/Users/earxzho/S2S/data/ECMWF/ssw-archive

#Where you store the combined file
mkdir /nfs/b0128/Users/earxzho/S2S/data/ECMWF/FINAL
FINAL=/nfs/b0128/Users/earxzho/S2S/data/ECMWF/FINAL

cd $MODEL 
for runs in *
do
#put the temporal files to the given experiment, then will delete it to save disk space
mkdir $FINAL/$runs
cd $MODEL/$runs
for filename in ecmf_cfpl*.grb
do 
# echo "ecmf_pfpl${filename:9}"
#echo $filename
cat "ecmf_pfpl${filename:9}" $filename > $FINAL/$runs/"merge${filename:9}"
grib_to_netcdf -u time -o $FINAL/$runs/"ecmf${filename:9:11}.nc" $FINAL/$runs/"merge${filename:9}" 
done 

rm -r $FINAL/$runs/*.grb
done



