## Dependencies
```bash
pip install bleak numpy cv2
pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
```

## How to run
```bash
python3 ./maze_solver.py ./images/curved.jpg
```
```bash
python3 ./maze_solver.py ./images/straight.jpg
```

## Test arucode angle finder
```bash
python3 arucode_cmd.py "./test_arucode_files/Robot in maze.jpg"
```
```bash
python3 arucode_cmd.py "./test_arucode_files/0.jpg"
```
```bash
python3 arucode_cmd.py "./test_arucode_files/90.jpg"
```