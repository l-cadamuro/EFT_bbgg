# benchmark definition
benchmarks=(
# SPACE is a separator, so don't use spaces in benchmark names
# name   chhh   ctth   cggh            cgghh             ctthh
"SM     1      1      0               0                 0"
"BM1    3.94   0.94   0.5             0.3333333333      -0.3333333333"
"BM2    6.84   0.61   0               -0.3333333333     0.3333333333  "
"BM3    2.21   1.05   0.5             0.5               -0.3333333333"
"BM4    2.79   0.61   -0.5            0.16666666667     0.3333333333  "
"BM5    3.95   1.17   0.16666666667   -0.5              -0.3333333333"
"BM6    5.68   0.83   -0.5            0.3333333333      0.3333333333"
"BM7    -0.1   0.94   0.16666666667   -0.16666666667    1"
)

## input
WSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"

for ((i = 0; i < ${#benchmarks[@]}; i++))
do
    bmpoint=${benchmarks[$i]}
    # echo "$bmpoint"
    # split the benchmark information
    set -- $bmpoint
    bmname=$1
    chhh=$2
    ctth=$3
    cggh=$4
    cgghh=$5
    ctthh=$6
    echo "Doing benchmark ${bmname}"
    echo " ... chhh  = ${chhh}"
    echo " ... ctth  = ${ctth}"
    echo " ... cggh  = ${cggh}"
    echo " ... cgghh = ${cgghh}"
    echo " ... ctthh = ${ctthh}"
    quickstats cls_limit -i ${WSpath} --poi mu_XS_HH --outname limits_${bmname}.json --fix chhh=${chhh},ctth=${ctth},cggh=${cggh},cgghh=${cgghh},ctthh=${ctthh} --blind
done

# plot them
python make_EFT_benchmarks.py