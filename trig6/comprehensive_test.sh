#!/bin/bash
# TRIG6 Comprehensive Test Suite

echo "=========================================="
echo "TRIG6 Comprehensive Test Suite"
echo "=========================================="
echo ""

echo "1. Doctor self-validation (8 tests)..."
python3 trig6.py doctor
echo ""

echo "2. Vector trigonometry (45°)..."
python3 trig6.py vector --theta 45
echo ""

echo "3. Bridle tension (300 lbf at 30°)..."
python3 trig6.py bridle --load 300 --theta 30
echo ""

echo "4. Highline tension (200 lbf, 10 ft sag)..."
python3 trig6.py highline --load 200 --sag 10
echo ""

echo "5. Fall impact force (200 lbf, FF 1.0)..."
python3 trig6.py impact --weight 200 --ff 1
echo ""

echo "6. Citation lookup..."
python3 trig6.py cite rope.knot.figure_8_on_bight | head -12
echo ""

echo "7. Model explanation..."
python3 trig6.py explain bridle_two_leg_equal_angle
echo ""

echo "8. List models..."
python3 trig6.py list models | head -5
echo ""

echo "9. Core modules self-test..."
python3 core/units.py | tail -3
python3 core/citations.py | tail -3
echo ""

echo "10. Domain modules self-test..."
python3 domains/rope/__init__.py | head -5
python3 domains/khaos/__init__.py | head -5
echo ""

echo "11. SAGCO bootloader..."
python3 sagco/bootloader.py | head -15
echo ""

echo "12. Chess debate engine..."
python3 games/chess_debate.py | head -10
echo ""

echo "=========================================="
echo "All Tests Complete!"
echo "=========================================="
