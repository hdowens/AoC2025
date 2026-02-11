echo "Advent of Code 2025 Runner";
echo "-------------------------------------";
.venv/Scripts/activate
for i in $(seq -w 1 12); 
    do echo "Day: $i";
    cd  "day$i";
    python3 "day$i".py -p;
    echo "-------------------------------------";
    cd ..
done