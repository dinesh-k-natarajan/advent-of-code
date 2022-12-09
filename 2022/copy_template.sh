DAY_with_pad=$(date +'%d')
DAY_without_pad=$(date +'%e')
scp -r template/ $DAY_with_pad 
cd $DAY_with_pad
for file in template.*
do 
    mv "$file" "${file/template./$DAY_without_pad.}"
done