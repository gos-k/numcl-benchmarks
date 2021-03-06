#!/bin/bash

# Usage : ./report.sh [regexp]

regexp=$1

if [ -z $regexp ]
then
    regexp=".*"
else
    ls numcl/logs/*.log | grep "$regexp" | xargs -n 1 rm -v
fi

make -j $(($(grep -c "^processor" /proc/cpuinfo)/2))

titles (){
    cat numcl/logs/*.log numpy/logs/*.log | awk -f report.awk | cut -f1 | sort | uniq
}
     
collect_numcl (){
    titles | while read title
    do
        cat numcl/logs/*.log | awk -f report.awk | (grep -m 1 $title || echo "N/A" ) | cut -f2
    done
}

collect_numpy (){
    titles | while read title
    do
        cat numpy/logs/*.log | awk -f report.awk | (grep -m 1 $title || echo "N/A" ) | cut -f2
    done
}

collect_ratio (){
    paste <(collect_numcl) <(collect_numpy) | while read numcl numpy
    do
        python -c "print('{:6.4g}'.format($numcl / $numpy))" 2>/dev/null || echo "N/A"
    done
}


(
    echo "title numcl numpy cl/py"
    paste <(titles) \
          <(collect_numcl) \
          <(collect_numpy) \
          <(collect_ratio) \
          | grep "$regexp"
) | column -t | tee $(date +%Y%m%d%H%M).log
