Write-Host "Advent of Code 2025 Runner"
Write-Host "-------------------------------------"

$totalTime = Measure-Command {

    1..12 | ForEach-Object {
        $day = "{0:D2}" -f $_   # zero pad (01, 02, ...)
        
        Write-Host "Day: $day"
        Push-Location "day$day"
        
        $dayTime = Measure-Command {
            uv run "day$day.py" -p
        }

        Pop-Location

        Write-Host ("Time for Day {0}: {1:N3} seconds" -f $day, $dayTime.TotalSeconds)
        Write-Host "-------------------------------------"
    }

}

Write-Host ("TOTAL TIME: {0:N3} seconds" -f $totalTime.TotalSeconds)
