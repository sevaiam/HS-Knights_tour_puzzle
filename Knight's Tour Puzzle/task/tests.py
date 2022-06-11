# from hstest.stage_test import StageTest
from hstest.stage_test import *
from hstest.test_case import TestCase, SimpleTestCase
from hstest.check_result import CheckResult
from copy import deepcopy
import random
from hstest.exception.outcomes import ErrorWithFeedback

# constants
DIRECTIONS = 8
move_x = [2, 1, -1, -2, -2, -1, 1, 2]
move_y = [1, 2, 2, 1, -1, -2, -2, -1]


def digits(num):
    return len(str(num))


def checkMove(board):
    movelist = []
    lastx = moves[-1][0]
    lasty = moves[-1][1]
    for i in range(DIRECTIONS):
        new_x = lastx + move_x[i]  # user coordinates 1 - n
        new_y = lasty + move_y[i]  # user coordinates 1 - n
        if new_x in range(1, ncols + 1) and new_y in range(1, nrows + 1) and (
                "_" in board[new_y - 1][new_x - 1] or board[new_y - 1][new_x - 1].isnumeric()):
            movelist.append([new_x, new_y])

    for i in range(ncols):  # i = x = cols
        for j in range(nrows):  # j = y = rows
            if [i + 1, j + 1] in movelist:
                possible = warnsdorff(i + 1, j + 1, board)
                if board[j][i] != str(possible):
                    return False, CheckResult.wrong("Incorrect value or marker missing from possible move")
            elif i + 1 == lastx and j + 1 == lasty:
                try:
                    if board[j][i] not in ["x", "X"]:
                        return False, CheckResult.wrong("Incorrect starting position or marker")
                except IndexError:
                    return False, CheckResult.wrong("The board is not set up correctly")
            elif [i + 1, j + 1] in moves:
                if board[j][i] != "*":
                    return False, CheckResult.wrong("Incorrect marker or marker missing from previous move")
            else:
                try:
                    if "_" not in board[j][i]:
                        return False, CheckResult.wrong("Markers placed in wrong location")
                except IndexError:
                    return False, CheckResult.wrong("The board is not set up correctly")
    return True, CheckResult.correct()


def warnsdorff(cur_x, cur_y, board):
    possible = 0
    for i in range(DIRECTIONS):
        new_x = cur_x + move_x[i]  # user coordinates 1 - n
        new_y = cur_y + move_y[i]  # user coordinates 1 - n
        if validMove(new_x, new_y, board):
            possible += 1
    return possible


def validMove(x, y, board):  # user coordinates 1 - n
    if not onBoard(x, y):
        return False
    if not "_" in board[y - 1][x - 1] and not board[y - 1][x - 1].isnumeric():
        return False
    return True


def onBoard(x, y):  # user coordinates 1 - n
    if x > 0 and y > 0 and x <= ncols and y <= nrows:
        return True
    return False

def unique_nums(board):
    result = []
    for row in board:
        for num in row:
            if num.isnumeric():
                result.append(num)
    result = set(result)
    return len(result) == spaces_sol

def check_knights_move(board):
    curr_x, curr_y = 0, 0
    for i in range(1, spaces_sol+1):
        for y, row in enumerate(board):
            for x, num in enumerate(row):
                if int(num) == i:
                    last_x, last_y = curr_x, curr_y
                    curr_x = x
                    curr_y = y
                    break
        if i != 1:
            x_space = abs(last_x - curr_x)
            y_space = abs(last_y - curr_y)
            if (x_space != 2 or y_space != 1) and (x_space != 1 or y_space != 2):
                return False
    return True


random.seed()
ncols = 4
nrows = 3
moves = [[1, 1], [3, 2], [1, 3], [2, 1]]
yaxiswidth = digits(nrows)
xaxiswidth = digits(nrows * ncols)
size = str(ncols) + " " + str(nrows)
x_start = random.randint(3, ncols)
y_start = random.randint(3, nrows)
start = str(x_start) + " " + str(y_start)

random.seed()
ncols_sol = random.choice([5])
nrows_sol = random.choice([5])
yaxiswidth_sol = digits(nrows_sol)
xaxiswidth_sol = digits(nrows_sol * ncols_sol)
size_sol = str(ncols_sol) + " " + str(nrows_sol)
x_start_sol = random.randint(1, 1)
y_start_sol = random.randint(5, 5)
start_sol = str(x_start_sol) + " " + str(y_start_sol)
spaces_sol = ncols_sol*nrows_sol


class KnightsTourTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [
                TestCase(stdin=[self.check_request_size, self.check_request_start, self.check_request_mode]),
                TestCase(stdin=["0 10", self.check_bounds]),
                TestCase(stdin=["1", self.check_length]),
                TestCase(stdin=["a 10", self.check_num]),
                TestCase(stdin=[size, "0 10", self.check_bounds]),
                TestCase(stdin=[size, "1", self.check_length]),
                TestCase(stdin=[size, "a 1", self.check_num]),
                TestCase(stdin=[size, start, "t", self.check_mode]),
                TestCase(stdin=[size, start, " ", self.check_mode]),
                TestCase(stdin=[size, start, "-1", self.check_mode]),

                # player tries board, possible solution case
                TestCase(stdin=["4 3", "1 1", "y", self.check_input_accepted], check_function=self.check_soln_exist),   # check input accepted
                TestCase(stdin=["4 3", "1 1", "y", "1 1", self.check_valid_move], check_function=self.check_soln_exist),  # choose taken spot
                TestCase(stdin=["4 3", "1 1", "y", "1 2", self.check_knight_move], check_function=self.check_soln_exist),  # not knight's move
                TestCase(stdin=["4 3", "1 1", "y", "3 2", "3 2", self.check_valid_move], check_function=self.check_soln_exist),  # choose taken spot
                TestCase(stdin=["4 3", "1 1", "y", "3 2", "3 3", self.check_knight_move], check_function=self.check_soln_exist),  # not knight's move
                TestCase(stdin=["4 3", "1 1", "y", "2 3", "3 1", "4 3", "2 2", "4 1", "3 3", "2 1", "1 3", "3 2"], attach="10",
                         check_function=self.check_dead_end),
                TestCase(stdin=["4 3", "1 1", "y", "3 2", "1 3", "2 1", self.check_progress], check_function=self.check_soln_exist),
                TestCase(
                    stdin=["4 3", "1 1", "y", "3 2", "1 3", "2 1", "4 2", "2 3", "3 1", "1 2", "3 3", "4 1", "2 2", "4 3"],
                    check_function=self.check_finish),

                # player tries board, no solution case
                TestCase(stdin=["3 3", "1 1", "y", self.check_no_soln1], check_function=self.check_no_soln2),  # board not possible

                # generate solution, no solution case
                TestCase(stdin=["3 3", "1 1", "n", self.check_input_accepted], check_function=self.check_no_soln2, time_limit=0),  # no board not possible

                # generate solution, solution exists
                TestCase(stdin=["5 5", "1 1", "n", self.check_input_accepted], check_function=self.check_soln_exist, time_limit=0),
                TestCase(stdin=[size_sol, start_sol, "n"], check_function=self.check_solution, time_limit=0),
                ]

    def check_soln_exist(self, reply: str, attach: Any) -> CheckResult:
        reply = reply.lower()
        if "here" not in reply or "solution" not in reply:
            return CheckResult.wrong("Solution should exist. You need to show the solution and a message")
        return CheckResult.correct()

    def check_no_soln1(self, output):
        output = output.lower()
        if "invalid" not in output:
            return CheckResult.wrong("You need to check if there are solutions for the board")
        return CheckResult.correct()

    def check_no_soln2(self, reply: str, attach: Any) -> CheckResult:
        for line in reply.lower().split("\n")[-2:-1]:
            if "exist" in line:
                break
        else:
            return CheckResult.wrong("No solution should exist, you need to check if there are solutions for the board")
        return CheckResult.correct()

    def check_input_accepted(self, output):
        output = output.lower()
        if "invalid" in output:
            return CheckResult.wrong("Input was not accepted")
        return CheckResult.correct()

    def check_request_size(self, output):
        output = output.lower()
        if "dimension" not in output:
            return CheckResult.wrong("Your program should ask for the board dimensions")
        return size

    def check_request_start(self, output):
        output = output.lower()
        if "position" not in output:
            return CheckResult.wrong("Your program should ask for the knight's starting position")
        return start

    def check_request_mode(self, output):
        output=output.lower()
        if "puzzle" not in output or "try" not in output:
            return CheckResult.wrong("Your program should ask if the player wants to try the puzzle")
        return CheckResult.correct()

    def check_bounds(self, output):
        if "invalid" not in output.lower():
            return CheckResult.wrong("Your program should check if the board size and position are within bounds")
        return CheckResult.correct()

    def check_length(self, output):
        if "invalid" not in output.lower():
            return CheckResult.wrong("Your program should check if there are the right number of inputs")
        return CheckResult.correct()

    def check_num(self, output):
        if "invalid" not in output.lower():
            return CheckResult.wrong("Your program should only accept integer inputs")
        return CheckResult.correct()

    def check_mode(self, output):
        if "invalid" not in output.lower():
            return CheckResult.wrong("Your program should only accept 'y' or 'n'")
        return CheckResult.correct()

    def check_next_move(self, output):
        if "move" not in output.lower():
            return CheckResult.wrong("Your program should only accept integer inputs")
        return CheckResult.correct()

    def check_valid_move(self, output):
        output = output.lower().split("\n")[-1]
        if "invalid" not in output:
            return CheckResult.wrong("Your program should check if the space has already been visited")
        if "move" not in output:
            return CheckResult.wrong("Your program should ask for another move")
        return CheckResult.correct()

    def check_knight_move(self, output):
        output = output.lower().split("\n")[-1]
        if "invalid" not in output:
            return CheckResult.wrong("Your program should only accept L-shaped knight moves")
        return CheckResult.correct()

    def check_dead_end(self, reply: str, attach: Any) -> CheckResult:
        for line in reply.lower().split("\n")[-4:-1]:
            if "possible" in line:
                break
        else:
            return CheckResult.wrong("You need check if there are no more possible moves")

        for line in reply.lower().split("\n")[-4:-1]:
            if attach in line:
                break
        else:
            return CheckResult.wrong("Number of moves taken is incorrect or not displayed")
        return CheckResult.correct()

    def check_finish(self, reply: str, attach: Any) -> CheckResult:
        for line in reply.lower().split("\n")[-2:-1]:
            if "tour" in line:
                break
        else:
            return CheckResult.wrong("End of game message missing.\n"
                                     "Expected output: 'What a great tour! Congratulations!'")
        return CheckResult.correct()

    def check_progress(self, reply):
        # check output
        try:
            if reply == "":
                return CheckResult.wrong("Output was empty")
            border = "-" * (ncols * (xaxiswidth + 1) + 3) + "\n"
            if border not in reply:
                return CheckResult.wrong(f"The board borders aren't found.\n"
                                         f"For a board of {ncols} columns and cell width {xaxiswidth}, \n"
                                         f"the following line should be printed as a border:\n"
                                         f"{border}\n"
                                         f"That is, a line of length {len(border)}.")
            reply = reply.split(border)
            if len(reply) != 3:
                return CheckResult.wrong("Incorrect border or spacing. \n"
                                         "There should be 2 identical borders for a board.\n"
                                         f"For a board of {ncols} columns and cell width {xaxiswidth}, \n"
                                         f"the following line should be printed as a border:\n"
                                         f"{border}\n"
                                         f"That is, a line of length {len(border)}.")
        except:
            return CheckResult.wrong("Incorrect output")

        # extract board and xlabels
        try:
            board = reply[1].replace(' | \n', ' |\n')
            board = board.split(" |\n")[0:nrows]
            if len(board) != nrows:
                return CheckResult.wrong("Incorrect side borders or format")
        except IndexError:
            return CheckResult.wrong("Incorrect border or spacing")

        board2 = []
        # iterate through rows to check
        for n, row in enumerate(board):
            rownum = nrows - n
            colnum = n + 1

            # split at left border, check if row split correctly
            row = row.split("|")
            if len(row) != 2:
                return CheckResult.wrong("Incorrect side borders or format")

            if len(row[0].strip()) != yaxiswidth:
                return CheckResult.wrong("Row numbers or side border not aligned")

            board2.append(row[1].split())

        board2 = board2[::-1]
        valid_board, message = checkMove(board2)
        if valid_board:
            pass
        else:
            return message

        return CheckResult.correct()

    def check_solution(self, reply: str, attach: Any) -> CheckResult:
        # check output
        if "no solution exist" in reply.lower():
            return CheckResult.wrong("Your program outputs the line \'No solution exists\' when there's a solution.")
        try:
            if reply == "":
                return CheckResult.wrong("Output was empty")
            border = "-" * (ncols_sol * (xaxiswidth_sol + 1) + 3) + "\n"
            reply = reply.split(border)
            if len(reply) != 3:
                return CheckResult.wrong("Incorrect border or spacing")
        except:
            return CheckResult.wrong("Incorrect output")

        # extract board and xlabels
        try:
            board = reply[1].split(" |\n")[0:nrows_sol]
            if len(board) != nrows_sol:
                return CheckResult.wrong("Incorrect side borders or format")
        except IndexError:
            return CheckResult.wrong("Incorrect border or spacing")

        board2 = []
        # iterate through rows to check
        for n, row in enumerate(board):
            rownum = nrows_sol - n
            colnum = n + 1

            # split at left border, check if row split correctly
            row = row.split("|")
            if len(row) != 2:
                return CheckResult.wrong("Incorrect side borders or format")

            if len(row[0].strip()) != yaxiswidth_sol:
                return CheckResult.wrong("Row numbers or side border not aligned")

            board2.append(row[1].split())

        if not (unique_nums(board2)):
            return CheckResult.wrong("Numbering should start from 1 and all numbers should be unique")

        if not check_knights_move(board2):
            return CheckResult.wrong("Your solution is incorrect, not all moves at knight's moves")
        return CheckResult.correct()

    def check(self, reply: str, attach: Any):
        raise ErrorWithFeedback(f"The program has unexpectedly terminated.\n" +
                                "It finished execution too early, should continue running.")


if __name__ == '__main__':
    KnightsTourTest().run_tests()
