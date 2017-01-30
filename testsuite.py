"""
A simple testing suite for Fifteen Puzzle
"""
import poc_simpletest
import user37_wBv4xkHaMMDFxyD_7 as mycode

def run_test_lower_row_invariant():
    """
    Tests for verifying Puzzle method lower_row_invariant
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test 1, 2x2, condition 1, 2, 3 is true
    puzzle = mycode.Puzzle(2, 2, [[0, 1], [2, 3]])
    suite.run_test(puzzle.lower_row_invariant(0,0), True, "lower_row_invariant, test1.")
    
    #test 2, 2x2, condition 1 is false
    puzzle = mycode.Puzzle(2, 2, [[2, 1], [0, 3]])
    suite.run_test(puzzle.lower_row_invariant(0,0), False, "lower_row_invariant, test2.")
    
    #test 3, 2x2, condition 2 is false
    puzzle = mycode.Puzzle(2, 2, [[0, 2], [1, 3]])
    suite.run_test(puzzle.lower_row_invariant(0,0), False, "lower_row_invariant, test3.")
    
    #test 4, 2x2, condition 3 is false
    puzzle = mycode.Puzzle(2, 2, [[0, 3], [1, 2]])
    suite.run_test(puzzle.lower_row_invariant(0,0), False, "lower_row_invariant, test4.")
    
    #test 5, 4X4, conditions are True
    puzzle = mycode.Puzzle(4, 4, [[4,2,3,7], [8,5,6,10], [9,1,0,11], [12,13,14,15]])
    suite.run_test(puzzle.lower_row_invariant(2,2), True, "lower_row_invariant, test5.")

    # report number of tests and failures
    suite.report_results()    

def run_test_solve_interior_tile():
    """
    Tests for verifying Puzzle method solve_interior_tile
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test 1, 3x3, target_tile 8 above zero_tile
    puzzle = mycode.Puzzle(3, 3, [[4,3,8], [1,2,5], [6,7,0]])
    suite.run_test(puzzle.solve_interior_tile(2,2), "uulddruld", "test1, solve_interior_tile, 3x3")
    #print puzzle # updated puzzle [[4,2,3], [1,2,7], [6,0,8]]
    
    #test 2, 3x3, target_tile 8 above zero_tile
    puzzle = mycode.Puzzle(3, 3, [[4,3,1], [8,2,5], [6,7,0]])
    suite.run_test(puzzle.solve_interior_tile(2,2), "ullurrdldruld", "test2, solve_interior_tile, 3x3")
    #print puzzle # updated puzzle [[4,3,1], [6,2,5], [7,0,8]]
    
    #test 3, 4x4, target_tile 13 above zero_tile
    puzzle = mycode.Puzzle(4, 4, [[4,13,1,3], [5,10,2,7], [8,12,6,11], [9,0,14,15]])
    suite.run_test(puzzle.solve_interior_tile(3,1), "uuulddrulddruld", "test3, solve_interior_tile, 4x4")
    
    #test 4, 3x3, target_tile above zero
    puzzle = mycode.Puzzle(3, 3, [[2,4,5], [3,1,8], [6,7,0]])
    suite.run_test(puzzle.solve_interior_tile(2,2), "uld", "test4, solve_interior_tile")
    
    #test5, 3x3, target top left
    puzzle = mycode.Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
    suite.run_test(puzzle.solve_interior_tile(2,2), "ululdrruldrulddruld", "test5 solve_interior_tile")
    
    #test6, 3x3, target top left
    puzzle = mycode.Puzzle(3, 3, [[7, 5, 6], [2, 4, 3], [1, 0, 8]])
    suite.run_test(puzzle.solve_interior_tile(2,1), "ulurdldruld", "test6 solve_interior_tile")
    
    # report number of tests and failures
    suite.report_results()    

