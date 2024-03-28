# Generate every possible value
Generating big files takes space. Consider your `arr,min,max` values.

#### Usage:

`python3 index.py <arr> <min> <max> `

#### Arguments:

`arr`: num | alphalower | alphaupper | custom separated by commas <br>

`min`: minimum word length <br>

`max`: maximum word length

#### Const values:

`SAVE_PATH`: Path where the file will be downloaded to. (default ~) <br>

`BUFFER`: How many times a file will be written to. (default 10) <br>
- Low values  = higher memory overhead, lower drive overhead. <br>
- High values = lower memory overhead, higher drive overhead
