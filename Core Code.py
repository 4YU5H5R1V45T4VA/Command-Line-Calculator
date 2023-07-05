import re
import sys
from typing import List, Tuple
from PyQt5.QtWidgets import *


class Token:
    def __init__(self, token_type, token_value):
        self.type = token_type
        self.value = token_value


class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = []
        self.current_token = None
        self.token_index = 0

    def tokenize(self):
        tokens = []
        # remove white spaces
        expression = re.sub(r"\s+", "", self.expression)
        # tokenize
        while len(expression) > 0:
            if re.match(r"\d+", expression):
                match = re.match(r"\d+", expression)
                tokens.append(Token("NUMBER", match.group(0)))
                expression = expression[len(match.group(0)):]
            elif expression[0] in ["+", "-", "*", "/"]:
                tokens.append(Token("OPERATOR", expression[0]))
                expression = expression[1:]
            else:
                raise Exception("Invalid character in expression")
        self.tokens = tokens

    def get_next_token(self):
        if self.token_index >= len(self.tokens):
            return Token("EOF", None)
        token = self.tokens[self.token_index]
        self.token_index += 1
        return token


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        self.lexer.tokenize()
        self.current_token = self.lexer.get_next_token()
        result = self.parse_expression()
        if self.current_token.type != "EOF":
            raise Exception("Invalid syntax")
        return result

    def parse_expression(self):
        result = self.parse_term()
        while self.current_token.type == "OPERATOR" and self.current_token.value in ["+", "-"]:
            operator_token = self.current_token
            self.current_token = self.lexer.get_next_token()
            right_operand = self.parse_term()
            if operator_token.value == "+":
                result += right_operand
            else:
                result -= right_operand
        return result

    def parse_term(self):
        result = self.parse_factor()
        while self.current_token.type == "OPERATOR" and self.current_token.value in ["*", "/"]:
            operator_token = self.current_token
            self.current_token = self.lexer.get_next_token()
            right_operand = self.parse_factor()
            if operator_token.value == "*":
                result *= right_operand
            else:
                result /= right_operand
        return result

    def parse_factor(self):
        if self.current_token.type == "NUMBER":
            result = float(self.current_token.value)
            self.current_token = self.lexer.get_next_token()
            return result
        elif self.current_token.type == "OPERATOR" and self.current_token.value == "-":
            self.current_token = self.lexer.get_next_token()
            result = self.parse_factor()
            return -result
        elif self.current_token.type == "LPAREN":
            self.current_token = self.lexer.get_next_token()
            result = self.parse_expression()
            if self.current_token.type != "RPAREN":
                raise Exception("Missing closing parenthesis")
            self.current_token = self.lexer.get_next_token()
            return result
        else:
            raise Exception("Invalid syntax")


class CalculatorUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator")

        self.input_label = QLabel("Enter expression:")
        self.input_edit = QLineEdit()
        self.result_label = QLabel("Result:")
        self.result_edit = QLineEdit()
        self.result_edit.setReadOnly