def run_test_solve_col0_tile():
    """
    Tests for verifying Puzzle method solve_col0_tile
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    #test 1, 3x3, target_tile right of zero tile
    puzzle = mycode.Puzzle(3, 3, [[1,2,6],[3,4,5],[0,7,8]])
    suite.run_test(puzzle.solve_col0_tile(2), "ururldruldrulldruldrdlurdluurddlurr", "test1, solve_col0_tile")
    #print puzzle #step3: [[4,3,5],[1,2,0][6,7,8]])
    
    #test 2, 3x3, target_tile above zero tile
    puzzle = mycode.Puzzle(3, 3, [[6,2,1],[3,4,5],[0,7,8]])
    suite.run_test(puzzle.solve_col0_tile(2), "uurdlruldrdlurdluurddlurr", "test2, solve_col0_tile")
    #print puzzle #step3: [[2,3,1],[4,5,0][6,7,8]])

    #test 3, 4x4, lucky: target_tile in place after step 1 of solution strategy
    puzzle = mycode.Puzzle(4, 4, [[5,4,1,3],[10,8,2,7],[12,9,6,11],[0,13,14,15]])
    suite.run_test(puzzle.solve_col0_tile(3), "urrr", "test2, solve_col0_tile")
    #print puzzle
    
    #test 4, 4x4, target tile right of zero tile
    puzzle = mycode.Puzzle(4, 4, [[12,4,1,3],[10,8,2,7],[5,9,6,11],[0,13,14,15]])
    suite.run_test(puzzle.solve_col0_tile(3), "uuurdldruldruldrdlurdluurddlurrr", "test4, solve_col0_tile")
    #print puzzle
    
    #test 5, 4x4, target tile above zero tile
    puzzle = mycode.Puzzle(4, 4, [[3,4,1,12],[10,8,2,7],[5,9,6,11],[0,13,14,15]])
    suite.run_test(puzzle.solve_col0_tile(3), "urururldruldrullddruldrulldruldrdlurdluurddlurrr", "test5, solve_col0_tile")
    #print puzzle
    
    # report number of tests and failures
    suite.report_results()    

def run_test_row1_invariant():
    """
    Tests for verifying Puzzle method row1_invariant
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test1, True
    puzzle = mycode.Puzzle(4, 4, [[4,6,1,3],[5,2,0,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.row1_invariant(2), True, "test1, row1_invariant.")
    
    # report number of tests and failures
    suite.report_results()

def run_test_row0_invariant():
    """
    Tests for verifying Puzzle method row0_invariant
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test1, True
    puzzle = mycode.Puzzle(4, 4, [[4,2,0,3],[5,1,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.row0_invariant(2), True, "test1, row0_invariant.")
    
    # report number of tests and failures
    suite.report_results()

def run_test_solve_row1_tile():
    """
    Tests for verifying Puzzle method solve_row1_tile
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test1
    puzzle = mycode.Puzzle(4, 4, [[4,6,1,3],[5,2,0,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_row1_tile(2), "uldruldur", "test1 solve_row1_tile.")
    
    #test2
    puzzle = mycode.Puzzle(3, 3, [[2,4,5],[3,1,0],[6,7,8]])
    suite.run_test(puzzle.solve_row1_tile(2), "u", "test2 solve_row1_tile.")
    
    # report number of tests and failures
    suite.report_results()

def run_test_solve_row0_tile():
    """
    Tests for verifying Puzzle method solve_row0_tile
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test 1: 3x3 board
    puzzle = mycode.Puzzle(3, 3, [[3,4,0],[2,1,5],[6,7,8]])
    suite.run_test(puzzle.solve_row0_tile(2), "ldlurdlurrdluldrruld", "test1 solve_row0_tile") 

    #test 2: 3x3 board
    puzzle = mycode.Puzzle(3, 3, [[2,4,0],[3,1,5],[6,7,8]])
    suite.run_test(puzzle.solve_row0_tile(2), "lduldruldurdlurrdluldrruld", "test2 solve_row0_tile")     
    
    #test 3: 4x4 board, target at (0,2)
    puzzle = mycode.Puzzle(4, 4, [[6,1,3,0],[4,5,2,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_row0_tile(3), "ld", "test3 solve_row0_tile")
    
    #test 4: 4x4 board, target at (1,2)
    puzzle = mycode.Puzzle(4, 4, [[6,1,2,0],[4,5,3,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_row0_tile(3), "lduldurdlurrdluldrruld", "test4 solve_row0_tile")
    
    #test 5: 4x4 board, target at (0,0)
    puzzle = mycode.Puzzle(4, 4, [[3,6,1,0],[4,5,2,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_row0_tile(3), "ldulldruldurrdlurdlurrdluldrruld", "test5 solve_row0_tile")
    
    #test 6: 4x4 board, target at (1,0)
    puzzle = mycode.Puzzle(4, 4, [[4,6,1,0],[3,5,2,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_row0_tile(3), "ldllurrdlurdlurrdluldrruld", "test5 solve_row0_tile")
    
    # report number of tests and failures
    suite.report_results()

def run_test_solve_2x2():
    """
    Tests for verifying Puzzle method solve_2x2
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    #test 1: 2x2 board, solvable, homework question 4
    puzzle = mycode.Puzzle(2, 2, [[2,1],[3,0]])
    suite.run_test(puzzle.solve_2x2(), "lu", "test1 solve_2x2") 
    
    #test 2: 2x2 board, solvable, homework question 5
    puzzle = mycode.Puzzle(2, 2, [[3,2],[1,0]])
    suite.run_test(puzzle.solve_2x2(), "lurdlu", "test2 solve_2x2") 
    
    # report number of tests and failures
    suite.report_results()

def run_test_solve_puzzle():
    """
    Tests for verifying Puzzle method solve_puzzle
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    #test1, 2x2, solvable
    puzzle = mycode.Puzzle(2, 2, [[2,1],[3,0]])
    suite.run_test(puzzle.solve_puzzle(), "lu", "test1 solve_puzzle.")
    
    #test2, 3x3, solvable
    puzzle = mycode.Puzzle(3, 3, [[2,4,0],[3,1,5],[6,7,8]])
    suite.run_test(puzzle.solve_puzzle(), "ddulduldurrulduldruldurdlurrdluldrruldlu", "test2 solve_puzzle.")
    
    #test3, 4x4, solvable
    puzzle = mycode.Puzzle(4, 4, [[4,6,1,3],[5,2,0,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzzle.solve_puzzle(), "drduldulduldurrrlulduldurrrlurlduldruldurldlu", "test3 solve_puzzle")
    
    #test4, 3x3, solvable
    puzzle = mycode.Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
    suite.run_test(puzzle.solve_puzzle(), "ululdrruldrulddrulduldrulduruldruldrdlurdluurddlurrllurrdlurldlurdlurrdluldrruldlurdlu", "test4 solve_puzzle")
    
    #test5, 4x4, solvable?
    puzzle = mycode.Puzzle(4, 4, [[14,2,7,12], [8,4,6,3], [1,9,10,0], [13,5,15,11]])
    suite.run_test(puzzle.solve_puzzle(), "dlululurdlurrdldrulddruldlurururldruldrullddruldrulldruldrdlurdluurddlurrrlullurrdldruldurlldruldrulduurdlruldrdlurdluurddlurrruldruldurlduldurdlurrdluldrruldlurldlurdlurrdluldrruldlurdlu", "test5 solve_puzzle")
    
    #test6, 4x4, solvable
    puzzle = mycode.Puzzle(4, 4, [[4,11,1,3], [12,0,5,2], [13,6,9,7], [14,10,8,15]])
    suite.run_test(puzzle.solve_puzzle(), "drdrlllurrdlluurdlruldrdlurdluurddlurrrululdrruldrulddruldluulddruldurlruldrdlurdluurddlurrrlurlduldurdlurrdluldrruldulldruldurrdlurldlu", "test6 solve_puzzle")
    
    # report number of tests and failures
    suite.report_results()
 
run_test_lower_row_invariant()
run_test_solve_interior_tile()
run_test_solve_col0_tile()
run_test_row1_invariant()
run_test_row0_invariant()
run_test_solve_row1_tile()
run_test_solve_row0_tile()    
run_test_solve_2x2()
run_test_solve_puzzle()

