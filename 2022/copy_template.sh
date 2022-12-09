DAY=$(date +'%d')
scp -r template/ $DAY 
cd $DAY
DAY=$(date +'%e')
for file in template.*
do 
    mv "$file" "${file/template./$DAY.}"
done