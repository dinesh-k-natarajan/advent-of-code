DAY=$(date +'%d')
scp -r template/ $DAY 
cd $DAY
for file in template.*
do 
    mv "$file" "${file/template./$DAY.}"
done
sed -i "s/1.example/$DAY.example/" $DAY.py
sed -i "s/1.in/$DAY.example/" $DAY.py
sed -i "s/1/$DAY/" README.md