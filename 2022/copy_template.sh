DAY=$(date +'%d')
scp -r template/ $DAY 
cd $DAY
for file in template.*
do 
    mv "$file" "${file/template./$DAY.}"
done
sed -i "s/date.example/$DAY.example/" $DAY.py
sed -i "s/date.in/$DAY.example/" $DAY.py
sed -i "s/date/$DAY/" README.md